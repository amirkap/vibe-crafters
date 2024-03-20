from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError

from src.models.Playlist import Playlist
from src.logic.logic import get_playlist
from src.logger import *

# run the FastAPI app
app = FastAPI()

origins = [
    "*"
]

# Add CORSMiddleware to the application
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # List of origins that are allowed to make requests
    allow_credentials=True,  # Whether to support cookies
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Serve files from the "frontend" directory under the "/frontend" route
#app.mount("/src/UI", StaticFiles(directory="/src/UI", html=True), name="frontend")

@app.post("/create_playlist")
async def create_playlist(playlist: Playlist):
    try:
        result = get_playlist(playlist)
        return {"playlist_url": result}
    except ValidationError as e:
        print(f"Error in input parameters: {e}")
        raise HTTPException(status_code=400, detail=f"Error in input parameters: {e}")
    except Exception as e:
        logger.error(f"Error creating playlist: {e}")
        raise HTTPException(status_code=500, detail="Error in creating playlist. Please try again.")

#result = get_playlist(Playlist(event="sad 10s", music_genre="pop", mood="sad", decade="2000s"))
result = get_playlist(Playlist(event="Gym Playlist", music_genre="pop", mood="energetic"))
#result = get_playlist(Playlist(event="EuroTrip", music_genre="alternative", mood="dreamy"))