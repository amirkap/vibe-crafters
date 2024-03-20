import unittest
from unittest.mock import patch, MagicMock
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


    @patch('src.logic.OpenAIClass.get_chat_response_from_openai')
    @patch('src.logic.SpotifyAPIClass.create_playlist_with_tracks')
    @patch('src.logic.find_seed_tracks_and_artists_from_spotify')
    @patch('src.logic.find_min_num_of_tracks_with_spotify_seeds')
    def test_convert_to_spotify_params_and_create_playlist(self, mock_find_min_tracks, mock_find_seeds, mock_create_playlist, mock_get_chat_response):
        # Set up mock return values
        mock_get_chat_response.return_value = mock_openai_response
        mock_find_seeds.return_value = mock_find_spotify_seeds_response
        mock_find_min_tracks.return_value = mock_find_min_tracks_response
        mock_create_playlist.return_value = 'playlist_url'

        # Call the function with a mock Playlist object
        user_input = Playlist(event='Driving to the beach', music_genre='rock', mood='happy')
        result = convert_to_spotify_params_and_create_playlist(user_input)

        # Assertions
        self.assertEqual(result, 'playlist_url')
        mock_get_chat_response.assert_called()
        mock_find_seeds.assert_called()
        mock_find_min_tracks.assert_called()
        mock_create_playlist.assert_called()

    @patch('src.logic.OpenAIClass.get_chat_response_from_openai')
    def test_get_new_seed_tracks_names(self, mock_get_chat_response):
        mock_get_chat_response.return_value = 'track1,track2'
        user_input = Playlist(event='Driving to the beach', music_genre='rock', mood='happy')
        result = get_new_seed_tracks_names(['track3', 'track4'], user_input)
        self.assertEqual(result, ['track1', 'track2'])

    @patch('src.logic.SpotifyAPIClass.query_api')
    def test_find_min_num_of_tracks_with_spotify_seeds(self, mock_query_api):
        mock_query_api.return_value = [{'id': 'track1'}, {'id': 'track2'}]
        params_dict = {'seed_tracks': 'track3,track4', 'seed_artists': 'artist1,artist2'}
        spotify = SpotifyAPIClass()
        user_input = Playlist(event='Driving to the beach', music_genre='rock', mood='happy')
        result = find_min_num_of_tracks_with_spotify_seeds(2, params_dict, spotify, user_input)
        self.assertEqual(result, [{'id': 'track1'}, {'id': 'track2'}])

    @patch('src.logic.SpotifyAPIClass.query_api')
    def test_find_min_num_of_tracks_with_gpt_seeds(self, mock_query_api):
        mock_query_api.return_value = [{'id': 'track1'}, {'id': 'track2'}]
        params_dict = {'seed_tracks': 'track3,track4', 'seed_artists': 'artist1,artist2'}
        user_input = Playlist(event='Driving to the beach', music_genre='rock', mood='happy')
        spotify = SpotifyAPIClass()
        result = find_min_num_of_tracks_with_gpt_seeds(2, params_dict, spotify, 'track5,track6', user_input)
        self.assertEqual(result, ['track1', 'track2'])

    @patch('src.logic.SpotifyAPIClass.search_item')
    @patch('src.logic.SpotifyAPIClass.get_playlist_songs')
    def test_find_seed_tracks_and_artists_from_spotify(self, mock_get_playlist_songs, mock_search_item):
        mock_search_item.return_value = mock_search_item_response
        mock_get_playlist_songs.return_value = mock_get_playlist_songs_response
        user_input = Playlist(event='Driving to the beach', music_genre='rock', mood='happy')
        result = find_seed_tracks_and_artists_from_spotify(user_input, 1)
        self.assertIsNotNone(result)
        self.assertIn('seed_tracks', result)
        self.assertIn('seed_artists', result)

    def test_get_most_popular_artists(self, mock_get_artist, mock_get_playlist_songs):
        mock_get_playlist_songs.return_value = {
            'items': [{'track': {'artists': [{'id': 'artist1'}, {'id': 'artist2'}]}}]}
        mock_get_artist.side_effect = [{'popularity': 80}, {'popularity': 90}]
        spotify = SpotifyAPIClass()
        result = get_most_popular_artists('playlist_id', spotify, 1)
        self.assertEqual(result, ['artist2'])

    @patch('src.logic.SpotifyAPIClass.get_playlist_songs')
    @patch('src.logic.SpotifyAPIClass.get_track')
    def test_get_most_popular_tracks(self, mock_get_track, mock_get_playlist_songs):
        mock_get_playlist_songs.return_value = {'items': [{'track': {'id': 'track1'}}, {'track': {'id': 'track2'}}]}
        mock_get_track.side_effect = [{'popularity': 80}, {'popularity': 90}]
        spotify = SpotifyAPIClass()
        result = get_most_popular_tracks('playlist_id', spotify, 1)
        self.assertEqual(result, ['track2'])

    @patch('src.logic.SpotifyAPIClass.get_playlist_songs')
    def test_find_seed_tracks_by_playlist_id(self, mock_get_playlist_songs):
        mock_response = {
            'items': [
                {'track': {'id': 'track1'}},
                {'track': {'id': 'track2'}},
                {'track': {'id': 'track3'}},
                {'track': {'id': 'track4'}},
                {'track': {'id': 'track5'}},
                {'track': {'id': 'track6'}}
            ]
        }
        mock_get_playlist_songs.return_value = mock_response

        spotify = SpotifyAPIClass()
        result = find_seed_tracks_by_playlist_id('playlist_id', spotify, 2)

        self.assertIsNotNone(result)
        self.assertEqual(len(result.split(',')), 4)

    @patch('src.logic.SpotifyAPIClass.get_playlist_songs')
    def test_find_seed_artists_by_playlist_id(self, mock_get_playlist_songs):
        mock_response = {
            'items': [
                {'track': {'artists': [{'id': 'artist1'}]}},
                {'track': {'artists': [{'id': 'artist2'}]}},
                {'track': {'artists': [{'id': 'artist3'}]}},
                {'track': {'artists': [{'id': 'artist4'}]}},
                {'track': {'artists': [{'id': 'artist5'}]}},
                {'track': {'artists': [{'id': 'artist6'}]}}
            ]
        }
        mock_get_playlist_songs.return_value = mock_response

        spotify = SpotifyAPIClass()
        result = find_seed_artists_by_playlist_id('playlist_id', spotify, 2)

        self.assertIsNotNone(result)
        self.assertEqual(len(result.split(',')), 4)

    def test_filter_tracks_by_decade(self):
        # Sample recommended tracks with the updated format
        recommended_tracks = [
            {
                "album": {
                    "release_date": "1975-03-11",
                    "name": "Album 1"
                },
                "name": "Bohemian Rhapsody"
            },
            {
                "album": {
                    "release_date": "1984-01-21",
                    "name": "Album 2"
                },
                "name": "Jump"
            },
            {
                "album": {
                    "release_date": "1991-09-24",
                    "name": "Album 3"
                },
                "name": "Smells Like Teen Spirit"
            },
            {
                "album": {
                    "release_date": "2003-06-09",
                    "name": "Album 4"
                },
                "name": "Seven Nation Army"
            },
            {
                "album": {
                    "release_date": "2014-05-27",
                    "name": "Album 5"
                },
                "name": "Uptown Funk"
            },
            {
                "album": {
                    "release_date": "2021-07-30",
                    "name": "Album 6"
                },
                "name": "Stay"
            }
        ]

        # Test filtering by 1970s
        filtered_tracks = filter_tracks_by_decade(recommended_tracks, '1970s')
        expected_tracks = [
            {
                "album": {
                    "release_date": "1975-03-11",
                    "name": "Album 1"
                },
                "name": "Bohemian Rhapsody"
            }
        ]
        assert filtered_tracks == expected_tracks

        # Test filtering by 1980s
        filtered_tracks = filter_tracks_by_decade(recommended_tracks, '1980s')
        expected_tracks = [
            {
                "album": {
                    "release_date": "1984-01-21",
                    "name": "Album 2"
                },
                "name": "Jump"
            }
        ]
        assert filtered_tracks == expected_tracks

        # Test filtering by 1990s
        filtered_tracks = filter_tracks_by_decade(recommended_tracks, '1990s')
        expected_tracks = [
            {
                "album": {
                    "release_date": "1991-09-24",
                    "name": "Album 3"
                },
                "name": "Smells Like Teen Spirit"
            }
        ]
        assert filtered_tracks == expected_tracks

        # Test filtering by 2000s
        filtered_tracks = filter_tracks_by_decade(recommended_tracks, '2000s')
        expected_tracks = [
            {
                "album": {
                    "release_date": "2003-06-09",
                    "name": "Album 4"
                },
                "name": "Seven Nation Army"
            }
        ]
        assert filtered_tracks == expected_tracks

        # Test filtering by 2010s
        filtered_tracks = filter_tracks_by_decade(recommended_tracks, '2010s')
        expected_tracks = [
            {
                "album": {
                    "release_date": "2014-05-27",
                    "name": "Album 5"
                },
                "name": "Uptown Funk"
            }
        ]
        assert filtered_tracks == expected_tracks

        # Test filtering by 2020s
        filtered_tracks = filter_tracks_by_decade(recommended_tracks, '2020s')
        expected_tracks = [
            {
                "album": {
                    "release_date": "2021-07-30",
                    "name": "Album 6"
                },
                "name": "Stay"
            }
        ]
        assert filtered_tracks == expected_tracks

    @patch('src.logic.SpotifyAPIClass.query_api')
    def test_translate_artist_names(self, mock_query_api):
        params_dict = {"seed_artists": "Artist1,Artist2"}
        spotify = SpotifyAPIClass()

        mock_query_api.side_effect = ['id1', 'id2']
        translate_artist_names(params_dict, spotify)

        self.assertEqual(params_dict["seed_artists"], "id1,id2")

    @patch('src.logic.SpotifyAPIClass.query_api')
    def test_translate_track_names(self, mock_query_api):
        params_dict = {"seed_tracks": "Track1,Track2"}
        spotify = SpotifyAPIClass()

        mock_query_api.side_effect = ['id1', 'id2']
        translate_track_names(params_dict, spotify)

        self.assertEqual(params_dict["seed_tracks"], "id1,id2")

    # Add more tests for other functions as needed


if __name__ == '__main__':
    unittest.main()
