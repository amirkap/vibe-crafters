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
    track_names = params_dict["seed_tracks"].split(",")
    track_ids = [spotify.query_api("get_track_id", {"track_name": track_name}) for track_name in track_names]
    params_dict["seed_tracks"] = ",".join(track_ids)


def convert_to_spotify_params_and_create_playlist(user_input: Playlist):
    openai = OpenAIClass()
    spotify = SpotifyAPIClass()

    # make sure all the parameters are given from openai
    all_params_given = False
    params_dict = {}
    knn_values_dict = {}

    while not all_params_given:
        response = openai.get_chat_response_from_openai(get_main_system_prompt(), get_user_prompt(user_input.__str__()))
        print(f"OpenAI response: {response}")

        # extract the parameters from the response
        params_dict = parse_params_to_dict(response)
        knn_values_dict = extract_nearest_neighbours_input(params_dict)
        validate_and_fix_dict(params_dict)

        if not "seed_artists" in params_dict or not "seed_tracks" in params_dict:
            print("Seed artists or seed tracks not provided. Asking for them again...")
            continue
        all_params_given = True

    if "seed_artists" in params_dict:
        translate_artist_names(params_dict, spotify)

    # have to check if the seed tracks is not none and if it is, then get the seed tracks from spotify
    seed_tracks = find_seed_tracks_from_spotify(user_input)

    seed_tracks_names = []
    if "seed_tracks" in params_dict:
        seed_tracks_names = params_dict["seed_tracks"]
        translate_track_names(params_dict, spotify)

    params_dict["seed_genres"] = user_input["music_genre"].value
    params_dict["limit"] = 100
    params_dict["market"] = "US"

    # correct audio values by differences values
    correct_audio_values_in_place(params_dict)
    correct_audio_values_in_place(knn_values_dict)

    recommended_tracks = find_min_num_of_tracks(40, params_dict, spotify, seed_tracks_names, user_input)

    print(f"KNN values: {knn_values_dict}")
    knn_tracks = find_nearest_neighbors_by_genre(knn_values_dict, user_input["music_genre"].value, 10)
    print(f"KNN tracks: {knn_tracks}")

    playlist_url = spotify.create_playlist_with_tracks(user_input["event"], "this is the default description",
                                                       recommended_tracks, knn_tracks)
    print(f"Playlist URL: {playlist_url}")
    return playlist_url


def get_new_seed_tracks_names(prev_seed_tracks, user_input: Playlist):
    openai = OpenAIClass()
    response = openai.get_chat_response_from_openai(get_extra_songs_system_prompt(prev_seed_tracks),
                                                    user_input.__str__())
    print(f"OpenAI new seed tracks response: {response}")
    return response


def find_min_num_of_tracks(min_num, params_dict, spotify, seed_tracks_names, user_input=None):
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
            seed_tracks_list.append(params_dict['seed_tracks'].split(","))
            translate_track_names(params_dict, spotify)

    return unique_tracks

def find_seed_tracks_from_spotify(user_input: Playlist):
    spotify = SpotifyAPIClass()
    playlist_search = f'{user_input["music_genre"].value} {user_input["mood"].value}'
    playlist_response = spotify.search_item('playlist', playlist_search)

    if not playlist_response:
        return None

    if playlist_response:
        playlist_id = playlist_response['playlists']['items'][0]['id']
        if not playlist_id:
            return None

        playlist_tracks = spotify.get_playlist_songs(playlist_id)
        if not playlist_tracks:
            return None

        tracks = [track['track']['uri'] for track in playlist_tracks['items']]
        if len(tracks) < 2:
            return None

        seed_tracks = random.sample(tracks, 2)
        return seed_tracks

# convert_to_spotify_params_and_create_playlist()
