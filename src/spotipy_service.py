import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import pprint
from dotenv import load_dotenv

load_dotenv()
client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")
print(client_id, client_secret)


class Spotipy:
    def __init__(self):
        scope = "playlist-modify-public"
        auth_manager = SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri,
                                    scope=scope)
        self.sp = spotipy.Spotify(auth_manager=auth_manager)

    def add_tracks_to_playlist(self, playlist_id, track_ids):
        self.sp.playlist_add_items(playlist_id, track_ids)

    def create_playlist(self, playlist_name, description):
        user_id = self.sp.me()["id"]
        playlist = self.sp.user_playlist_create(user_id, playlist_name, public=True, description=description)
        playlist_url = playlist["external_urls"]["spotify"]
        return playlist_url

    def create_playlist_with_tracks(self, playlist_name, description, track_ids):
        playlist_url = self.create_playlist(playlist_name, description)
        playlist_id = playlist_url.split("/")[-1]
        self.add_tracks_to_playlist(playlist_id, track_ids)
        return playlist_url

    def get_recommendations(self, seed_artists, seed_tracks, seed_genres, limit, country):
        recommendations = self.sp.recommendations(seed_artists=seed_artists, seed_genres=seed_genres,
                                                  seed_tracks=seed_tracks,
                                                  limit=limit, country=country)
        recommended_tracks = [track["id"] for track in recommendations["tracks"]]
        return recommended_tracks

    def get_track(self, track_id):
        track_info = {
            "track_name": self.sp.track(track_id)["name"],
            "track_id": track_id,
            "track_artists": [artist["name"] for artist in self.sp.track(track_id)["artists"]],
            "track_album": self.sp.track(track_id)["album"]["name"],
            "track_release_year": self.sp.track(track_id)["album"]["release_date"][:4],
            "track_popularity": self.sp.track(track_id)["popularity"],
        }
        return track_info

    def get_artist(self, artist_id):
        artist_info = {
            "artist_name": self.sp.artist(artist_id)["name"],
            "artist_id": artist_id,
            "artist_popularity": self.sp.artist(artist_id)["popularity"],
            "artist_genres": self.sp.artist(artist_id)["genres"]
        }
        return artist_info

    def get_track_id(self, track_name):
        track_id = self.sp.search(track_name, type="track")["tracks"]["items"][0]["id"]
        return track_id

    def get_artist_id(self, artist_name):
        artist_id = self.sp.search(artist_name, type="artist")["artists"]["items"][0]["id"]
        return artist_id

    def get_album(self, album_id):
        return self.sp.album(album_id)

    def get_playlist(self, playlist_id):
        return self.sp.playlist(playlist_id)

    def get_audio_features(self, track_id):
        return self.sp.audio_features(track_id)

    def get_audio_analysis(self, track_id):
        return self.sp.audio_analysis(track_id)

    def get_available_genre_seeds(self):
        return self.sp.recommendation_genre_seeds()


spotify = Spotipy()
# print(spotify.sp.current_user())
# available_genres = spotify.get_available_genre_seeds()
# pprint.pprint(available_genres)
pprint.pprint(spotify.get_track("6K4t31amVTZDgR3sKmwUJJ"))  # The less I know the better
pprint.pprint(spotify.get_artist("2lxX1ivRYp26soIavdG9bX"))  # Yardbirds
# print(spotify.get_track_id("The less I know the better"))
# print(spotify.get_artist_id("Yardbirds"))
recommended_songs = spotify.get_recommendations(seed_artists=["2lxX1ivRYp26soIavdG9bX"],
                                                 seed_tracks=["6K4t31amVTZDgR3sKmwUJJ"], seed_genres=["indie"],
                                                 limit=30, country="US")
pprint.pprint(recommended_songs)
new_playlist = spotify.create_playlist_with_tracks("Test playlist", "This is a test playlist", recommended_tracks)
print(new_playlist)
