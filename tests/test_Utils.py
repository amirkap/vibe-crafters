import pytest
from src.utils.utils import parse_params_to_dict, extract_nearest_neighbours_input, validate_and_fix_dict, limit_dict_seeds_number, correct_audio_values_in_place

def test_parse_params_to_dict():
    # Valid input string
    input_str = '''{
        "seed_artists": "Bee Gees,KC and The Sunshine Band",
        "seed_tracks": "Stayin' Alive - Bee Gees,That's the Way (I Like It) - KC and The Sunshine Band",
        "target_valence": 0.8,
        "min_valence": 0.7,
        "max_valence": 1.0,
        "target_danceability": 0.8,
        "min_danceability": 0.7,
        "max_danceability": 1.0,
        "target_energy": 0.8,
        "min_energy": 0.7,
        "max_energy": 1.0
    }'''
    expected_output = {
        "seed_artists": "Bee Gees,KC and The Sunshine Band",
        "seed_tracks": "Stayin' Alive - Bee Gees,That's the Way (I Like It) - KC and The Sunshine Band",
        "target_valence": 0.8,
        "min_valence": 0.7,
        "max_valence": 1.0,
        "target_danceability": 0.8,
        "min_danceability": 0.7,
        "max_danceability": 1.0,
        "target_energy": 0.8,
        "min_energy": 0.7,
        "max_energy": 1.0
    }
    assert parse_params_to_dict(input_str) == expected_output

    # Invalid input string (not a dictionary)
    input_str = "[1, 2, 3]"
    expected_output = {"Error": "Input string is not a dictionary"}
    assert parse_params_to_dict(input_str) == expected_output

    # Invalid input string (syntax error)
    input_str = "{invalid: syntax}"
    expected_output = {"Error": "Invalid input string"}
    assert parse_params_to_dict(input_str) == expected_output

    # Empty input string
    input_str = ""
    expected_output = {"Error": "Invalid input string"}
    assert parse_params_to_dict(input_str) == expected_output

    # Non-string input (should raise an exception or return an error)
    input_str = 123
    expected_output = {"Error": "Invalid input string"}
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
    # Test with valid keys
    input_dict = {"min_acousticness": 0.1, "max_acousticness": 0.5, "seed_tracks": "track1,track2"}
    expected_output = input_dict.copy()
    validate_and_fix_dict(input_dict)
    assert input_dict == expected_output

    # Test with mixed keys
    input_dict = {"min_acousticness": 0.1, "invalid_key": "value", "seed_tracks": "track1,track2"}
    expected_output = {"min_acousticness": 0.1, "seed_tracks": "track1,track2"}
    validate_and_fix_dict(input_dict)
    assert input_dict == expected_output

    # Test remove seed artists
    input_dict = {"min_acousticness": 0.1, "seed_artists": "artist1,artist2", "seed_tracks": "track1,track2"}
    expected_output = {"min_acousticness": 0.1, "seed_tracks": "track1,track2"}
    validate_and_fix_dict(input_dict, add_artists=False)
    assert input_dict == expected_output

    # Test convert seed artists to string
    input_dict = {"min_acousticness": 0.1, "seed_artists": ["artist1", "artist2"], "seed_tracks": "track1,track2"}
    expected_output = {"min_acousticness": 0.1, "seed_artists": "artist1,artist2", "seed_tracks": "track1,track2"}
    validate_and_fix_dict(input_dict)
    assert input_dict == expected_output

    # Test convert seed tracks to string
    input_dict = {"min_acousticness": 0.1, "seed_artists": "artist1,artist2", "seed_tracks": ["track1", "track2"]}
    expected_output = {"min_acousticness": 0.1, "seed_artists": "artist1,artist2", "seed_tracks": "track1,track2"}
    validate_and_fix_dict(input_dict)
    assert input_dict == expected_output


def test_limit_dict_seeds_number():
    # Test with fewer than allowed seed artists and tracks
    input_dict = {"seed_artists": "artist1,artist2", "seed_tracks": "track1,track2,track3"}
    expected_output = {"seed_artists": "artist1,artist2", "seed_tracks": "track1,track2"}
    limit_dict_seeds_number(input_dict)
    assert input_dict == expected_output

    # Test with more than allowed seed artists
    input_dict = {"seed_artists": "artist1,artist2,artist3", "seed_tracks": "track1,track2"}
    expected_output = {"seed_artists": "artist1,artist2", "seed_tracks": "track1,track2"}
    limit_dict_seeds_number(input_dict)
    assert input_dict == expected_output

    # Test with more than allowed seed tracks when artists are included
    input_dict = {"seed_artists": "artist1,artist2", "seed_tracks": "track1,track2,track3,track4,track5"}
    expected_output = {"seed_artists": "artist1,artist2", "seed_tracks": "track1,track2"}
    limit_dict_seeds_number(input_dict)
    assert input_dict == expected_output

    # Test with more than allowed seed tracks when artists are not included
    input_dict = {"seed_tracks": "track1,track2,track3,track4,track5"}
    expected_output = {"seed_tracks": "track1,track2,track3,track4"}
    limit_dict_seeds_number(input_dict, add_artists=False)
    assert input_dict == expected_output

    # Test with artists not added and less than allowed seed tracks
    input_dict = {"seed_tracks": "track1,track2"}
    expected_output = input_dict.copy()
    limit_dict_seeds_number(input_dict, add_artists=False)
    assert input_dict == expected_output

    # Test with empty seed artists and tracks
    input_dict = {"seed_artists": "", "seed_tracks": ""}
    expected_output = input_dict.copy()
    limit_dict_seeds_number(input_dict)
    assert input_dict == expected_output

    # Test with seed artists and tracks as lists
    input_dict = {"seed_artists": ["artist1", "artist2", "artist3"], "seed_tracks": ["track1", "track2", "track3", "track4", "track5"]}
    expected_output = {"seed_artists": "artist1,artist2", "seed_tracks": "track1,track2"}
    limit_dict_seeds_number(input_dict)
    assert input_dict == expected_output

    # Test with removal of seed artists
    input_dict = {"seed_artists": "artist1,artist2,artist3", "seed_tracks": "track1,track2,track3"}
    expected_output = {"seed_tracks": "track1,track2,track3"}
    limit_dict_seeds_number(input_dict, add_artists=False)
    assert input_dict == expected_output

    # Test with no seed artists or tracks in the dictionary
    input_dict = {"other_param": "value"}
    expected_output = input_dict.copy()
    limit_dict_seeds_number(input_dict)
    assert input_dict == expected_output


def test_correct_audio_values_in_place():
    input_dict = {
        'target_danceability': 1.2,
        'target_energy': 0.6,
        'target_loudness': -10,
        'target_valence': 0.7,
        'target_acousticness': 2.0
    }
    expected_output = {
        'target_danceability': 1.0,
        'target_energy': 0.552,
        'target_loudness': 0.0,
        'target_valence': 0.651,
        'target_acousticness': 1.0
    }
    correct_audio_values_in_place(input_dict)

    # Round values to avoid floating-point precision issues
    input_dict_rounded = {k: round(v, 3) for k, v in input_dict.items()}
    expected_output_rounded = {k: round(v, 3) for k, v in expected_output.items()}

    assert input_dict_rounded == expected_output_rounded



