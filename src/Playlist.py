from datetime import datetime
from pydantic import BaseModel, field_validator
from src.music_genre import MusicGenre
from src.mood import Mood
import re
from typing import Optional



class Playlist(BaseModel):
    event: str
    music_genre: MusicGenre
    mood: Optional[Mood] = None
    year_range: Optional[str] = None

    @field_validator('year_range')
    @classmethod
    def validate_year_range(cls, v):
        if not re.match(r'^\d{4}-\d{4}$', v):
            raise ValueError('Year range must be in the format "start_year-end_year"')
        start_year, end_year = map(int, v.split('-'))
        current_year = datetime.now().year
        if start_year < 1900:
            raise ValueError('Start year must not be earlier than 1900')
        if end_year > current_year:
            raise ValueError('End year must not be later than the current year')
        if start_year >= end_year:
            raise ValueError('Start year must be less than end year')
        return v

    def __getitem__(self, key):
        return getattr(self, key)
