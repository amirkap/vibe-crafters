import base64
import json
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv, set_key, dotenv_values
import requests


class SpotifyAPIClass:
    """
    A class to represent the Spotify API and its functionalities.
    """
    def __init__(self):
        load_dotenv()
        self.client_id = os.getenv("SPOTIFY_CLIENT_ID")
        self.client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
        self.user_id = os.getenv("SPOTIFY_USER_ID")
        self.access_token = os.getenv("ACCESS_TOKEN")
        self.refresh_token = os.getenv("SPOTIFY_REFRESH_TOKEN")

        # get access token
        env_values = dotenv_values("../.env")
        current_time = datetime.now()

        # Check if token expiry exists and has passed
        if "TOKEN_EXPIRY" in env_values:
            token_expiry = datetime.strptime(env_values["TOKEN_EXPIRY"], "%Y-%m-%d %H:%M:%S")
            if current_time >= token_expiry:
                # Token has expired, request a new one
                self.refresh_token_and_update_env()
            else:
                print("Existing token is still valid.")
        else:
            # No token expiry set, fetch a new token
            self.refresh_token_and_update_env()


    def get_access_token(self):
        """
        Fetches a new access token from the Spotify API.
        Returns:
            A dictionary containing the access token and its expiry time.
        """
        url = "https://accounts.spotify.com/api/token"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }

        response = requests.post(url, headers=headers, data=data)

        return response.json()

    def update_env_with_new_token(self, access_token, expires_in, refresh_token=None):
        """
        Updates the .env file with the new access token and its expiry time.
        Args:
            access_token: The new access token.
            expires_in: The time in seconds until the token expires.
            refresh_token: The new refresh token.

        Returns:

        """
        expiry_time = datetime.now() + timedelta(seconds=expires_in)
        env_path = '../.env'
        set_key(env_path, "ACCESS_TOKEN", access_token)
        set_key(env_path, "TOKEN_EXPIRY", expiry_time.strftime("%Y-%m-%d %H:%M:%S"))
        if refresh_token:
            set_key(env_path, "SPOTIFY_REFRESH_TOKEN", refresh_token)

    def get_access_token_and_update_env(self):
        new_token_data = self.get_access_token()
        self.update_env_with_new_token(new_token_data["access_token"], new_token_data["expires_in"])
        os.environ["ACCESS_TOKEN"] = new_token_data["access_token"]
        load_dotenv()
        self.access_token = os.getenv("ACCESS_TOKEN")
        print("Token updated.")

    def refresh_access_token(self):
        """
        Refreshes the access token using the refresh token.
        Returns:
            A dictionary containing the new access token and its expiry time.
        """
        url = "https://accounts.spotify.com/api/token"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            'Authorization': 'Basic ' + base64.urlsafe_b64encode(
                f'{self.client_id}:{self.client_secret}'.encode()).decode(),
        }
        data = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
            "client_id": self.client_id,
        }

        response = requests.post(url, headers=headers, data=data)
        print("This is the response", response.json())
        return response.json()

    def refresh_token_and_update_env(self):
        """
        Refreshes the access token and updates the .env file with the new token and its expiry time.
        """
        new_token_data = self.refresh_access_token()
        self.update_env_with_new_token(new_token_data["access_token"], new_token_data["expires_in"])
        os.environ["ACCESS_TOKEN"] = new_token_data["access_token"]
        load_dotenv()
        self.access_token = os.getenv("ACCESS_TOKEN")
        print("Token updated.")

    def query_api(self, func_name, kwargs, iteration_no=0):
        """
        Queries the Spotify API using the specified function name and keyword arguments.
        Args:
            func_name: The name of the function to call.
            kwargs: The keyword arguments to pass to the function.
            iteration_no: The number of times to retry in the case of an error.

        Returns:
            The response from the API.
        """
        try:
            method = getattr(self, func_name)
            response = method(**kwargs)
            if func_name == "get_recommendations" and "error" not in response:
                only_tracks = [track["uri"] for track in response]
                print(f"Response of '{func_name}()': {only_tracks}")
            else:
                print(f"Response of '{func_name}()': {response}")
            if "error" in response:
                if response["error"]["status"] == 401 and iteration_no < 2:
                    if response["error"]["message"] in ["The access token expired", "Invalid access token"]:
                        self.refresh_token_and_update_env()
                        return self.query_api(func_name, kwargs, iteration_no + 1)
                return {"error": response["error"]["status"], "message": response["error"]["message"]}
            return response
        except Exception as e:
            # add to logger
            print(e)
            return {"error": 500, "message": "Internal server error"}

    def create_playlist(self, name, description=''):
        """
        Creates a new playlist for the current user.
        Args:
            name: The name of the playlist.
            description: The description of the playlist.

        Returns:
            A dictionary containing the response from the API.
        """
        url = f"https://api.spotify.com/v1/users/{self.user_id}/playlists"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        data = {
            "name": name,
            "description": description
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))
        return response.json()

    def add_to_playlist(self, playlist_id, songs_list):
        """
        Adds a list of songs to the specified playlist.
        Args:
            playlist_id: The ID of the playlist to add the songs to.
            songs_list: A list of Spotify URIs for the songs to add.

        Returns:
            A dictionary containing the response from the API.
        """
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        data = {
            "uris": songs_list,
            "position": 0
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))
        return response.json()

    def get_recommendations(self, **kwargs):
        """
        Gets a list of recommended tracks based on the specified parameters.
        Args:
            **kwargs: The parameters to pass to the API.

        Returns:
            A list of recommended tracks.
        """
        url = "https://api.spotify.com/v1/recommendations"
        headers = {
            "Authorization": f"Bearer {self.access_token}"}

        params = {k: v for k, v in kwargs.items() if v is not None}
        seeds_values_count = sum(len(v.split(',')) for k, v in params.items() if "seed" in k)

        if "seed_artists" or "seed_genres" or "seed_tracks" in params and seeds_values_count <= 5:
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                # tracks_list = [track["uri"] for track in response.json()["tracks"]]
                # return tracks_list
                tracks = response.json()["tracks"]
                return tracks
            return response.json()

        return {"error": 400, "message": "At least one of seed_artists, seed_genres, or seed_tracks is required, at most five can be provided."}

    def create_playlist_with_tracks(self, name, description, tracks_list, neighbor_tracks_list=None):
        """
        Creates a new playlist and adds the specified tracks to it.
        Args:
            name: The name of the playlist.
            description: The description of the playlist.
            tracks_list: A list of tracks to add to the playlist.
            neighbor_tracks_list: A list of tracks to add to the playlist, found by knn.

        Returns:
            The URL of the created playlist.
        """
        if len(tracks_list) == 0 and (not neighbor_tracks_list or len(neighbor_tracks_list) == 0):
            return {"error": 400, "message": "We were unable to find tracks matching, try again."}

        create_playlist_response = self.query_api("create_playlist", {"name": name, "description": description})
        if "error" in create_playlist_response:
            return create_playlist_response
        playlist_id = create_playlist_response["id"]
        tracks_uri_list = [track["uri"] for track in tracks_list]

        if len(tracks_uri_list) > 89:
            tracks_uri_list = tracks_uri_list[:88]

        if neighbor_tracks_list:
            tracks_uri_list.extend(["spotify:track:" + track for track in neighbor_tracks_list])

        add_to_playlist_response = self.query_api("add_to_playlist", {"playlist_id": playlist_id, "songs_list": tracks_uri_list})
        if "error" in add_to_playlist_response:
            return add_to_playlist_response
        playlist_url = create_playlist_response["external_urls"]["spotify"]
        return playlist_url

    def get_artist_id(self, artist_name):
        """
        Gets the ID of the specified artist.
        Args:
            artist_name: The name of the artist to get the ID for.

        Returns:
            The ID of the artist.
        """
        search_url = "https://api.spotify.com/v1/search"
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }
        params = {
            'q': artist_name,
            'type': 'artist',
            'limit': 1  # Assuming you want the top result
        }
        search_response = requests.get(search_url, headers=headers, params=params)
        search_results = search_response.json()

        # Step 3: Extract the Artist ID
        if search_results['artists']['items']:
            artist_id = search_results['artists']['items'][0]['id']
            return artist_id
        else:
            return None

    def get_track_id(self, track_name):
        """
        Gets the ID of the specified track.
        Args:
            track_name: The name of the track to get the ID for.

        Returns:
            The ID of the track.
        """
        search_url = "https://api.spotify.com/v1/search"
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }
        params = {
            'q': track_name,
            'type': 'track',
            'limit': 1
        }
        search_response = requests.get(search_url, headers=headers, params=params)
        search_results = search_response.json()

        if search_results['tracks']['items']:
            track_id = search_results['tracks']['items'][0]['id']
            return track_id
        else:
            return None

    def get_track_and_artist_name(self, track_id):
        """
        Gets the name of the track and its artist.
        Args:
            track_id: The ID of the track to get the name and artist for.

        Returns:
            A dictionary containing the track name and artist name.
        """
        url = f"https://api.spotify.com/v1/tracks/{track_id}"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
        }

        response = requests.get(url, headers=headers)
        track_info = response.json()
        artist_name = track_info["artists"][0]["name"]
        track_name = track_info["name"]
        return {"track_name": track_name, "artist_name": artist_name}

    def get_track_features(self, track_id):
        """
        Gets the audio features for the specified track.
        Args:
            track_id: The ID of the track to get the audio features for.

        Returns:
            A dictionary containing the response from the API.
        """
        url = f"https://api.spotify.com/v1/audio-features/{track_id}"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
        }
        response = requests.get(url, headers=headers)
        return response.json()

    def get_track(self, track_id):
        """
        Gets the information for the specified track.
        Args:
            track_id: The ID of the track to get the information for.

        Returns:
            A dictionary containing the response from the API.
        """
        url = f"https://api.spotify.com/v1/tracks/{track_id}"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
        }
        response = requests.get(url, headers=headers)
        return response.json()

    def get_multiple_tracks_info(self, track_ids):
        """
        Gets the information for the specified tracks.
        Args:
            track_ids: A list of track IDs to get the information for.

        Returns:
            A dictionary containing the response from the API.
        """
        track_ids_str = ",".join(track_ids)
        url = f"https://api.spotify.com/v1/tracks?ids={track_ids_str}"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
        }
        response = requests.get(url, headers=headers)
        return response.json()


    def get_artist(self, artist_id):
        """
        Gets the information for the specified artist.
        Args:
            artist_id: The ID of the artist to get the information for.

        Returns:
            A dictionary containing the response from the API.
        """
        url = f"https://api.spotify.com/v1/artists/{artist_id}"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
        }

        response = requests.get(url, headers=headers)
        return response.json()

    def search_item(self, item_type, query, limit=10):
        """
        Searches for items on Spotify based on the specified query and type.
        Args:
            item_type: The type of item to search for (e.g., 'track', 'artist', 'album').
            query: The search query.
            limit: The maximum number of items to return.

        Returns:
            A dictionary containing the response from the API.
        """
        url = "https://api.spotify.com/v1/search"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
        }
        params = {
            'q': query,
            'type': item_type,
            'limit': limit,
            'market': 'US'
        }

        response = requests.get(url, headers=headers, params=params)
        return response.json()

    def get_playlist_songs(self, playlist_id):
        """
        Gets the songs in the specified playlist.
        Args:
            playlist_id: The ID of the playlist to get the songs from.

        Returns:
            A dictionary containing the response from the API.
        """
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
        }

        response = requests.get(url, headers=headers)
        return response.json()