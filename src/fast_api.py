from fastapi import FastAPI
from pydantic import BaseModel
from src.music_genre import MusicGenre
import src.Playlist
from src.logic import *

app = FastAPI()


@app.post("/create_playlist")
async def create_playlist(playlist: Playlist):
    result = get_playlist(playlist)
    return result


@app.get("/recommended_artists")
async def recommended_artists():
    result = get_recommended_artists()
    return result
