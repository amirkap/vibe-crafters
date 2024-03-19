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
    num_attempts = 3
    # ask openai for the parameters for spotify api
    response = openai.get_chat_response_from_openai(get_main_system_prompt(), get_user_prompt(user_input.__str__()))
    print(f"OpenAI response: {response}")

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

        recommended_tracks = find_min_num_of_tracks_with_gpt_seeds(40, params_dict, spotify, seed_tracks_names, user_input, num_attempts)

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

def find_min_num_of_tracks_with_spotify_seeds(min_num, params_dict, spotify, user_input=None, num_attempts=3):
    attempts = 0
    max_attempts = num_attempts
    unique_tracks = []
    year_range = None
    add_artists = True

    if not params_dict["seed_tracks"] or not params_dict["seed_artists"]:
        return None

    full_seed_tracks = params_dict["seed_tracks"].split(",")
    full_seed_artists = params_dict["seed_artists"].split(",")

    print("full_seed_tracks:", full_seed_tracks)
    print("full_seed_artists:", full_seed_artists)

    if user_input["year_range"]:
        year_range = user_input["year_range"]

    while attempts < max_attempts and len(unique_tracks) < min_num:
        print("indexeds:", attempts*2, attempts*2+2)
        params_dict["seed_tracks"] = ",".join(full_seed_tracks[attempts*2:(attempts*2)+2])
        params_dict["seed_artists"] = ",".join(full_seed_artists[attempts*2:(attempts*2)+2])
        limit_dict_seeds_number(params_dict, add_artists)
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

    return unique_tracks

def find_min_num_of_tracks_with_gpt_seeds(min_num, params_dict, spotify, seed_tracks_names, user_input=None, num_attempts=3):
    attempts = 0
    max_attempts = num_attempts
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

    unique_tracks = [track["id"] for track in unique_tracks]
    return unique_tracks

def find_seed_tracks_and_artists_from_spotify(user_input: Playlist, num_attempts):
    spotify = SpotifyAPIClass()
    mood_provided = user_input["mood"] is not None
    playlist_search = f'{user_input["mood"].value if mood_provided else ""} {user_input["music_genre"].value}'
    playlist_response = spotify.search_item('playlist', playlist_search)

    if not playlist_response:
        return None

    playlist_id = playlist_response['playlists']['items'][0]['id']
    if not playlist_id:
        return None

    print(f"Playlist ID: {playlist_id}")
    seed_tracks = get_most_popular_tracks(playlist_id, spotify)
    seed_artists = get_most_popular_artists(playlist_id, spotify)

    return {"seed_tracks": seed_tracks, "seed_artists": seed_artists}



def find_seed_tracks_by_playlist_id(playlist_id, spotify, num_attempts):
    playlist_tracks = spotify.get_playlist_songs(playlist_id)
    if not playlist_tracks:
        return None

    tracks = [track['track']['id'] for track in playlist_tracks['items']]
    if len(tracks) < num_attempts * 2:
        return None

    seed_tracks = random.sample(tracks, num_attempts * 2)
    seed_tracks_str = ",".join(seed_tracks)
    return seed_tracks_str

def find_seed_artists_by_playlist_id(playlist_id, spotify, num_attempts):
    playlist_tracks = spotify.get_playlist_songs(playlist_id)
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
    playlist_tracks = spotify.get_playlist_songs(playlist_id)
    if not playlist_tracks:
        return None

    artists_ids = list(set([track['track']['artists'][0]['id'] for track in playlist_tracks['items']]))
    print(artists_ids)
    if len(artists_ids) < num_attempts * 2:
        return None
    ids_and_popularity = [(artist_id, spotify.get_artist(artist_id)["popularity"]) for artist_id in artists_ids]
    sorted_ids_and_popularity = sorted(ids_and_popularity, key=lambda x: x[1], reverse=True)
    print(sorted_ids_and_popularity)
    seed_artists = [x[0] for x in sorted_ids_and_popularity][:6]
    #seed_artists = sorted(artists_ids, key=lambda x: spotify.get_artist(x)["popularity"], reverse=True)

    return seed_artists

def get_most_popular_tracks(playlist_id, spotify, num_attempts):
    playlist_tracks = spotify.get_playlist_songs(playlist_id)
    if not playlist_tracks:
        return None

    tracks_ids = list(set([track['track']['id'] for track in playlist_tracks['items']]))
    if len(tracks_ids) < num_attempts * 2:
        return None
    ids_and_popularity = [(track_id, spotify.get_track(track_id)["popularity"]) for track_id in tracks_ids]
    sorted_ids_and_popularity = sorted(ids_and_popularity, key=lambda x: x[1], reverse=True)
    seed_tracks = [x[0] for x in sorted_ids_and_popularity][:6]

    return seed_tracks

spotify = SpotifyAPIClass()
# print(find_seed_artists_by_playlist_id("6TeyryiZ2UEf3CbLXyztFA", spotify))
# print(find_seed_tracks_by_playlist_id("6TeyryiZ2UEf3CbLXyztFA", spotify))
#print(get_most_popular_artists("6TeyryiZ2UEf3CbLXyztFA", spotify))
