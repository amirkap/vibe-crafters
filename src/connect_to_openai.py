from dotenv import load_dotenv
import os
from openai import OpenAI



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

    def get_chat_response_from_openai(self, system_prompt, user_input):
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user",
             "content": user_input},
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
    Make sure the the songs you provide are not one of those two songs. 
    The output should be a string of exactly 4 song names separated by commas (2 songs would be in this format: "Let It Be - The Beatles,Shape of You - Ed Sheeran", but you need to provide 4).
    """
    return system_prompt
def get_main_system_prompt():
    system_prompt = """Given a set of user input parameters for a custom playlist creation API, translate these parameters into the corresponding input parameters required for the Spotify API's /recommendations endpoint.
     The user input parameters are as follows:
    - Event: A string describing the type of event (e.g., 'wedding', 'birthday party').
    - Music Genre: A string representing the music genre (e.g., 'pop', 'rock').
    - Mood: A string indicating the mood of the music (e.g., 'happy', 'energetic'). - Optional
    - Year Range: A string representing the range of years for the music (e.g., '2010-2020'). - Optional

    Based on these user input parameters, determine the appropriate values for the following Spotify API parameters, provide only these parameters: 
    - seed_artists (comma-separated string of artists' names, not artist id) provide exactly 2 existing artists.
    - seed_tracks (comma-separated string of track names and their artist, not track id. e.g: "Let It Be - The Beatles,Shape of You - Ed Sheeran")
    IMPORTANT NOTE - THE SEED TRACKS MUST NOT BE BY THE SAME ARTISTS YOU PROVIDE IN SEED ARTISTS, however they should still fit the user input parameters. make sure to provide exactly 2 tracks.
    MAKE SURE TO FIT THE SEED ARTISTS AND SEED TRACKS TO THE REQUESTED MUSIC GENRE AND THE EVENT, AND TO THE MOOD AND YEAR RANGE IF THEY ARE PROVIDED.
    Moreover, make sure to fit the next parameters I will tell you in the same way.
    - min_acousticness, max_acousticness, target_acousticness (float, range: 0-1)
    - min_danceability, max_danceability, target_danceability (float, range: 0-1)
    - min_energy, max_energy, target_energy (float, range: 0-1)
    - min_instrumentalness, max_instrumentalness, target_instrumentalness (float, range: 0-1)
    - min_liveness, max_liveness, target_liveness (float, range: 0-1)
    
    The values for the Spotify API parameters should be derived based on the given user input parameters, taking into account the characteristics of the event, music genre, audience age range, and year range.
    Make sure not to choose extreme values for the parameters, and try to keep them within a reasonable range based on the user input.
    Output the result as a JSON object and nothing else."""
    return system_prompt




# openai = OpenAIClass()
# user_input = Playlist(event="casual driving", music_genre="rock", audience_age_range="5-75", year_range="1960-2002")
# response = openai.get_chat_response_from_openai(get_system_prompt(), user_input.__str__())
# print(response)