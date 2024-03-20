from pydantic import BaseModel
from src.models.music_genre import MusicGenre
from src.models.mood import Mood
from src.models.decade import Decade
from typing import Optional



class Playlist(BaseModel):
    """
    A class to represent a playlist input parameters form the user to the API.
    """
    event: str
    music_genre: MusicGenre
    mood: Optional[Mood] = None
    decade: Optional[Decade] = None

    def __getitem__(self, key):
        return getattr(self, key)

    def __str__(self):
        return_string = f"Event: {self.event}, Music Genre: {self.music_genre.value}"
        if self.mood:
            return_string += f", Mood: {self.mood.value}"
        if self.decade:
            return_string += f", Decade: {self.decade}"
        return return_string
