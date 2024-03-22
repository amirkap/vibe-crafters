import pandas as pd
import os
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors

audio_features = ['danceability', 'energy', 'loudness', 'speechiness', 'acousticness',
                  'instrumentalness', 'liveness', 'valence', 'tempo']

# Get the directory where dataset_manipulation.py is located
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the streamlit.csv file
DATASET_NAME = os.path.join(current_dir, "streamlit.csv.gz")

def init_data_frame():
    """
    Reads the compressed CSV file and returns a pandas DataFrame.

    Returns:
        A pandas DataFrame containing the data from the compressed CSV file.
    """
    # Read the compressed CSV file
    data_frame = pd.read_csv(DATASET_NAME, compression='gzip')
    return data_frame

def find_nearest_neighbors(data_frame, instance, n_neighbors=5):
    """
    Finds the nearest neighbors to a given instance within a DataFrame.

    Parameters:
    - data_frame: A pandas DataFrame containing the data points.
    - instance: An array or list containing the feature values of the instance.
    - n_neighbors: The number of nearest neighbors to find.

    Returns:
    - indices of the n_neighbors closest points in the data_frame.
    """

    # Ensure the instance is reshaped correctly if it's a 1D array (to match feature number)
    if len(instance.shape) == 1:
        instance = instance.reshape(1, -1)

    # Extract features from the DataFrame and the instance
    data = data_frame[audio_features]
    instance = pd.DataFrame(instance, columns=audio_features)

    # Scale the features (both from the DataFrame and the instance)
    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(data)
    instance_scaled = scaler.transform(instance)

    # Initialize and fit the NearestNeighbors model
    nn_model = NearestNeighbors(n_neighbors=n_neighbors)
    nn_model.fit(data_scaled)

    # Find the nearest neighbors to the instance
    distances, indices = nn_model.kneighbors(instance_scaled)

    return data_frame.iloc[indices[0]]

def contains_genre(genres_str, target_genre):
    """
    Checks if a given string of genres contains a specific genre.

    Parameters:
    - genres_str: A string containing a list of genres separated by commas.
    - target_genre: A string representing the genre to search for.

    Returns:
    - A boolean indicating whether the target_genre is in the genres_str.
    """
    # Split the genre_list into an array of genres
    genres_list = genres_str.split()
    # Check if target_genre is in the array
    return target_genre.lower() in genres_list

def find_nearest_neighbors_by_genre(instance, filter_genre, n_neighbors=5):
    """
    Finds the nearest neighbors to a given instance within a DataFrame that match a specific genre.

    Parameters:
    - data_frame: A pandas DataFrame containing the data points.
    - instance: An array or list containing the feature values of the instance.
    - genre: A string representing the genre to filter by.
    - n_neighbors: The number of nearest neighbors to find.

    Returns:
    - A DataFrame of the n_neighbors closest points in the data_frame that match the genre.
    """

    data_frame = init_data_frame()

    # Filter the DataFrame for rows where 'Artist_genres' contains the specified genre
    filtered_df = data_frame[data_frame['Artist_genres'].apply(lambda x: contains_genre(x, filter_genre))]

    if filtered_df.empty:
        return []

    instance = pd.DataFrame([instance], index=[0])
    instance_features = list(instance.columns)
    # Extract features from the filtered DataFrame
    data = filtered_df[instance_features]

    # Scale the features (both from the DataFrame and the instance)
    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(data)
    instance_scaled = scaler.transform(instance)

    # Initialize and fit the NearestNeighbors model
    nn_model = NearestNeighbors(n_neighbors=n_neighbors)
    nn_model.fit(data_scaled)

    # Find the nearest neighbors to the instance
    distances, indices = nn_model.kneighbors(instance_scaled)

    # Return the filtered DataFrame rows corresponding to the nearest neighbors
    return filtered_df.iloc[indices[0]]['track_uri'].tolist()