import pytest
from src.Playlist import Playlist
from src.music_genre import MusicGenre


# Test cases for valid inputs
@pytest.mark.parametrize("event, music_genre, audience_age_range, year_range", [
    ("Wedding", MusicGenre.POP, "18-35", "2000-2020"),
    ("Party", MusicGenre.ROCK_N_ROLL, "20-50", "1990-2010"),
    ("Corporate Event", MusicGenre.CLASSICAL, "25-60", "1980-2000"),
])
def test_playlist_valid(event, music_genre, audience_age_range, year_range):
    playlist = Playlist(event=event, music_genre=music_genre, audience_age_range=audience_age_range,
                        year_range=year_range)
    assert playlist.event == event
    assert playlist.music_genre == music_genre
    assert playlist.audience_age_range == audience_age_range
    assert playlist.year_range == year_range


# Test cases for invalid audience_age_range
@pytest.mark.parametrize("audience_age_range", [
    "18-17",  # min_age >= max_age
    "-10-30",  # negative min_age
    "30-121",  # max_age > 120
    "abc-def",  # non-numeric
])
def test_playlist_invalid_age_range(audience_age_range):
    with pytest.raises(ValueError):
        Playlist(event="Wedding", music_genre=MusicGenre.POP, audience_age_range=audience_age_range,
                 year_range="2000-2020")


# Test cases for invalid year_range
@pytest.mark.parametrize("year_range", [
    "2000-1999",  # start_year >= end_year
    "1899-2000",  # start_year < 1900
    "2000-2025",  # end_year > current year
    "abc-def",  # non-numeric
])
def test_playlist_invalid_year_range(year_range):
    with pytest.raises(ValueError):
        Playlist(event="Wedding", music_genre=MusicGenre.POP, audience_age_range="18-35", year_range=year_range)


# Test cases for invalid music_genre
@pytest.mark.parametrize("music_genre", [
    "rocknroll",  # incorrect format
    "poprock",  # non-existent genre
    123,  # non-string
])
def test_playlist_invalid_music_genre(music_genre):
    with pytest.raises(ValueError):
        Playlist(event="Wedding", music_genre=music_genre, audience_age_range="18-35", year_range="2000-2020")
