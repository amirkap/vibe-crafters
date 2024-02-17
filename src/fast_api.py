from fastapi import FastAPI
from pydantic import BaseModel
from logic import get_playlist, get_recommended_artists
from music_genre import MusicGenre

app = FastAPI()

class Playlist(BaseModel):
    event: str
    music_genre: MusicGenre
    # we need to have a certain format for range, so FastAPI can validate it
    audience_age_range: str 
    year_range: str

    def __str__(self):
        return self.model_dump_json()
    
@app.post("/create_playlist")
async def create_playlist(playlist: Playlist):
    result = get_playlist(playlist)
    return result

@app.get("/get_recommended_artists")
async def get_recommended_artists():
    result = get_recommended_artists()
    return result