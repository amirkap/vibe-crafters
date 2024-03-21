import json
from src.utils.Utils import *
from src.services.connect_to_openai import *
from src.models.Playlist import Playlist
from src.services.connect_to_spotify import SpotifyAPIClass
from src.songs_dataset.dataset_manipulation import find_nearest_neighbors_by_genre
import random


def get_playlist(user_input: Playlist):
    """
    This function is the main entry point for the API. It takes a Playlist object as input and returns a URL to a Spotify.
    Args:
        user_input: A Playlist object containing the user's input parameters.

    Returns:
        A string containing the URL to the playlist on Spotify.
    """
    return convert_to_spotify_params_and_create_playlist(user_input)


def filter_tracks_by_decade(recommended_tracks, decade: str):
    """
    Filter the recommended tracks by the given year range.
    Args:
        recommended_tracks: A list of dictionaries representing the recommended tracks.
        decade: A string representing the year range in the format "start_year-end_year".

    Returns:
        A list of dictionaries representing the filtered recommended tracks.
    """

    decade_years = get_decades_start_and_end_years()
    start_year, end_year = decade_years[decade]["start_year"], decade_years[decade]["end_year"]
    return [track for track in recommended_tracks if start_year <= int(track["album"]["release_date"][:4]) <= end_year]


def translate_artist_names(params_dict, spotify):
    """
    Translate the artist names to their corresponding Spotify IDs.
    Args:
        params_dict: A dictionary containing the input parameters for the Spotify API.
        spotify: An instance of the SpotifyAPIClass.
    """
    artist_names = params_dict["seed_artists"].split(",")
    artist_ids = [spotify.query_api("get_artist_id", {"artist_name": artist_name}) for artist_name in artist_names]
    params_dict["seed_artists"] = ",".join(artist_ids)


def translate_track_names(params_dict, spotify):
    """
    Translate the track names to their corresponding Spotify IDs.
    Args:
        params_dict: A dictionary containing the input parameters for the Spotify API.
        spotify: An instance of the SpotifyAPIClass.
    """
    track_names = params_dict["seed_tracks"].split(",")
    track_ids = [spotify.query_api("get_track_id", {"track_name": track_name}) for track_name in track_names]
    params_dict["seed_tracks"] = ",".join(track_ids)


def convert_to_spotify_params_and_create_playlist(user_input: Playlist):
    """
    The main logic for the API. It takes a Playlist object as input, converts the input parameters to the corresponding
    Spotify API parameters, and creates a playlist on Spotify.
    Args:
        user_input: A Playlist object containing the user's input parameters.

    Returns:
        A string containing the URL to the playlist on Spotify.
    """
    openai = OpenAIClass()
    spotify = SpotifyAPIClass()

    all_params_given = False
    params_dict = {}
    knn_values_dict = {}
    num_attempts = 3
    # ask openai for the parameters for spotify api
    response = openai.get_chat_response_from_openai(get_main_system_prompt(), get_user_prompt(user_input.__str__()))

    # extract the parameters from the response
    params_dict = parse_params_to_dict(response)
    knn_values_dict = extract_nearest_neighbours_input(params_dict)
    validate_and_fix_dict(params_dict)

    params_dict["seed_genres"] = user_input["music_genre"].value
    params_dict["limit"] = 100
    params_dict["market"] = "US"

    # correct audio values by differences values
    correct_audio_values_in_place(params_dict)
    correct_audio_values_in_place(knn_values_dict)

    seed_tracks_and_artists = find_seed_tracks_and_artists_from_spotify(user_input, num_attempts)

    if seed_tracks_and_artists and seed_tracks_and_artists["seed_tracks"] and seed_tracks_and_artists["seed_artists"]:
        params_dict["seed_artists"] = seed_tracks_and_artists["seed_artists"]
        params_dict["seed_tracks"] = seed_tracks_and_artists["seed_tracks"]
        all_params_given = True

        recommended_tracks = find_min_num_of_tracks_with_spotify_seeds(40, params_dict, spotify,
                                                                   user_input, num_attempts)

    else:
        # if the seed tracks and artists are not found from spotify, then get them from gpt
        while not all_params_given:
            response = openai.get_chat_response_from_openai(get_main_system_prompt(), get_user_prompt(user_input.__str__()))

            if not "seed_artists" in params_dict or not "seed_tracks" in params_dict:
                continue
            all_params_given = True

        if "seed_artists" in params_dict:
            translate_artist_names(params_dict, spotify)

        seed_tracks_names = []
        if "seed_tracks" in params_dict:
            seed_tracks_names = params_dict["seed_tracks"].split(",")
            translate_track_names(params_dict, spotify)

        recommended_tracks = find_min_num_of_tracks_with_gpt_seeds(40, params_dict, spotify, seed_tracks_names, user_input, num_attempts)

    if not user_input["decade"]:
        knn_tracks = find_nearest_neighbors_by_genre(knn_values_dict, user_input["music_genre"].value, 10)

    else:
        knn_tracks = []

    playlist_description = get_playlist_description(user_input["event"])
    playlist_url = spotify.query_api("create_playlist_with_tracks", {"name": user_input["event"],
                                                                    "description": playlist_description,
                                                                    "tracks_list": recommended_tracks,
                                                                     "neighbor_tracks_list": knn_tracks})
    return playlist_url


