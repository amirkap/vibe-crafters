import pandas as pd
import numpy as np
import ast
from src.services.connect_to_openai import OpenAIClass, get_assemsment_sys_promompt, get_assesment_user_prompt
from src.services.connect_to_spotify import SpotifyAPIClass

FILENAME = 'songs_dataset/streamlit.csv'
NUM_EXPERIMENTS = 10
audio_features = ['danceability', 'energy', 'loudness', 'speechiness', 'acousticness',
                  'instrumentalness', 'liveness', 'valence', 'tempo']

# Set display options
pd.set_option('display.max_rows', 30)  # Set the maximum number of rows to display
pd.set_option('display.max_columns', 20)  # Set the maximum number of columns to display
pd.set_option('display.width', 100)  # Set the width of the display in characters

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
    print(f"features_df before resetting index: {features_df}")
    shared_columns = [col for col in features_df.columns if col in streamlit_df.columns]
    print(f"Shared columns before resetting index: {shared_columns}")
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
        diffs[col + '_diff'] = np.mean(merged_df[col + '_predicted'] - merged_df[col + '_true'])

    return diffs


def calculate_audio_features_for_median():
    # Example usage
    streamlit_df = read_csv_file(FILENAME)  # Read the entire CSV file
    spotify = SpotifyAPIClass()

    num_rows = 150  # Number of random track IDs to extract
    uri_df = read_random_track_uris(streamlit_df, num_rows)
    #print(uri_df)
    names_list = {track_uri: spotify.get_track_and_artist_name(track_uri) for track_uri in uri_df['track_uri']}
    #print(names_list)

    track_info_df = pd.DataFrame.from_dict(names_list, orient='index')
    track_info_df.reset_index(inplace=True)
    track_info_df.rename(columns={'index': 'track_uri'}, inplace=True)

    true_features = streamlit_df[streamlit_df['track_uri'].isin(uri_df['track_uri'])]
    full_df_with_names = pd.merge(track_info_df, true_features, on='track_uri')

    # Concatenate the song name and artist name into a single column
    full_df_with_names['name_and_artist'] = full_df_with_names['track_name'] + ' - ' + full_df_with_names['artist_name']

    # Resulting DataFrame
    print(full_df_with_names)

    # create a dictionary for holding the predicted audio features
    predicted_audio_features = []
    true_audio_features = []

    batch_size = 15
    for i in range(0, len(full_df_with_names), batch_size):
        current_batch = full_df_with_names[i:i + batch_size]['name_and_artist'].tolist()
        current_batch_uris = full_df_with_names[i:i + batch_size]['track_uri'].tolist()
        openai = OpenAIClass()
        print("#################### OPENAI RESPONSE ####################")
        response = openai.get_chat_response_from_openai(get_assemsment_sys_promompt(),
                                                        get_assesment_user_prompt(current_batch))
        print(response)
        audio_features_list = ast.literal_eval(response)
        predicted_audio_features.extend(audio_features_list)

    features_df = pd.DataFrame(predicted_audio_features)
    featurs_df_with_uris = pd.concat([full_df_with_names['track_uri'], features_df], axis=1)
    print(f"featurs_df_with_uris before resetting index:", featurs_df_with_uris)
    shared_columns = [col for col in featurs_df_with_uris.columns if col in full_df_with_names.columns]
    print(f"Shared columns before resetting index", shared_columns)
    featurs_df_with_uris = featurs_df_with_uris[shared_columns]
    true_values_with_names = full_df_with_names[shared_columns]
    true_values_with_names = true_values_with_names.reset_index(drop=True)
    featurs_df_with_uris = featurs_df_with_uris.reset_index(drop=True)
    df_true_and_predict = pd.merge(featurs_df_with_uris, true_values_with_names, on='track_uri', suffixes=('_predicted', '_true'))
    print(f"df_true_and_predict after merging:")
    print(df_true_and_predict)

    diffs = {}
    for col in audio_features:
        if col + '_predicted' not in df_true_and_predict.columns or col + '_true' not in df_true_and_predict.columns:
            continue
        diffs[col + '_diff'] = np.median(df_true_and_predict[col + '_true'] - df_true_and_predict[col + '_predicted'])

    print(diffs)
    return diffs


        #features_df = pd.DataFrame(audio_features_list)
#
#
#
# totals = {feature + '_diff': 0 for feature in audio_features}
# for i in range(NUM_EXPERIMENTS):
#     print(f"###################### Experiment {i + 1} #######################")
#     avg_diffs = experiment()
#     filtered_avg_diffs = {feature_diff: avg_diffs[feature_diff] for feature_diff in totals.keys()}
#     print(f"Experiment {i + 1} average differences: {filtered_avg_diffs}")
#     for feature in totals:
#         totals[feature] += filtered_avg_diffs[feature]
#     print("\n\n\n")
#
# print(f"###################### AVERAGE DIFFERENCES #######################")
# print({feature: totals[feature] / NUM_EXPERIMENTS for feature in totals})

# print("#################### SPOTIFY API ####################")
# print([spotify.get_track_features(track_uri) for track_uri in uris_list])

calculate_audio_features_for_median()
