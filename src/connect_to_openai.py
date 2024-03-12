from dotenv import load_dotenv
import os
from openai import OpenAI
# from src.Playlist import Playlist


class OpenAIClass:

    def __init__(self):
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        org_id = os.getenv("OPENAI_ORG_ID")
        client = OpenAI(api_key=api_key, organization=org_id)
        self.client = client

    def get_embedding_from_text(self, text):
        response = self.client.embeddings.create(
            input=text,
            model="text-embedding-ada-002",
        )
        return response.data[0].embedding

    def get_chat_response_from_openai(self, system_prompt, user_prompt):
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user",
             "content": user_prompt},
        ]
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=messages
        )
        return response.choices[0].message.content

    def get_image_from_dalle(self, prompt):
        response = self.client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )

        image_url = response.data[0].url
        return image_url


def get_extra_songs_system_prompt(songs_list):
    system_prompt = f"""Given the following set of user input parameters for a custom playlist creation API:
    - Event: A string describing the type of event (e.g., 'wedding', 'birthday party').
    - Music Genre: A string representing the music genre (e.g., 'pop', 'rock').
    - Mood: A string indicating the mood of the music (e.g., 'happy', 'energetic') - Optional.
    - Year Range: A string representing the range of years for the music (e.g., '2010-2020') - Optional.
    
    Your task is to provide exactly 4 additional songs along with their artists separated by commas, 
    that can be added to the playlist based on the given user input parameters, and based on the following songs: {songs_list}.
    Make sure the tracks you provide were released within the year range if it was provided, and that they fit the music genre and the event.
    Make sure the the songs you provide are not one of those songs, provide only other songs. 
    The output should be a string of exactly 4 song names separated by commas (2 songs would be in this format: "Let It Be - The Beatles,Shape of You - Ed Sheeran", but you need to provide 4). 
    MAKE SURE NOT WRITE ANY ADDITIONAL INFORMATION SUCH AS WHY YOU CHOSE THESE SONGS, ONLY THE SONG NAMES AND THEIR ARTISTS SEPARATED BY COMMAS.
    """
    return system_prompt


def get_main_system_prompt():
    system_prompt = f"""You will be provided with a set of user input parameters for a custom playlist creation API. 
    Your task is to translate these parameters into the input parameters required for the Spotify API '/recommendations' endpoint.
    Your translation should be based on the given user input parameters, taking into account the characteristics of both the 'event' and 'music genre' strings, and the 'mood' string if it is provided.
    Your output should be a JSON object containing the Spotify API parameters that correspond to the given user input parameters, and nothing else.
    """

    return system_prompt


def get_user_prompt(user_input):
    user_prompt = f"""I will provide you with a set of user input parameters for a custom playlist creation API. 
    Translate these parameters into the corresponding input parameters required for the Spotify API's /recommendations endpoint.
      The user input types are as follows:
     - Event: A string describing the type of event (e.g., 'wedding', 'birthday party').
     - Music Genre: A string representing the music genre (e.g., 'pop', 'rock').
     - Mood: A string indicating the mood of the music (e.g., 'happy', 'energetic'). - Optional
     - Year Range: A string representing the range of years for the music (e.g., '2010-2020'). - Optional
     
     The user input parameters are: f{user_input} 
     Based on these user input parameters, determine the appropriate values for the following Spotify API parameters; Provide only these parameters: 
     - seed_artists (comma-separated string of ARTIST NAMES (NOT IDS!)) - PROVIDE EXACTLY 2 ARTIST NAMES.
     - seed_tracks (comma-separated string of track names and their artist (NOT IDS!)). DO NOT PROVIDE TRACKS BY ARTISTS THAT YOU CHOOSE FOR SEED_ARTISTS!!!
     Moreover, make sure to fit the next parameters I will tell you in the same way.
     - target_valence (float, range: 0-1)
     - target_danceability (float, range: 0-1)
     - target_acousticness (float, range: 0-1)
     - target_energy (float, range: 0-1)
     - target_instrumentalness (float, range: 0-1)
     - target_liveness (float, range: 0-1)

     The values for the Spotify API parameters should be derived based on the given user input parameters, taking into account the characteristics of the event, music genre, and mood.
     Output the result as a JSON object and nothing else. DO NOT WRAP IT WITH ```json``` OR ANYTHING ELSE.
     """

    return user_prompt


def get_assemsment_sys_promompt():
    sys_prompt = """You will be provided with a list of track names and their artist. Your goal is to provide the Spotify audio features for each track.
    The input will be a list of track names and their artists. 
    The output should be a list of dictionaries containing the audio features for each track, and nothing else.
    """
    return sys_prompt

def get_assesment_user_prompt(tracks_list):
    user_prompt = f"""I will provide you with a list of track names and their artist. Your goal is to provide the Spotify audio features for each track.
    It might be helpful for you to figure out the track id for each track, and then use the Spotify API to get the audio features for each track.
    The input is:
     {tracks_list}
     
    The output should be a list of dictionaries containing the audio features and the track's name for each track. 
    DO NOT SAY ANYTHING IN YOUR RESPONSE, JUST PROVIDE THE AUDIO FEATURES FOR EVERY TRACK AND NOTHING ELSE.
    DO NOT WRAP IT WITH ```python ``` OR ANYTHING ELSE.
    MAKE SURE YOU PROVIDE ALL THE TRACKS IN THE SAME ORDER AS THEY WERE PROVIDED TO YOU.
    """
    return user_prompt


openai = OpenAIClass()
# user_input = Playlist(event="Casual driving on the coastline", music_genre="indie", mood="happy",
#                       year_range="2010-2020")
# response = openai.get_chat_response_from_openai(get_main_system_prompt(), get_user_prompt(user_input))
# print(response)

