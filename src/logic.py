import json

from Utils import *
from src.connect_to_openai import *
from src.Playlist import Playlist
from src.connect_to_spotify import SpotifyAPIClass
from src.streamlit_clustering import find_nearest_neighbors_by_genre
import random


def get_playlist(user_input: Playlist):
    return convert_to_spotify_params_and_create_playlist(user_input)


def get_recommended_artists():
    pass


def filter_tracks_by_year_range(recommended_tracks, year_range: str):
    start_year, end_year = tuple(year_range.split('-'))
    return [track for track in recommended_tracks if start_year <= track["album"]["release_date"][:4] <= end_year]


def translate_artist_names(params_dict, spotify):
    artist_names = params_dict["seed_artists"].split(",")
    artist_ids = [spotify.query_api("get_artist_id", {"artist_name": artist_name}) for artist_name in artist_names]
    params_dict["seed_artists"] = ",".join(artist_ids)


def translate_track_names(params_dict, spotify):
    track_names = params_dict["seed_tracks"]
    track_ids = [spotify.query_api("get_track_id", {"track_name": track_name}) for track_name in track_names]
    params_dict["seed_tracks"] = ",".join(track_ids)


def convert_to_spotify_params_and_create_playlist(user_input: Playlist):
    openai = OpenAIClass()
    spotify = SpotifyAPIClass()

    all_params_given = False
    params_dict = {}
    knn_values_dict = {}

    # ask openai for the parameters for spotify api
    response = openai.get_chat_response_from_openai(get_main_system_prompt(), get_user_prompt(user_input.__str__()))
    print(f"OpenAI response: {response}")

    # extract the parameters from the response
    params_dict = parse_params_to_dict(response)
    knn_values_dict = extract_nearest_neighbours_input(params_dict)
    validate_and_fix_dict(params_dict)

    # correct audio values by differences values
    correct_audio_values_in_place(params_dict)
    correct_audio_values_in_place(knn_values_dict)

    seed_tracks_and_artists = find_seed_tracks_and_artists_from_spotify(user_input)

    if seed_tracks_and_artists and seed_tracks_and_artists["seed_tracks"] and seed_tracks_and_artists["seed_artists"]:
        params_dict["seed_artists"] = seed_tracks_and_artists["seed_artists"]
        params_dict["seed_tracks"] = seed_tracks_and_artists["seed_tracks"]
        all_params_given = True

        recommended_tracks = find_min_num_of_tracks_with_spotify_seeds(40, params_dict, spotify,
                                                                   user_input)

    else:
        # if the seed tracks and artists are not found from spotify, then get them from gpt
        print("Didnt find seed artists\songs from spotify. checking with gpt...")

        while not all_params_given:
            response = openai.get_chat_response_from_openai(get_main_system_prompt(), get_user_prompt(user_input.__str__()))
            print(f"OpenAI response: {response}")

            if not "seed_artists" in params_dict or not "seed_tracks" in params_dict:
                print("Seed artists or seed tracks not provided. Asking for them again...")
                continue
            all_params_given = True

        if "seed_artists" in params_dict:
            translate_artist_names(params_dict, spotify)

        seed_tracks_names = []
        if "seed_tracks" in params_dict:
            seed_tracks_names = params_dict["seed_tracks"].split(",")
            translate_track_names(params_dict, spotify)

        recommended_tracks = find_min_num_of_tracks_with_gpt_seeds(40, params_dict, spotify, seed_tracks_names, user_input)

    params_dict["seed_genres"] = user_input["music_genre"].value
    params_dict["limit"] = 100
    params_dict["market"] = "US"

    if not user_input["year_range"]:
        print(f"KNN values: {knn_values_dict}")
        knn_tracks = find_nearest_neighbors_by_genre(knn_values_dict, user_input["music_genre"].value, 10)
        print(f"KNN tracks: {knn_tracks}")

    else:
        knn_tracks = []

    playlist_url = spotify.create_playlist_with_tracks(user_input["event"], "this is the default description",
                                                       recommended_tracks, knn_tracks)
    print(f"Playlist URL: {playlist_url}")
    return playlist_url


def get_new_seed_tracks_names(prev_seed_tracks, user_input: Playlist):
    openai = OpenAIClass()
    response = openai.get_chat_response_from_openai(get_extra_songs_system_prompt(prev_seed_tracks),
                                                    user_input.__str__())
    print(f"OpenAI new seed tracks response: {response}")
    seed_tracks_list = response.split(",")
    return seed_tracks_list

