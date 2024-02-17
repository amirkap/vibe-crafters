from pydantic import BaseModel
from src.music_genre import MusicGenre


class Playlist(BaseModel):
    event: str
    music_genre: MusicGenre
    # we need to have a certain format for range, so FastAPI can validate it
    audience_age_range: str
    year_range: str

    def __str__(self):
        return self.json()

    def __getitem__(self, key):
        return getattr(self, key)