def get_new_seed_tracks_names(prev_seed_tracks, user_input: Playlist):
    """
    Get new seed tracks based on the user input. The songs have to be different from the previous seed tracks.
    Args:
        prev_seed_tracks: A list of strings representing the previous seed tracks.
        user_input: A Playlist object containing the user's input parameters.

    Returns:
        A list of strings representing the new seed tracks.
    """
    openai = OpenAIClass()
    response = openai.get_chat_response_from_openai(get_extra_songs_system_prompt(prev_seed_tracks),
                                                    user_input.__str__())
    seed_tracks_list = response.split(",")
    return seed_tracks_list

def find_min_num_of_tracks_with_spotify_seeds(min_num, params_dict, spotify, user_input, num_attempts=3):
    """
    Find the minimum number of unique tracks based on the given input parameters, extracting
    seed songs from the Spotify API.
    Args:
        min_num: An integer representing the minimum number of unique tracks to find.
        params_dict: A dictionary containing the input parameters for the Spotify API.
        spotify: An instance of the SpotifyAPIClass.
        user_input: A Playlist object containing the user's input parameters.
        num_attempts: An integer representing the maximum number of attempts to make.

    Returns:
        A list of strings representing the unique track IDs or None if an error occurred.
    """
    attempts = 0
    max_attempts = num_attempts
    unique_tracks = []
    decade = None
    add_artists = True

    if not params_dict["seed_tracks"] or not params_dict["seed_artists"]:
        return None


    full_seed_tracks = params_dict["seed_tracks"].split(",")
    full_seed_artists = params_dict["seed_artists"].split(",")
    if user_input["decade"]:
        decade = user_input["decade"]

    while attempts < max_attempts and len(unique_tracks) < min_num:
        params_dict["seed_tracks"] = ",".join(full_seed_tracks[attempts*2:(attempts*2)+2])
        params_dict["seed_artists"] = ",".join(full_seed_artists[attempts*2:(attempts*2)+2])
        limit_dict_seeds_number(params_dict, add_artists)
        # Fetch recommendations based on the current parameters
        recommended_tracks = spotify.query_api("get_recommendations", params_dict)

        if "error" in recommended_tracks:
            return recommended_tracks

        if decade:
            recommended_tracks = filter_tracks_by_decade(recommended_tracks, decade)

        # Add new unique tracks to the set
        for track in recommended_tracks:
            if track not in unique_tracks:
                unique_tracks.append(track)

        # Check if the results meet the desired count
        if len(unique_tracks) >= min_num:
            break
        else:
            # If not enough unique tracks, prepare for another attempt
            attempts += 1

    return unique_tracks

