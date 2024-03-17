from fastapi import FastAPI
from pydantic import BaseModel
from src.music_genre import MusicGenre
from src.Playlist import Playlist
from src.logic import get_playlist, get_recommended_artists

app = FastAPI()


@app.post("/create_playlist")
async def create_playlist(playlist: Playlist):
    result = get_playlist(playlist)
    return result


@app.get("/recommended_artists")
async def recommended_artists():
    result = get_recommended_artists()
    return result


#result = get_playlist(Playlist(event="Driving to the beach_new", music_genre="rock", mood="angry"))
result = get_playlist(Playlist(event="Gym Playlist", music_genre="pop", mood="energetic"))