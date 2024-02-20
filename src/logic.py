import json

from Utils import *
from src.connect_to_openai import *
from src.Playlist import Playlist
from src.connect_to_spotify import SpotifyAPIClass


def get_playlist(user_input: Playlist):
    return convert_to_spotify_params_and_create_playlist(user_input)


def get_recommended_artists():
    pass


def filter_tracks_by_year_range(recommended_tracks, year_range : str):
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
    # user_input = Playlist(event="University graduation", music_genre="indie", mood="happy", year_range="2010-2020")
    response = openai.get_chat_response_from_openai(get_main_system_prompt(), user_input.__str__())
    print(f"OpenAI response: {response}")
    params_dict = parse_params_to_dict(response)
    if "seed_artists" in params_dict:
        translate_artist_names(params_dict, spotify)
    if "seed_tracks" in params_dict:
        translate_track_names(params_dict, spotify)
    params_dict["seed_genres"] = user_input["music_genre"].value
    params_dict["limit"] = 100
    params_dict["market"] = "US"

    recommended_tracks = find_min_num_of_tracks(40, params_dict, spotify, user_input["year_range"], user_input)

    playlist_url = spotify.create_playlist_with_tracks("KaplanTrying", "yofi tofi", recommended_tracks)
    print(f"Playlist URL: {playlist_url}")
    return playlist_url

def get_new_seed_tracks_names(prev_seed_tracks, user_input: Playlist):
    openai = OpenAIClass()
    response = openai.get_chat_response_from_openai(get_extra_songs_system_prompt(prev_seed_tracks), user_input.__str__())
    print(f"OpenAI new seed tracks response: {response}")
    return response


def find_min_num_of_tracks(min_num, params_dict, spotify, year_range=None, user_input=None, prev_seed_tracks_names=None):
    attempts = 0
    max_attempts = 3
    unique_tracks = []

    while attempts < max_attempts and len(unique_tracks) < min_num:
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
            params_dict['seed_tracks'] = get_new_seed_tracks_names(prev_seed_tracks_names, user_input)
            prev_seed_tracks_names = params_dict['seed_tracks']
            translate_track_names(params_dict, spotify)
            # Ensure seed_artists is not used in the next request
            if 'seed_artists' in params_dict:
                del params_dict['seed_artists']
            # if unique_tracks:
            #     # Use up to 4 unique tracks from the results as seed_tracks for the next attempt
            #     new_seed_tracks_list = [track["id"] for track in unique_tracks[-4:]]
            #     if new_seed_tracks_list:
            #         new_seed_tracks = ','.join(new_seed_tracks_list)
            #         params_dict['seed_tracks'] = new_seed_tracks
            #         # Ensure seed_artists is not used in the next request
            #         if 'seed_artists' in params_dict:
            #             del params_dict['seed_artists']

    return unique_tracks


# convert_to_spotify_params_and_create_playlist()