def find_min_num_of_tracks_with_gpt_seeds(min_num, params_dict, spotify, seed_tracks_names, user_input, num_attempts=3):
    """
    Find the minimum number of unique tracks based on the given input parameters, extracting
    seed songs from the Openai API. Trying to find seed tracks that are not in the previous seed tracks.
    Args:
        min_num: An integer representing the minimum number of unique tracks to find.
        params_dict: A dictionary containing the input parameters for the Spotify API.
        spotify: An instance of the SpotifyAPIClass.
        seed_tracks_names: A list of strings representing the seed track names.
        user_input: A Playlist object containing the user's input parameters.
        num_attempts: An integer representing the maximum number of attempts to make.

    Returns:
        A list of strings representing the unique track IDs or None if an error occurred.
    """
    attempts = 0
    max_attempts = num_attempts
    unique_tracks = []
    seed_tracks_list = seed_tracks_names.split(",")
    decade = None
    add_artists = True

    if user_input["decade"]:
        decade = user_input["decade"]

    while attempts < max_attempts and len(unique_tracks) < min_num:
        validate_and_fix_dict(params_dict, add_artists)
        # Fetch recommendations based on the current parameters
        recommended_tracks = spotify.query_api("get_recommendations", params_dict)

        if "error" in recommended_tracks:
            return recommended_tracks

        if decade:
            recommended_tracks = filter_tracks_by_decade(recommended_tracks, decade)

        # Add new unique tracks to the set
        for track in recommended_tracks:
            if track not in unique_tracks:
                unique_tracks.append(track)

        # Check if the results meet the desired count
        if len(unique_tracks) >= min_num:
            break
        else:
            # If not enough unique tracks, prepare for another attempt
            attempts += 1
            add_artists = False
            params_dict['seed_tracks'] = get_new_seed_tracks_names(seed_tracks_list, user_input)
            seed_tracks_list.append(params_dict['seed_tracks'])
            params_dict['seed_tracks'] = ",".join(params_dict['seed_tracks'])
            translate_track_names(params_dict, spotify)

    unique_tracks = [track["id"] for track in unique_tracks]
    return unique_tracks

def find_seed_tracks_and_artists_from_spotify(user_input: Playlist, num_attempts=3):
    """
    Find seed tracks and artists based on the given input parameters, extracting seed songs from the Spotify API.
    Args:
        user_input: A Playlist object containing the user's input parameters.
        num_attempts: An integer representing the maximum number of attempts to make (important in order to know
        how many seed tracks and artists to return).

    Returns:
        A dictionary containing the seed tracks and artists or None if an error occurred.
    """
    spotify = SpotifyAPIClass()
    mood_provided = user_input["mood"] is not None
    decade_provided = user_input["decade"] is not None
    playlist_search = f'{user_input["decade"].value if decade_provided else ""} {user_input["mood"].value if mood_provided else ""} {user_input["music_genre"].value}'
    playlist_response = spotify.query_api("search_item", {"item_type": "playlist", "query": playlist_search})

    if not playlist_response:
        return None

    playlist_id = playlist_response['playlists']['items'][0]['id']
    if not playlist_id:
        return None

    seed_tracks = get_most_popular_tracks(playlist_id, spotify, num_attempts)
    seed_artists = get_most_popular_artists(playlist_id, spotify, num_attempts)

    return {"seed_tracks": seed_tracks, "seed_artists": seed_artists}



