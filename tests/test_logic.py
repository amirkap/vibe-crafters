import unittest
from unittest.mock import patch, MagicMock, ANY

import pytest

from mock_responses import *
from src.logic.logic import (
    find_seed_tracks_by_playlist_id,
    find_seed_artists_by_playlist_id,
    filter_tracks_by_decade,
    translate_artist_names,
    translate_track_names,
    SpotifyAPIClass,
    Playlist,
    convert_to_spotify_params_and_create_playlist,
    get_new_seed_tracks_names,
    find_min_num_of_tracks_with_spotify_seeds,
    find_min_num_of_tracks_with_gpt_seeds,
    find_seed_tracks_and_artists_from_spotify,
    get_most_popular_artists,
    get_most_popular_tracks
)


class TestLogic(unittest.TestCase):

    @patch('src.services.connect_to_spotify.SpotifyAPIClass')
    def test_get_most_popular_tracks(self, mock_spotify_class):
        # Create a mock SpotifyAPI instance with hardcoded responses
        mock_spotify_instance = mock_spotify_class.return_value

        # Hardcoded response for 'get_playlist_songs' API call
        playlist_songs_response = {
            "items": [{"track": {"id": f"track{i}"}} for i in range(1, 11)]
        }

        # Hardcoded response for 'get_multiple_tracks' API call
        multiple_tracks_response = {
            "tracks": [
                {"id": "track1", "popularity": 10},
                {"id": "track2", "popularity": 20},
                {"id": "track3", "popularity": 30},
                {"id": "track4", "popularity": 40},
                {"id": "track5", "popularity": 50},
                {"id": "track6", "popularity": 60},
                {"id": "track7", "popularity": 70},
                {"id": "track8", "popularity": 80},
                {"id": "track9", "popularity": 90},
                {"id": "track10", "popularity": 100},
            ]
        }

        # Setup the side_effect to return these hardcoded responses
        def side_effect_query_api(method, params):
            if method == "get_playlist_songs":
                return playlist_songs_response
            elif method == "get_multiple_tracks":
                return multiple_tracks_response
            else:
                return None

        mock_spotify_instance.query_api.side_effect = side_effect_query_api

        result = get_most_popular_tracks("some_playlist_id", mock_spotify_instance, num_attempts=1)

        # The expected result string, assuming your function sorts by popularity and joins the top 6 track IDs
        expected_result = "track10,track9,track8,track7,track6,track5"
        self.assertEqual(expected_result, result)


    # tests for filtering tracks by decade
    def setUpDecadeYears(self):
        # Hardcoded decade years for testing
        self.decade_years = {
            '1980s': {'start_year': 1980, 'end_year': 1989},
            '1990s': {'start_year': 1990, 'end_year': 1999},
            '2000s': {'start_year': 2000, 'end_year': 2009},
        }
        self.recommended_tracks = [
            {"album": {"release_date": "1985-06-17"}, "name": "Track 1"},
            {"album": {"release_date": "1992-04-20"}, "name": "Track 2"},
            {"album": {"release_date": "1979-12-03"}, "name": "Track 3"}
        ]

    @patch('src.logic.logic.get_decades_start_and_end_years')
    def test_filter_tracks_1980s(self, mock_get_decades):
        self.setUpDecadeYears()
        mock_get_decades.return_value = self.decade_years
        filtered_tracks = filter_tracks_by_decade(self.recommended_tracks, '1980s')
        expected_tracks = [self.recommended_tracks[0]]  # Only Track 1 is from the 1980s
        self.assertEqual(filtered_tracks, expected_tracks)

    @patch('src.logic.logic.get_decades_start_and_end_years')
    def test_filter_tracks_1990s(self, mock_get_decades):
        self.setUpDecadeYears()
        mock_get_decades.return_value = self.decade_years
        filtered_tracks = filter_tracks_by_decade(self.recommended_tracks, '1990s')
        expected_tracks = [self.recommended_tracks[1]]  # Only Track 2 is from the 1990s
        self.assertEqual(filtered_tracks, expected_tracks)

    @patch('src.logic.logic.get_decades_start_and_end_years')
    def test_no_tracks_in_decade(self, mock_get_decades):
        self.setUpDecadeYears()
        mock_get_decades.return_value = self.decade_years
        filtered_tracks = filter_tracks_by_decade(self.recommended_tracks, '2000s')  # Assuming no 2000s in songs
        expected_tracks = []  # No tracks should match this decade
        self.assertEqual(filtered_tracks, expected_tracks)

    @patch('src.logic.logic.get_decades_start_and_end_years')
    def test_decade_not_recognized(self, mock_get_decades):
        with pytest.raises(KeyError):
            self.setUpDecadeYears()
            mock_get_decades.return_value = self.decade_years
            filtered_tracks = filter_tracks_by_decade(self.recommended_tracks, '2010s')  # Assuming no 2010s in setup
            expected_tracks = []  # No tracks should match this decade
            self.assertEqual(expected_tracks, filtered_tracks)

    # tests for translate artist names
    @patch('src.services.connect_to_spotify.SpotifyAPIClass')
    def test_translate_artist_names(self, mock_spotify_class):
        # Create a mock instance of the SpotifyAPIClass
        mock_spotify_instance = MagicMock()

        # Mock the response of the query_api method for different artist names
        # Simulate each call to query_api returning a unique artist ID
        mock_spotify_instance.query_api.side_effect = [
            "artist_id_1",
            "artist_id_2",
            "artist_id_3"
        ]

        # Input dictionary with artist names
        params_dict = {"seed_artists": "Artist One,Artist Two,Artist Three"}

        # Expected dictionary with artist IDs
        expected_dict = {"seed_artists": "artist_id_1,artist_id_2,artist_id_3"}

        # Call the function under test
        translate_artist_names(params_dict, mock_spotify_instance)

        # Verify that the params_dict is correctly updated with artist IDs
        self.assertEqual(params_dict, expected_dict)

        # Verify that query_api was called with the correct arguments
        calls = [
            unittest.mock.call("get_artist_id", {"artist_name": "Artist One"}),
            unittest.mock.call("get_artist_id", {"artist_name": "Artist Two"}),
            unittest.mock.call("get_artist_id", {"artist_name": "Artist Three"})
        ]
        mock_spotify_instance.query_api.assert_has_calls(calls, any_order=True)

    # tests for translate track names
    @patch('src.services.connect_to_spotify.SpotifyAPIClass')
    def test_translate_track_names(self, mock_spotify_class):
        # Create a mock instance of the SpotifyAPIClass
        mock_spotify_instance = MagicMock()

        # Mock the response of the query_api method for different track names
        # Simulate each call to query_api returning a unique track ID
        mock_spotify_instance.query_api.side_effect = [
            "track_id_1",
            "track_id_2",
            "track_id_3"
        ]

        # Input dictionary with track names
        params_dict = {"seed_tracks": "Track One,Track Two,Track Three"}

        # Expected dictionary with track IDs
        expected_dict = {"seed_tracks": "track_id_1,track_id_2,track_id_3"}

        # Call the function under test
        translate_track_names(params_dict, mock_spotify_instance)

        # Verify that the params_dict is correctly updated with track IDs
        self.assertEqual(expected_dict, params_dict)

        # Verify that query_api was called with the correct arguments
        calls = [
            unittest.mock.call("get_track_id", {"track_name": "Track One"}),
            unittest.mock.call("get_track_id", {"track_name": "Track Two"}),
            unittest.mock.call("get_track_id", {"track_name": "Track Three"})
        ]
        mock_spotify_instance.query_api.assert_has_calls(calls, any_order=True)

    # tests for get_new_seed_tracks_names
    @patch('src.logic.logic.get_extra_songs_system_prompt')
    @patch('src.logic.logic.OpenAIClass')
    def test_get_new_seed_tracks_names(self, mock_openai_class, mock_get_extra_songs_system_prompt):
        # Mock the system prompt based on previous seed tracks
        mock_system_prompt = "System prompt for new tracks"
        mock_get_extra_songs_system_prompt.return_value = mock_system_prompt

        # Create a mock instance of the OpenAIClass and set the return value for get_chat_response_from_openai
        mock_openai_instance = MagicMock()
        mock_openai_instance.get_chat_response_from_openai.return_value = "New Track 1,New Track 2,New Track 3"
        mock_openai_class.return_value = mock_openai_instance

        # Previous seed tracks and mock user input as a Playlist object
        prev_seed_tracks = ["Old Track 1", "Old Track 2"]
        user_input = Playlist(event="Birthday Party", music_genre="pop", decade="2010s")

        # Expected new seed tracks
        expected_new_seed_tracks = ["New Track 1", "New Track 2", "New Track 3"]

        # Call the function under test
        new_seed_tracks = get_new_seed_tracks_names(prev_seed_tracks, user_input)

        # Verify that the new seed tracks are as expected
        self.assertEqual(expected_new_seed_tracks, new_seed_tracks)

        # Verify that get_chat_response_from_openai was called with the correct arguments
        mock_openai_instance.get_chat_response_from_openai.assert_called_once_with(
            mock_system_prompt,
            str(user_input)
        )

    # test find_min_num_of_tracks_with_spotify_seeds
    @patch('src.logic.logic.SpotifyAPIClass')
    @patch('src.logic.logic.filter_tracks_by_decade')
    def test_find_tracks(self, mock_filter_tracks, mock_spotify_api):
        # Mock successful API response
        mock_spotify_instance = mock_spotify_api.return_value
        mock_spotify_instance.query_api.return_value = [{'id': 'track1'}, {'id': 'track2'}, {'id': 'track3'}]

        # Mock filter_tracks_by_decade if necessary
        mock_filter_tracks.side_effect = lambda tracks, _: tracks  # Return tracks as-is

        # Define test inputs
        min_num = 3
        params_dict = {'seed_tracks': 'track3,track4', 'seed_artists': 'artist1,artist2'}
        user_input = Playlist(event='Driving to the beach', music_genre='rock', mood='happy')

        # Call function
        result = find_min_num_of_tracks_with_spotify_seeds(min_num, params_dict, mock_spotify_instance, user_input)

        # Assertions
        self.assertEqual(len(result), 3)
        self.assertIn({'id': 'track1'}, result)

    # test find_min_num_of_tracks_with_gpt_seeds
    @patch('src.logic.logic.translate_track_names')
    @patch('src.logic.logic.get_new_seed_tracks_names')
    @patch('src.logic.logic.SpotifyAPIClass')
    def test_successful_track_find(self, mock_spotify_api, mock_get_new_seed_tracks_names, mock_translate_track_names):
        # Mock the SpotifyAPI responses for get_recommendations
        mock_spotify_api.return_value.query_api.side_effect = [
            [{'id': 'track1'}, {'id': 'track2'}, {'id': 'track3'}],  # First attempt
            [{'id': 'track4'}, {'id': 'track5'}],  # Second attempt
        ]

        # Mock get_new_seed_tracks_names to simulate fetching new seed tracks
        mock_get_new_seed_tracks_names.return_value = ['track6', 'track7']

        # Mock translate_track_names to simulate conversion of track names to IDs
        mock_translate_track_names.side_effect = lambda params_dict, spotify: None

        # Define test inputs
        min_num = 5
        params_dict = {'seed_tracks': 'trackA,trackB', 'seed_artists': 'artist1,artist2'}
        seed_tracks_names = "trackA,trackB"
        user_input = Playlist(event='Party', music_genre='pop', mood='happy')
        num_attempts = 2

        # Expected result
        expected_tracks = ['track1', 'track2', 'track3', 'track4', 'track5']

        # Execute the test
        result = find_min_num_of_tracks_with_gpt_seeds(min_num, params_dict, mock_spotify_api.return_value, seed_tracks_names, user_input, num_attempts)

        # Verify the result
        self.assertEqual(expected_tracks, result)

        # Verify interactions
        mock_spotify_api.return_value.query_api.assert_called()
        mock_get_new_seed_tracks_names.assert_called_with(['trackA', 'trackB', ['track6', 'track7']], user_input)
        mock_translate_track_names.assert_called()

    # test find_seed_tracks_by_playlist_id
    @patch('src.logic.logic.SpotifyAPIClass')
    def test_playlist_with_not_enough_tracks(self, mock_spotify_class):
        # Mocking SpotifyAPIClass' query_api method to return fewer tracks than needed
        mock_spotify_instance = MagicMock()
        mock_spotify_class.return_value = mock_spotify_instance
        mock_spotify_instance.query_api.return_value = {
            'items': [{'track': {'id': 'track1'}}]}  # Only one track returned

        playlist_id = 'test_playlist_id'
        num_attempts = 1  # Requires 2 tracks but only one is available

        # Call the function
        result = find_seed_tracks_by_playlist_id(playlist_id, mock_spotify_instance, num_attempts)

        # Check that the result is None due to not enough tracks
        self.assertIsNone(result)

    @patch('src.logic.logic.SpotifyAPIClass')
    def test_failed_to_retrieve_playlist(self, mock_spotify_class):
        # Mocking SpotifyAPIClass' query_api method to return None, simulating a failure
        mock_spotify_instance = MagicMock()
        mock_spotify_class.return_value = mock_spotify_instance
        mock_spotify_instance.query_api.return_value = None  # Simulate failure

        playlist_id = 'test_playlist_id'
        num_attempts = 1

        # Call the function
        result = find_seed_tracks_by_playlist_id(playlist_id, mock_spotify_instance, num_attempts)

        # Check that the result is None due to failure to retrieve playlist
        self.assertIsNone(result)

    # test find_seed_artists_by_playlist_id
    @patch('src.services.connect_to_spotify.SpotifyAPIClass')
    def test_find_seed_artists_successful(self, mock_spotify_class):
        mock_instance = mock_spotify_class.return_value
        # Mock the response from SpotifyAPIClass.query_api for getting playlist songs
        mock_instance.query_api.return_value = {
            'items': [{'track': {'artists': [{'id': 'artist1'}]}}, {'track': {'artists': [{'id': 'artist2'}]}}]
        }
        playlist_id = 'test_playlist_id'
        num_attempts = 1

        result = find_seed_artists_by_playlist_id(playlist_id, mock_instance, num_attempts)

        # Since the function randomly selects, we check if the result is one of the possible combinations
        self.assertIn(result, ['artist1,artist2', 'artist2,artist1'])

    @patch('src.logic.logic.SpotifyAPIClass')
    def test_get_most_popular_artists_insufficient_data(self, mock_spotify_class):
        # Setup mock Spotify API responses
        mock_spotify_instance = mock_spotify_class.return_value
        mock_playlist_response = {
            'items': [{'track': {'artists': [{'id': 'artist1'}]}}]  # Only one artist found
        }
        mock_artist_response = {'popularity': 80}
        mock_spotify_instance.query_api.side_effect = [
            mock_playlist_response, mock_artist_response
        ]

        # Execute the function with only one artist available
        playlist_id = 'playlist123'
        num_attempts = 2  # Expecting more than one artist for a successful operation
        result = get_most_popular_artists(playlist_id, mock_spotify_instance, num_attempts)

        # Validate the response to ensure it handles insufficient data gracefully
        self.assertIsNone(result)

    @patch('src.services.connect_to_spotify.SpotifyAPIClass')
    @patch('src.services.connect_to_spotify.SpotifyAPIClass.query_api')
    def test_find_seed_artists_no_artists(self, mock_spotify_class, mock_query_api):
        # Simulate an empty playlist response
        spotify = mock_spotify_class.return_value
        mock_query_api.return_value = {'items': []}
        playlist_id = 'empty_playlist_id'
        num_attempts = 1

        result = find_seed_artists_by_playlist_id(playlist_id, spotify, num_attempts)

        self.assertIsNone(result)

    # test get_most_popular_artists
    @patch('src.logic.logic.SpotifyAPIClass')
    def test_get_most_popular_artists_success(self, mock_spotify_class):
        # Setup mock Spotify API responses
        mock_spotify_instance = mock_spotify_class.return_value
        mock_playlist_response = {
            'items': [{'track': {'artists': [{'id': 'artist1'}, {'id': 'artist2'}]}}, {'track': {'artists': [{'id': 'artist3'}, {'id': 'artist4'}]}}]
        }
        mock_artist_responses = [
            {'popularity': 80}, {'popularity': 90}
        ]
        mock_spotify_instance.query_api.side_effect = [
            mock_playlist_response, *mock_artist_responses
        ]

        # Execute the function
        playlist_id = 'playlist123'
        num_attempts = 1
        result = get_most_popular_artists(playlist_id, mock_spotify_instance, num_attempts)

        # Split the result into a list of artist IDs and sort it
        result_ids = sorted(result.split(','))
        # Define the expected artist IDs as a sorted list
        expected_ids = sorted(['artist1', 'artist3'])
        self.assertEqual(expected_ids, result_ids)

    # test get_most_popular_tracks
    @patch('src.logic.logic.SpotifyAPIClass')
    def test_get_most_popular_tracks_success(self, mock_spotify_class):
        # Setup mock Spotify API responses
        mock_spotify_instance = mock_spotify_class.return_value
        mock_playlist_response = {
            'items': [{'track': {'id': 'track1'}}, {'track': {'id': 'track2'}}]
        }
        mock_track_responses = [
            {'tracks': [{'id': 'track1', 'popularity': 50}, {'id': 'track2', 'popularity': 70}]}
        ]
        mock_spotify_instance.query_api.side_effect = [
            mock_playlist_response, *mock_track_responses
        ]

        # Execute the function
        playlist_id = 'playlist123'
        num_attempts = 1
        result = get_most_popular_tracks(playlist_id, mock_spotify_instance, num_attempts)

        # Validate the response
        expected_result = 'track2,track1'
        self.assertEqual(expected_result, result)

    @patch('src.logic.logic.SpotifyAPIClass')
    def test_get_most_popular_tracks_insufficient_data(self, mock_spotify_class):
        # Setup mock Spotify API responses
        mock_spotify_instance = mock_spotify_class.return_value
        mock_playlist_response = {
            'items': [{'track': {'id': 'track1'}}]  # Only one track found
        }
        mock_track_response = {'tracks': [{'id': 'track1', 'popularity': 50}]}
        mock_spotify_instance.query_api.side_effect = [
            mock_playlist_response, mock_track_response
        ]

        # Execute the function with only one track available
        playlist_id = 'playlist123'
        num_attempts = 2  # Expecting more than one track for a successful operation
        result = get_most_popular_tracks(playlist_id, mock_spotify_instance, num_attempts)

        # Validate the response to ensure it handles insufficient data gracefully
        self.assertIsNone(result)

    # test convert_to_spotify_params_and_create_playlist
    @patch('src.logic.logic.OpenAIClass')
    @patch('src.logic.logic.SpotifyAPIClass')
    @patch('src.logic.logic.find_seed_tracks_and_artists_from_spotify')
    @patch('src.logic.logic.find_min_num_of_tracks_with_spotify_seeds')
    @patch('src.logic.logic.find_min_num_of_tracks_with_gpt_seeds')
    @patch('src.logic.logic.find_nearest_neighbors_by_genre')
    @patch('src.logic.logic.get_playlist_description')
    def test_convert_to_spotify_params_and_create_playlist(
        self, mock_get_playlist_description, mock_find_nearest_neighbors_by_genre,
        mock_find_min_num_of_tracks_with_gpt_seeds, mock_find_min_num_of_tracks_with_spotify_seeds,
        mock_find_seed_tracks_and_artists_from_spotify, mock_spotify_api, mock_openai_api):

        # Mocking OpenAI API response
        mock_openai_instance = mock_openai_api.return_value
        mock_openai_instance.get_chat_response_from_openai.return_value = ('{"seed_genres": "pop", "limit": 100, '
                                                                           '"market": "US"}')

        # Mocking Spotify API interactions
        mock_spotify_instance = mock_spotify_api.return_value
        mock_spotify_instance.query_api.return_value = "https://open.spotify.com/playlist/1"

        # Mocking additional function behaviors
        mock_find_seed_tracks_and_artists_from_spotify.return_value = {"seed_tracks": "track1,track2", "seed_artists": "artist1,artist2"}
        mock_find_min_num_of_tracks_with_spotify_seeds.return_value = ["track1", "track2", "track3"]
        mock_find_min_num_of_tracks_with_gpt_seeds.return_value = ["track4", "track5"]
        mock_find_nearest_neighbors_by_genre.return_value = ["track6"]
        mock_get_playlist_description.return_value = "A playlist for the event"

        # Define test input
        user_input = Playlist(event="Party", music_genre="pop", mood="happy")

        # Execute the function under test
        result = convert_to_spotify_params_and_create_playlist(user_input)

        # Assertions
        self.assertEqual("https://open.spotify.com/playlist/1", result)
        mock_openai_instance.get_chat_response_from_openai.assert_called()
        mock_spotify_instance.query_api.assert_called_with("create_playlist_with_tracks", ANY)

if __name__ == '__main__':
    unittest.main()
