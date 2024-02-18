from Utils import *
from src.connect_to_openai import *
from Playlist import *
from src.connect_to_spotify import SpotifyAPIClass


def get_playlist(playlist: Playlist):
    pass


def get_recommended_artists():
    pass


def filter_tracks_by_year_range(recommended_tracks, year_range : str):
    start_year, end_year = tuple(year_range.split('-'))
    return [track for track in recommended_tracks if start_year <= track["album"]["release_date"][:4] <= end_year]

def translate_artist_names(params_dict, spotify):
    artist_names = params_dict["seed_artists"].split(",")
    artist_ids = [spotify.query_api("get_artist_id", {"artist_name": artist_name}) for artist_name in artist_names]
    params_dict["seed_artists"] = ",".join(artist_ids)

def convert_to_spotify_params_and_create_playlist():
    openai = OpenAIClass()
    spotify = SpotifyAPIClass()
    user_input = Playlist(event="Grandma's 75th birthday", music_genre="jazz", audience_age_range="5-55",
                          year_range="1970-2023")
    response = openai.get_chat_response_from_openai(get_system_prompt(), user_input.__str__())
    print(f"OpenAI response: {response}")
    params_dict = parse_to_dict(response)
    if "seed_artists" in params_dict:
        translate_artist_names(params_dict, spotify)
    params_dict["seed_genres"] = user_input["music_genre"].value
    params_dict["limit"] = 100
    params_dict["market"] = "US"
    print(params_dict)
    recommended_tracks = spotify.query_api("get_recommendations", params_dict)
    if "error" in recommended_tracks:
        print(f"Error in get_recommendations()! Returned value is: {recommended_tracks}")
        return recommended_tracks
    print(f"Before filtering: {len(recommended_tracks)} tracks")
    recommended_tracks = filter_tracks_by_year_range(recommended_tracks, user_input["year_range"])
    print(f"After filtering: {len(recommended_tracks)} tracks")
    playlist_url = spotify.create_playlist_with_tracks("AmirCreatedThis 7", "yofi tofi", recommended_tracks)
    print(f"Playlist URL: {playlist_url}")
    return playlist_url


    # full_request = spotify.full_request_flow(
    #     params_dict,
    #     "AmirCreatedThis 6", "This is a check")
    # print(full_request)





convert_to_spotify_params_and_create_playlist()
# spotify = SpotifyAPIClass()
# print (spotify.query_api("get_artist_id", {"artist_name": "temptations"}))

