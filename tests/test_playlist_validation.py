import pytest
from src.Playlist import Playlist
from src.music_genre import MusicGenre
from src.mood import Mood

# Test cases for valid inputs
@pytest.mark.parametrize("event, music_genre, mood, year_range", [
    ("Wedding", MusicGenre.POP, Mood.HAPPY, "2000-2020"),
    ("Party", MusicGenre.ROCK_N_ROLL, Mood.ENERGETIC, "1990-2010"),
    ("Corporate Event", MusicGenre.CLASSICAL, Mood.SERENE, "1980-2000"),
])
def test_playlist_valid(event, music_genre, mood, year_range):
    playlist = Playlist(event=event, music_genre=music_genre, mood=mood, year_range=year_range)
    assert playlist.event == event
    assert playlist.music_genre == music_genre
    assert playlist.mood == mood
    assert playlist.year_range == year_range

# Test cases for invalid year_range
@pytest.mark.parametrize("year_range", [
    "2000-1999",  # start_year >= end_year
    "1899-2000",  # start_year < 1900
    "2000-2025",  # end_year > current year
    "abc-def",    # non-numeric
])
def test_playlist_invalid_year_range(year_range):
    with pytest.raises(ValueError):
        Playlist(event="Wedding", music_genre=MusicGenre.POP, mood=Mood.HAPPY, year_range=year_range)

# Test cases for invalid music_genre
@pytest.mark.parametrize("music_genre", [
    "rocknroll",  # incorrect format
    "poprock",    # non-existent genre
    123,          # non-string
])
def test_playlist_invalid_music_genre(music_genre):
    with pytest.raises(ValueError):
        Playlist(event="Wedding", music_genre=music_genre, mood=Mood.HAPPY, year_range="2000-2020")

# Test cases for invalid mood
@pytest.mark.parametrize("mood", [
    "angry",   # incorrect format
    123,       # non-string
    None,      # null value
])
def test_playlist_invalid_mood(mood):
    with pytest.raises(ValueError):
        Playlist(event="Wedding", music_genre=MusicGenre.POP, mood=mood, year_range="2000-2020")
