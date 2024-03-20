import pytest
from Utils import parse_params_to_dict, extract_nearest_neighbours_input, validate_and_fix_dict, limit_dict_seeds_number, correct_audio_values_in_place

def test_parse_params_to_dict():
    input_str = "{\n    'key1': 'value1',\n    'key2': 2,\n    'key3': 3.0\n}"
    expected_output = {'key1': 'value1', 'key2': 2, 'key3': 3.0}
    assert parse_params_to_dict(input_str) == expected_output

def test_extract_nearest_neighbours_input():
    params_dict = {
        'target_acousticness': 0.5,
        'target_danceability': 0.6,
        'target_energy': 0.7,
        'target_instrumentalness': 0.8,
        'target_valence': 0.9,
        'other_param': 1.0
    }
    expected_output = {
        'acousticness': 0.5,
        'danceability': 0.6,
        'energy': 0.7,
        'instrumentalness': 0.8,
        'valence': 0.9
    }
    assert extract_nearest_neighbours_input(params_dict) == expected_output

def test_validate_and_fix_dict():
    params_dict = {
        'min_acousticness': 0.1,
        'max_acousticness': 0.2,
        'seed_artists': ['artist1', 'artist2'],
        'invalid_param': 0.3
    }
    validate_and_fix_dict(params_dict)
    assert 'invalid_param' not in params_dict
    assert params_dict['seed_artists'] == 'artist1,artist2'

def test_limit_dict_seeds_number():
    params_dict = {
        'seed_artists': ['artist1', 'artist2', 'artist3'],
        'seed_tracks': ['track1', 'track2', 'track3', 'track4', 'track5', 'track6']
    }
    limit_dict_seeds_number(params_dict)
    assert len(params_dict['seed_artists'].split(',')) <= 2
    assert len(params_dict['seed_tracks'].split(',')) <= 2

def test_correct_audio_values_in_place():
    predict_audio_features = {
        'min_danceability': 0.0,
        'max_energy': 1.0,
        'target_loudness': -60.0
    }
    correct_audio_values_in_place(predict_audio_features)
    assert 0 <= predict_audio_features['min_danceability'] <= 1
    assert 0 <= predict_audio_features['max_energy'] <= 1
    assert -60 <= predict_audio_features['target_loudness'] <= 0
