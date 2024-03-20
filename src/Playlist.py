from datetime import datetime
from pydantic import BaseModel, field_validator
from src.music_genre import MusicGenre
from src.mood import Mood
from src.decade import Decade
import re
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
