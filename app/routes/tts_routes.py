from fastapi import APIRouter
from fastapi.responses import FileResponse
from pydantic import BaseModel
from app.services.tts_service import text_to_speech, cleanup_old_audio_files
import os

router = APIRouter()

class TTSRequest(BaseModel):
    text: str
    language: str = 'en'

@router.post("/")
async def generate_speech(request: TTSRequest):
    """
    Generate speech from text in the specified language.
    Returns the audio file.
    """
    # Clean up old files periodically
    cleanup_old_audio_files()
    
    # Generate audio
    audio_path = text_to_speech(request.text, request.language)
    
    if audio_path and os.path.exists(audio_path):
        return FileResponse(
            audio_path,
            media_type="audio/mpeg",
            filename="response.mp3"
        )
    else:
        return {"error": "Failed to generate audio"}
