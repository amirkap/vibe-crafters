from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pydantic import ValidationError

from src.music_genre import MusicGenre
from src.Playlist import Playlist
from src.logic import get_playlist, get_recommended_artists
import logging

# Configure logging to write to a file
logging.basicConfig(
    filename='VibeCreatorsExceptions.log',
    level=logging.WARNING,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# run the FastAPI app
app = FastAPI()

@app.post("/create_playlist")
async def create_playlist(playlist: Playlist):
    try:
        result = get_playlist(playlist)
        return result
    except ValidationError as e:
        print(f"Error in input parameters: {e}")
        raise HTTPException(status_code=400, detail=f"Error in input parameters: {e}")
    except Exception as e:
        logger.error(f"Error creating playlist: {e}")
        raise HTTPException(status_code=500, detail="Error in creating playlist. Please try again.")


@app.get("/recommended_artists")
async def recommended_artists():
    result = get_recommended_artists()
    return result


result = get_playlist(Playlist(event="sad 10s", music_genre="pop", mood="sad", decade="2000s"))
#result = get_playlist(Playlist(event="Gym Playlist", music_genre="pop", mood="energetic"))
#result = get_playlist(Playlist(event="EuroTrip", music_genre="alternative", mood="dreamy"))