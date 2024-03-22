from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import ValidationError
from pathlib import Path
from src.api_calls_db.log_api_calls_db import log_api_call
from src.models.Playlist import Playlist
from src.logic.logic import get_playlist
from src.exception_logs_db.logger import *

# run the FastAPI app
app = FastAPI()

# Add the static files (frontend files) to the application
current_file_path = Path(__file__).resolve()
project_root = current_file_path.parent
static_files_path = project_root / "static"
app.mount("/static", StaticFiles(directory=static_files_path), name="static")


origins = [
    "*"
]

# Add CORSMiddleware to the application.
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # List of origins that are allowed to make requests
    allow_credentials=True,  # Whether to support cookies
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Middleware for logging API calls
@app.middleware("http")
async def db_log_middleware(request: Request, call_next):
    response = await call_next(request)
    path = request.url.path
    success = response.status_code < 400  # Success if status code is less than 400
    ip_address = request.client.host
    try:
        log_api_call(path, success, ip_address)  # Log the API call
    except Exception as e:
        logger.exception(f"Error logging API call: {e}")
    return response

@app.get("/")
async def serve_spa():
    return FileResponse("src/static/index.html")

@app.post("/api/create_playlist")
async def create_playlist(playlist: Playlist):
    try:
        result = get_playlist(playlist)
        return {"playlist_url": result}
    except ValidationError as e:
        print(f"Error in input parameters: {e}")
        raise HTTPException(status_code=400, detail=f"Error in input parameters: {e}")
    except Exception as e:
        logger.exception(f"Error creating playlist: {e}")
        raise HTTPException(status_code=500, detail="Error in creating playlist. Please try again.")