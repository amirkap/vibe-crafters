from dotenv import load_dotenv
import os
from openai import OpenAI
from Playlist import *


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
    
def get_system_prompt():
    system_prompt = """Given a set of user input parameters for a custom playlist creation API, translate these parameters into the corresponding input parameters required for the Spotify API's /recommendations endpoint. The user input parameters are as follows:
    - Event: A string describing the type of event (e.g., 'wedding', 'birthday party').
    - Music Genre: A string representing the music genre (e.g., 'pop', 'rock').
    - Audience Age Range: A string indicating the age range of the audience (e.g., '25-35').
    - Year Range: A string representing the range of years for the music (e.g., '2010-2020').

    Based on these user input parameters, determine the appropriate values for the following Spotify API parameters:
    - seed_artists (comma-separated string of artists' names) provide 2 exactly artists.
    MAKE SURE TO FIT THOSE ARTISTS TO THE REQUESTED MUSIC GENRE AND THE EVENT, AS WELL AS THE AUDIENCE AGE AND YEAR RANGE.
    Moreover, make sure to fit the next parameters I will tell you in the same way.
    - min_acousticness, max_acousticness, target_acousticness (float, range: 0-1)
    - min_danceability, max_danceability, target_danceability (float, range: 0-1)
    - min_energy, max_energy, target_energy (float, range: 0-1)
    - min_instrumentalness, max_instrumentalness, target_instrumentalness (float, range: 0-1)
    - min_liveness, max_liveness, target_liveness (float, range: 0-1)
    
    The values for the Spotify API parameters should be derived based on the given user input parameters, taking into account the characteristics of the event, music genre, audience age range, and year range.
    Output the result as a JSON object and nothing else."""
    return system_prompt




# openai = OpenAIClass()
# user_input = Playlist(event="casual driving", music_genre="rock", audience_age_range="5-75", year_range="1960-2002")
# response = openai.get_chat_response_from_openai(get_system_prompt(), user_input.__str__())
# print(response)