import pandas as pd
import numpy as np
import ast
from connect_to_openai import OpenAIClass, get_assemsment_sys_promompt, get_assesment_user_prompt
from connect_to_spotify import SpotifyAPIClass

FILENAME = 'streamlit.csv'
NUM_EXPERIMENTS = 3
audio_features = ['danceability', 'energy', 'loudness', 'speechiness', 'acousticness',
                  'instrumentalness', 'liveness', 'valence', 'tempo']


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


def experiment():
    # Example usage
    streamlit_df = read_csv_file(FILENAME)  # Read the entire CSV file
    spotify = SpotifyAPIClass()

    # Sample 10,000 random track URIs
    num_rows = 15  # Number of random track IDs to extract
    uri_df = read_random_track_uris(streamlit_df, num_rows)
    print(uri_df)
    names_list = [spotify.get_track_and_artist_name(track_uri) for track_uri in uri_df['track_uri']]
    print(names_list)

    # Set up OpenAI API
    openai = OpenAIClass()
    print("#################### OPENAI RESPONSE ####################")
    response = openai.get_chat_response_from_openai(get_assemsment_sys_promompt(),
                                                    get_assesment_user_prompt(names_list))
    print(response)
    audio_features_list = ast.literal_eval(response)
    features_df = pd.DataFrame(audio_features_list)
    shared_columns = [col for col in features_df.columns if col in streamlit_df.columns]
    print(f"Shared columns: {shared_columns}")
    features_df = features_df[shared_columns]
    uri_df = uri_df.reset_index(drop=True)
    features_df = features_df.reset_index(drop=True)
    features_df = pd.concat([uri_df, features_df], axis=1)
    print(f"Predicted features:\n{features_df}")
    true_features_df = streamlit_df[streamlit_df['track_uri'].isin(uri_df['track_uri'])]
    true_features_df = true_features_df[shared_columns + ['track_uri']]
    print(f"True features:\n{true_features_df}")
    merged_df = pd.merge(features_df, true_features_df, on='track_uri', suffixes=('_predicted', '_true'))

    diffs = {}
    for col in shared_columns:
        diffs[col + '_diff'] = np.mean(abs(merged_df[col + '_predicted'] - merged_df[col + '_true']))

    return diffs


totals = {feature + '_diff': 0 for feature in audio_features}
for i in range(NUM_EXPERIMENTS):
    print(f"###################### Experiment {i + 1} #######################")
    avg_diffs = experiment()
    filtered_avg_diffs = {feature_diff: avg_diffs[feature_diff] for feature_diff in totals.keys()}
    print(f"Experiment {i + 1} average differences: {filtered_avg_diffs}")
    for feature in totals:
        totals[feature] += filtered_avg_diffs[feature]
    print("\n\n\n")

print(f"###################### AVERAGE DIFFERENCES #######################")
print({feature: totals[feature] / NUM_EXPERIMENTS for feature in totals})

# print("#################### SPOTIFY API ####################")
# print([spotify.get_track_features(track_uri) for track_uri in uris_list])
