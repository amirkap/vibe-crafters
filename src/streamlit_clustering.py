import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import ast

audio_features = ['danceability', 'energy', 'loudness', 'speechiness', 'acousticness',
                  'instrumentalness', 'liveness', 'valence', 'tempo']

# Set display options
pd.set_option('display.max_rows', 30)  # Set the maximum number of rows to display
pd.set_option('display.max_columns', 20)  # Set the maximum number of columns to display
pd.set_option('display.width', 100)  # Set the width of the display in characters

# Load the data
df = pd.read_csv('streamlit.csv')

# Specify the columns you want to use for clustering
columns_for_clustering = audio_features

# Extract the specified columns and track_uri
data = df[columns_for_clustering]
track_uri = df['track_uri']

# Scale the data
scaler = StandardScaler()
data_scaled = scaler.fit_transform(data)

# Apply K-Means
num_clusters = 10  # Adjust this based on your needs
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
kmeans.fit(data_scaled)

# Assign labels (add the number of the cluster to the original DataFrame)
df['cluster'] = kmeans.labels_

# Check the result
# print(df.head())


# Split the 'Artist_genres' column into separate genres
df['Artist_genres'] = df['Artist_genres'].str.split()

# Initialize a dictionary to store statistics for each cluster
cluster_stats = {}

for cluster_num in range(num_clusters):
    cluster_df = df[df['cluster'] == cluster_num]
    print(f"Cluster {cluster_num} contains:")
    print(cluster_df[['track_uri', 'artist_uri', 'Artist_genres', 'cluster']])

    # Explode the 'Artist_genres' column to count tracks in each artist genre
    exploded_df = cluster_df.explode('Artist_genres')
    genre_counts = exploded_df['Artist_genres'].value_counts()

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

