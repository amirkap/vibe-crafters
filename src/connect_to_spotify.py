import base64
import json
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv, set_key, dotenv_values
import requests


class SpotifyAPIClass:
    def __init__(self):
        load_dotenv()
        self.client_id = os.getenv("SPOTIFY_CLIENT_ID")
        self.client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
        self.user_id = os.getenv("SPOTIFY_USER_ID")
        self.access_token = os.getenv("ACCESS_TOKEN")
        self.refresh_token = os.getenv("SPOTIFY_REFRESH_TOKEN")

        # get access token
        env_values = dotenv_values(".env")
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
        expiry_time = datetime.now() + timedelta(seconds=expires_in)
        env_path = '.env'
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
        new_token_data = self.refresh_access_token()
        self.update_env_with_new_token(new_token_data["access_token"], new_token_data["expires_in"])
        os.environ["ACCESS_TOKEN"] = new_token_data["access_token"]
        load_dotenv()
        self.access_token = os.getenv("ACCESS_TOKEN")
        print("Token updated.")

    def query_api(self, func_name, kwargs, iteration_no=0):
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

    def create_playlist_with_tracks(self, name, description, tracks_list):
        create_playlist_response = self.query_api("create_playlist", {"name": name, "description": description})
        if "error" in create_playlist_response:
            return create_playlist_response
        playlist_id = create_playlist_response["id"]
        tracks_uri_list = [track["uri"] for track in tracks_list]
        add_to_playlist_response = self.query_api("add_to_playlist", {"playlist_id": playlist_id, "songs_list": tracks_uri_list})
        if "error" in add_to_playlist_response:
            return add_to_playlist_response
        playlist_url = create_playlist_response["external_urls"]["spotify"]
        return playlist_url

 # I broke down full_request_flow() function into a call to get_recommendations() and a call to create_playlist_with_tracks() (see in logic.py)
 # I did it because of the tracks' filtering by year range.
    def full_request_flow(self, params, name, description=''):
        get_rec_response = self.query_api("get_recommendations", params)
        if "error" in get_rec_response:
            return get_rec_response

        create_playlist_response = self.query_api("create_playlist", {"name": name,
                                                      "description": description})
        if "error" in create_playlist_response:
            return create_playlist_response

        playlist_url = create_playlist_response["external_urls"]["spotify"]
        playlist_id = create_playlist_response["id"]

        add_to_playlist_response = self.query_api("add_to_playlist", {"playlist_id": playlist_id,
                                                      "songs_list": get_rec_response})
        if "error" in add_to_playlist_response:
            return add_to_playlist_response
        return playlist_url
    def get_artist_id(self, artist_name):
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

    def get_track_features(self, track_id):
        url = f"https://api.spotify.com/v1/audio-features/{track_id}"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
        }
        response = requests.get(url, headers=headers)
        return response.json()


    def get_artist(self, artist_id):
        url = f"https://api.spotify.com/v1/artists/{artist_id}"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
        }

        response = requests.get(url, headers=headers)
        return response.json()

    def callback(self):

        redirect_uri = 'http://localhost:8888/callback'

        auth_options = {
            'grant_type': 'authorization_code',
            'code': "AQAbaC_MSWKqk37cp0p2zUEctMwyX_yJX7zA-wxeArvGQxhgy86_6fUnRQ50wP-v1h_rxO5MGANhmT220mxiQ_Y-pbjEfxuGKtGI8FkCkKLAwPMmciyERZOrPyQrPuQutsospXem7QTQ5MLuV_OmB_MN0aPBxULAe2kMeKmWdVDwBii2ZHh3W_gKab-WCCc1aLz9tGHr6oxONQ",
            'redirect_uri': redirect_uri
        }

        response = requests.post('https://accounts.spotify.com/api/token', data=auth_options,
                                 headers={'Authorization': 'Basic ' + base64.urlsafe_b64encode(
                                     f'{self.client_id}:{self.client_secret}'.encode()).decode()})

        if response.status_code != 200:
            return "Failed to fetch token", response.status_code

        token_info = response.json()
        print(token_info)

        # Store the tokens and expiry time in your storage solution (e.g., session, database)

connect = SpotifyAPIClass()
# res = connect.query_api("create_playlist", {"name": "JustTOTRY",
#     "description": "New playlist description"})
# print(res)
# connect.callback()
#connect.get_artist("4Z8W4fKeB5YxbusRsdQVPb")
#add_songs = connect.query_api("add_to_playlist", {"playlist_id": "2ozSrPTu9s8HDcst9emP9n",
                                                  #"songs_list": ["spotify:track:4iVYEdYUVa79Axb7Rh","spotify:track:1301WleyT98MSxVHPZCA6M"]})2
#get_rec = connect.query_api("get_recommendations", {"seed_artists": "2U5N2KMBT6aFPrQMygMkhj"})
# add_songs = connect.query_api("add_to_playlist", {"playlist_id": "2ozSrPTu9s8HDcst9emP9n", "songs_list": get_rec})
# artists: "seed_artists": "06HL4z0CvFAxyc27GXpf02"
# full_request = connect.full_request_flow({"seed_genres": "dance", "seed_tracks": ["2WfaOiMkCvy7F5fcp2zZ8L", "0Q6mJSyGsUmg9WXgOcOf7A"], "limit": 100},
#                                          "80s Dance", "New playlist description")
# print(full_request)

#get_track_id = connect.query_api("get_track_id", {"track_name": "The Less I Know The Better"})

# for_rec = {
#     "seed_artists": "06HL4z0CvFAxyc27GXpf02,0du5cEVh5yTK9QJze8zA0C",
#     "seed_tracks": "0VjIjW4GlUZAMYd2vXMi3b,3PfIrDoz19wz7qK7tYeu62",
#     "min_acousticness": 0.2,
#     "max_acousticness": 0.6,
#     "min_danceability": 0.6,
#     "max_danceability": 0.8,
#     "min_energy": 0.6,
#     "max_energy": 0.8,
#     # "min_instrumentalness": 0.1,
#     "max_instrumentalness": 0.4,
#     "min_liveness": 0.1,
#     "max_liveness": 0.7,
#     "seed_genres": "pop",
#     "limit": 100,
#     "market": "US"
# }
# get_rec = connect.query_api("get_recommendations", for_rec)
# print(len(get_rec))