def find_min_num_of_tracks_with_spotify_seeds(min_num, params_dict, spotify, user_input=None):
    attempts = 0
    max_attempts = 3
    unique_tracks = []
    year_range = None
    add_artists = True

    if not params_dict["seed_tracks"] or not params_dict["seed_artists"]:
        return None

    full_seed_tracks = params_dict["seed_tracks"]
    full_seed_artists = params_dict["seed_artists"]

    if user_input["year_range"]:
        year_range = user_input["year_range"]

    while attempts < max_attempts and len(unique_tracks) < min_num:
        validate_and_fix_dict(params_dict, add_artists)
        print("params for spotify:", json.dumps(params_dict, indent=2))
        # Fetch recommendations based on the current parameters
        recommended_tracks = spotify.query_api("get_recommendations", params_dict)

        if "error" in recommended_tracks:
            print(f"Error in get_recommendations()! Returned value is: {recommended_tracks}")
            return recommended_tracks

        if year_range:
            print(f"Before filtering: {len(recommended_tracks)} tracks")
            recommended_tracks = filter_tracks_by_year_range(recommended_tracks, year_range)
            print(f"After filtering: {len(recommended_tracks)} tracks")

        # Add new unique tracks to the set
        for track in recommended_tracks:
            if track not in unique_tracks:
                unique_tracks.append(track)

        print(f"Unique tracks after adding to list: {len(unique_tracks)}")
        # Check if the results meet the desired count
        if len(unique_tracks) >= min_num:
            break
        else:
            # If not enough unique tracks, prepare for another attempt
            attempts += 1
            print(f"Attempt #{attempts}: Unique tracks so far: {len(unique_tracks)}. Trying to find more...")
            add_artists = False
            params_dict['seed_tracks'] = get_new_seed_tracks_names(seed_tracks_list, user_input)
            seed_tracks_list.append(params_dict['seed_tracks'].split(","))
            translate_track_names(params_dict, spotify)

    return unique_tracks

def find_min_num_of_tracks_with_gpt_seeds(min_num, params_dict, spotify, seed_tracks_names, user_input=None):
    attempts = 0
    max_attempts = 4
    unique_tracks = []
    seed_tracks_list = seed_tracks_names.split(",")
    year_range = None
    add_artists = True

    if user_input["year_range"]:
        year_range = user_input["year_range"]

    while attempts < max_attempts and len(unique_tracks) < min_num:
        validate_and_fix_dict(params_dict, add_artists)
        print("params for spotify:", json.dumps(params_dict, indent=2))
        # Fetch recommendations based on the current parameters
        recommended_tracks = spotify.query_api("get_recommendations", params_dict)

        if "error" in recommended_tracks:
            print(f"Error in get_recommendations()! Returned value is: {recommended_tracks}")
            return recommended_tracks

        if year_range:
            print(f"Before filtering: {len(recommended_tracks)} tracks")
            recommended_tracks = filter_tracks_by_year_range(recommended_tracks, year_range)
            print(f"After filtering: {len(recommended_tracks)} tracks")

        # Add new unique tracks to the set
        for track in recommended_tracks:
            if track not in unique_tracks:
                unique_tracks.append(track)

        print(f"Unique tracks after adding to list: {len(unique_tracks)}")
        # Check if the results meet the desired count
        if len(unique_tracks) >= min_num:
            break
        else:
            # If not enough unique tracks, prepare for another attempt
            attempts += 1
            print(f"Attempt #{attempts}: Unique tracks so far: {len(unique_tracks)}. Trying to find more...")
            add_artists = False
            params_dict['seed_tracks'] = get_new_seed_tracks_names(seed_tracks_list, user_input)
            seed_tracks_list.append(params_dict['seed_tracks'])
            translate_track_names(params_dict, spotify)

    return unique_tracks

def find_seed_tracks_and_artists_from_spotify(user_input: Playlist):
    spotify = SpotifyAPIClass()
    playlist_search = f'{user_input["music_genre"].value} {user_input["mood"].value}'
    playlist_response = spotify.search_item('playlist', playlist_search)

    if not playlist_response:
        return None

    playlist_id = playlist_response['playlists']['items'][0]['id']
    if not playlist_id:
        return None

    seed_tracks = find_seed_tracks_by_playlist_id(playlist_id, spotify)
    seed_artists = find_seed_artists_by_playlist_id(playlist_id, spotify)

    return {"seed_tracks": seed_tracks, "seed_artists": seed_artists}



def find_seed_tracks_by_playlist_id(playlist_id, spotify):
    playlist_tracks = spotify.get_playlist_songs(playlist_id)
    if not playlist_tracks:
        return None

    tracks = [track['track']['uri'] for track in playlist_tracks['items']]
    if len(tracks) < 4:
        return None

    seed_tracks = random.sample(tracks, 6)
    return seed_tracks

def find_seed_artists_by_playlist_id(playlist_id, spotify):
    playlist_tracks = spotify.get_playlist_songs(playlist_id)
    if not playlist_tracks:
        return None

    artists = [track['track']['artists'][0]['name'] for track in playlist_tracks['items']]
    if len(artists) < 4:
        return None

    seed_artists = random.sample(artists, 6)
    return seed_artists


spotify = SpotifyAPIClass()
print(find_seed_artists_by_playlist_id("37i9dQZF1DX76Wlfdnj7AP", spotify))
print("TESTTTTT")