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

        # get access token
        env_values = dotenv_values(".env")
        current_time = datetime.now()

        # Check if token expiry exists and has passed
        if "TOKEN_EXPIRY" in env_values:
            token_expiry = datetime.strptime(env_values["TOKEN_EXPIRY"], "%Y-%m-%d %H:%M:%S")
            if current_time >= token_expiry:
                # Token has expired, request a new one
                self.get_access_token_and_update_env()
                load_dotenv()
            else:
                print("Existing token is still valid.")
        else:
            # No token expiry set, fetch a new token
            self.get_access_token_and_update_env()
            load_dotenv()

        self.access_token = os.getenv("ACCESS_TOKEN")


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

    def update_env_with_new_token(self, access_token, expires_in):
        expiry_time = datetime.now() + timedelta(seconds=expires_in)
        env_path = '.env'
        set_key(env_path, "ACCESS_TOKEN", access_token)
        set_key(env_path, "TOKEN_EXPIRY", expiry_time.strftime("%Y-%m-%d %H:%M:%S"))

    def get_access_token_and_update_env(self):
        new_token_data = self.get_access_token()
        self.update_env_with_new_token(new_token_data["access_token"], new_token_data["expires_in"])
        print("Token updated.")

    def create_playlist(self, name, description=''):
        response = self.client.user_playlist_create(self.user_id, name, public=True, collaborative=False, description=description)
        print(response)

    def get_artist(self, artist_id):
        url = "https://api.spotify.com/v1/artists/4Z8W4fKeB5YxbusRsdQVPb"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
        }

        response = requests.get(url, headers=headers)

        # To print the whole response content
        print(response.json())

connect = SpotifyAPIClass()
connect.get_artist("4Z8W4fKeB5YxbusRsdQVPb")