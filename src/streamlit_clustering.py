import pandas as pd
import os
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors

audio_features = ['danceability', 'energy', 'loudness', 'speechiness', 'acousticness',
                  'instrumentalness', 'liveness', 'valence', 'tempo']

# Get the directory where streamlit_clustering.py is located
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the streamlit.csv file
DATASET_NAME = os.path.join(current_dir, "streamlit.csv")

def init_data_frame():
    # Read the CSV file
    data_frame = pd.read_csv(DATASET_NAME)
    return data_frame

def create_clusters(data_frame, num_clusters=10):
    # Specify the columns you want to use for clustering
    columns_for_clustering = audio_features

    # Extract the specified columns and track_uri
    data = data_frame[columns_for_clustering]
    track_uri = data_frame['track_uri']

    # Scale the data
    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(data)

    # Apply K-Means
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    kmeans.fit(data_scaled)

    # Assign labels (add the number of the cluster to the original DataFrame)
    data_frame['cluster'] = kmeans.labels_

def print_cluster_stats(data_frame, num_of_clusters):
    cluster_stats = {}

    # Split the 'Artist_genres' column into separate genres
    data_frame['Artist_genres'] = data_frame['Artist_genres'].str.split()

    for cluster_num in range(num_of_clusters):
        cluster_df = data_frame[data_frame['cluster'] == cluster_num]
        print(f"Cluster {cluster_num} contains:")
        print(cluster_df[['track_uri', 'artist_uri', 'Artist_genres', 'cluster']])

        # Explode the 'Artist_genres' column to count tracks in each artist genre
        exploded_df = cluster_df.explode('Artist_genres')
        genre_counts = exploded_df['Artist_genres'].value_counts().head(20)

        # Count unique artists
        unique_artists = cluster_df['artist_uri'].nunique()

        # Store the statistics in the dictionary
        cluster_stats[cluster_num] = {
            'genre_counts': genre_counts,
            'unique_artists': unique_artists
        }
        print(f'Cluster {cluster_num} statistics:')
        print(cluster_stats[cluster_num])
        print()


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

def extract_artist_genres(data_frame):
    pop_genres_list = data_frame['Artist_genres'].apply(lambda x: [genre for genre in x.split() if genre == 'pop']).tolist()
    general_genres_list = data_frame['Artist_genres'].apply(lambda x: x.split()).tolist()

    # Flatten the list of lists if necessary
    flat_pop_genres_list = {genre for sublist in pop_genres_list for genre in sublist}
    flat_general_genres_list = {genre for sublist in general_genres_list for genre in sublist}

    #print(flat_pop_genres_list)
    print(flat_pop_genres_list)

instance = {'valence': 0.751, 'danceability': 0.709, 'energy': 0.752}
print(find_nearest_neighbors_by_genre(instance, "dance", 5))