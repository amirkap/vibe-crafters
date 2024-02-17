from Utils import *
from src.connect_to_openai import *
from Playlist import *
from src.connect_to_spotify import *

def get_playlist(playlist: Playlist):
    pass

def get_recommended_artists():
    pass

def convert_to_spotify_params_and_create_playlist():
    openai = OpenAIClass()
    user_input = Playlist(event="casual driving", music_genre="rock", audience_age_range="5-75", year_range="1960-2002")
    response = openai.get_chat_response_from_openai(get_system_prompt(), user_input.__str__())
    params_dict = parse_to_dict(response)
    params_dict["seed_genres"] = user_input["music_genre"].value
    params_dict["seed_artists"] = ["3WrFJ7ztbogyGnTHbHJFl2", "22bE4uQ6baNwSHPVcDxLCe"]
    params_dict["limit"] = 100
    params_dict["market"] = "US"

    full_request = connect.full_request_flow(
        params_dict,
        "TryingNew", "New playlist description")
    print(full_request)

convert_to_spotify_params_and_create_playlist()
