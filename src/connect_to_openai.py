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

    def get_chat_response_from_openai(self, prompt, system_prompt, user_input):
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
    
def get_system_prompt(self):
    # Initial gpt4 suggestion, probably needs to be shortened and fine tuned... 
    system_prompt = """Given a set of user input parameters for a custom playlist creation API, translate these parameters into the corresponding input parameters required for the Spotify API's /recommendations endpoint. The user input parameters are as follows:
    - Event: A string describing the type of event (e.g., 'wedding', 'birthday party').
    - Music Genre: A string representing the music genre (e.g., 'pop', 'rock').
    - Audience Age Range: A string indicating the age range of the audience (e.g., '25-35').
    - Year Range: A string representing the range of years for the music (e.g., '2010-2020').

    Translate these user input parameters into the following Spotify API parameters:
    - limit (integer, range: 1-100)
    - market (string, ISO 3166-1 alpha-2 country code)
    - seed_artists (string, comma separated list of Spotify IDs for seed artists)
    - seed_genres (string, comma separated list of genres)
    - seed_tracks (string, comma separated list of Spotify IDs for seed tracks)
    - min_acousticness, max_acousticness, target_acousticness (number, range: 0-1)
    - min_danceability, max_danceability, target_danceability (number, range: 0-1)
    - min_energy, max_energy, target_energy (number, range: 0-1)
    - min_instrumentalness, max_instrumentalness, target_instrumentalness (number, range: 0-1)
    - min_liveness, max_liveness, target_liveness (number, range: 0-1)
    - min_loudness, max_loudness, target_loudness (number)
    - min_popularity, max_popularity, target_popularity (integer, range: 0-100)
    - min_tempo, max_tempo, target_tempo (number)
    - min_valence, max_valence, target_valence (number, range: 0-1)
    ...
    Provide a list of values for each required Spotify API parameter based on the given user input parameters."""
    return system_prompt

    