def find_seed_tracks_by_playlist_id(playlist_id, spotify, num_attempts):
    """
    Find seed tracks based on the given playlist ID. Selects tracks randomly from the playlist.
    Finds two tracks for every attempt.
    Args:
        playlist_id: A string representing the playlist ID.
        spotify: An instance of the SpotifyAPIClass.
        num_attempts: An integer representing the maximum number of attempts to make.

    Returns:
        A string containing the seed tracks or None if an error occurred.
    """
    playlist_tracks = spotify.query_api("get_playlist_songs", {"playlist_id": playlist_id})
    if not playlist_tracks:
        return None

    tracks = [track['track']['id'] for track in playlist_tracks['items']]
    if len(tracks) < num_attempts * 2:
        return None

    seed_tracks = random.sample(tracks, num_attempts * 2)
    seed_tracks_str = ",".join(seed_tracks)
    return seed_tracks_str

def find_seed_artists_by_playlist_id(playlist_id, spotify, num_attempts):
    """
    Find seed artists based on the given playlist ID. Selects artists randomly from the playlist.
    Finds two artists for every attempt.
    Args:
        playlist_id: A string representing the playlist ID.
        spotify: An instance of the SpotifyAPIClass.
        num_attempts: An integer representing the maximum number of attempts to make.

    Returns:
        A string containing the seed artists or None if an error occurred.
    """
    playlist_tracks = spotify.query_api("get_playlist_songs", {"playlist_id": playlist_id})
    if not playlist_tracks:
        return None

    artists = [track['track']['artists'][0]['id'] for track in playlist_tracks['items']]

    # remove duplicates
    artists = list(set(artists))

    if len(artists) < num_attempts * 2:
        return None

    seed_artists = random.sample(artists, num_attempts * 2)
    seed_artists_str = ",".join(seed_artists)
    return seed_artists_str

def get_most_popular_artists(playlist_id, spotify, num_attempts):
    """
    Get the most popular artists based on the given playlist ID.
    Finds two artists for every attempt.
    Args:
        playlist_id: A string representing the playlist ID.
        spotify: An instance of the SpotifyAPIClass.
        num_attempts: An integer representing the maximum number of attempts to make.

    Returns:
        A string containing the seed artists or None if an error occurred.
    """
    playlist_tracks = spotify.query_api("get_playlist_songs", {"playlist_id": playlist_id})
    if not playlist_tracks:
        return None

    artists_ids = list(set([track['track']['artists'][0]['id'] for track in playlist_tracks['items']]))
    if len(artists_ids) < num_attempts * 2:
        return None
    ids_and_popularity = [(artist_id, spotify.query_api("get_artist", {"artist_id": artist_id})["popularity"]) for artist_id in artists_ids]
    sorted_ids_and_popularity = sorted(ids_and_popularity, key=lambda x: x[1], reverse=True)
    seed_artists = [x[0] for x in sorted_ids_and_popularity][:6]
    seed_artists_str = ",".join(seed_artists)
    return seed_artists_str

def get_most_popular_tracks(playlist_id, spotify, num_attempts):
    """
    Gets the most popular tracks based on the given playlist ID. Finds two tracks for every attempt.
    Args:
        playlist_id: A string representing the playlist ID.
        spotify: An instance of the SpotifyAPIClass.
        num_attempts: An integer representing the maximum number of attempts to make.

    Returns:
        A string containing the seed tracks or None if an error occurred.
    """
    playlist_tracks = spotify.query_api("get_playlist_songs", {"playlist_id": playlist_id})
    if not playlist_tracks:
        return None

    tracks_ids = list(set([track['track']['id'] for track in playlist_tracks['items']]))
    if len(tracks_ids) < num_attempts * 2:
        return None

    popularity_list = []
    for i in range(0, len(tracks_ids), 50):
        track_group = tracks_ids[i:i+50]
        tracks = spotify.query_api("get_multiple_tracks", {"track_ids": track_group})
        for track in tracks['tracks']:
            popularity_list.append((track["id"], track["popularity"]))

    sorted_ids_and_popularity = sorted(popularity_list, key=lambda x: x[1], reverse=True)
    seed_tracks = [x[0] for x in sorted_ids_and_popularity][:6]
    seed_tracks_str = ",".join(seed_tracks)
    return seed_tracks_str
