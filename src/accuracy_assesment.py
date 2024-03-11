import pandas as pd
import numpy as np
from connect_to_openai import OpenAIClass, get_assemsment_sys_promompt, get_assesment_user_prompt
from connect_to_spotify import SpotifyAPIClass
FILENAME = 'streamlit.csv'


def read_csv_file(filename):
    df = pd.read_csv(filename)
    return df


def read_random_track_uris(df, num_rows):
    # Extract the 'track_uri' column
    track_uris = df['track_uri']

    # Drop duplicates to get unique track URIs
    unique_track_uris = track_uris.drop_duplicates()

    # Use min to ensure num_rows does not exceed the number of unique track URIs
    num_rows = min(num_rows, len(unique_track_uris))

    # Sample the specified number of random track URIs
    sampled_track_uris = unique_track_uris.sample(n=num_rows)

    # Return the sampled track URIs as a DataFrame
    return pd.DataFrame({'track_uri': sampled_track_uris})


# Example usage

streamlit_df = read_csv_file(FILENAME)  # Read the entire CSV file

# Sample 10,000 random track URIs
num_rows = 20 # Number of random track IDs to extract
sampled_df = read_random_track_uris(streamlit_df, num_rows)
print(sampled_df)
# uris_list = sampled_df['track_uri'].tolist()
# print(uris_list)

# Set up OpenAI API
openai = OpenAIClass()
print("#################### OPENAI RESPONSE ####################")
response = openai.get_chat_response_from_openai(get_assemsment_sys_promompt(), get_assesment_user_prompt(sampled_df))
print(response)

# spotify = SpotifyAPIClass()
# print("#################### SPOTIFY API ####################")
# print([spotify.get_track_features(track_uri) for track_uri in uris_list])
