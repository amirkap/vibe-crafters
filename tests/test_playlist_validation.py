import pytest
from src.models.Playlist import Playlist
from src.models.music_genre import MusicGenre
from src.models.mood import Mood
from src.models.decade import Decade

# Test cases for valid inputs
@pytest.mark.parametrize("event, music_genre, mood, decade", [
    ("Wedding", MusicGenre.POP, Mood.HAPPY, Decade.EIGHTIES),
    ("Party", MusicGenre.ROCK_N_ROLL, Mood.ENERGETIC, Decade.FIFTIES),
    ("Corporate Event", MusicGenre.CLASSICAL, Mood.SERENE, Decade.TWENTY_TENS),
])
def test_playlist_valid(event, music_genre, mood, decade):
    playlist = Playlist(event=event, music_genre=music_genre, mood=mood, decade=decade)
    assert playlist.event == event
    assert playlist.music_genre == music_genre
    assert playlist.mood == mood
    assert playlist.decade == decade

# Test cases for invalid decade
@pytest.mark.parametrize("decade", [
    "195",        # incomplete and missing 's'
    "2030s",      # decade beyond defined range
    "nineteen80s", # incorrect format
    1990,        # numeric value, assuming a typo without quotes
    "random"      # completely unrelated string
])
def test_playlist_invalid_decade(decade):
    with pytest.raises(ValueError):
        Playlist(event="Wedding", music_genre=MusicGenre.POP, mood=Mood.HAPPY, decade=decade)

# Test cases for invalid music_genre
@pytest.mark.parametrize("music_genre", [
    "rocknroll",  # incorrect format
    "poprock",    # non-existent genre
    123,          # non-string
    "",           # empty string
])
def test_playlist_invalid_music_genre(music_genre):
    with pytest.raises(ValueError):
        Playlist(event="Wedding", music_genre=music_genre, mood=Mood.HAPPY, decade="1950s")

# Test cases for invalid mood
@pytest.mark.parametrize("mood", [
    "notpartofenum",      # incorrect format
    123,          # non-string
    None,         # null value (Mood is optional, so this should not raise an error)
    "happy123",   # mixed alphanumeric
    "",           # empty string
    " ",          # whitespace
])
def test_playlist_invalid_mood(mood):
    if mood is None:
        playlist = Playlist(event="Wedding", music_genre=MusicGenre.POP, mood=mood, decade="1950s")
        assert playlist.mood is None
    else:
        with pytest.raises(ValueError):
            Playlist(event="Wedding", music_genre=MusicGenre.POP, mood=mood, decade="1950s")
