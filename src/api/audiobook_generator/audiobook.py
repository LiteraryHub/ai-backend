from fastapi import APIRouter
from fastapi.responses import JSONResponse
import io
import soundfile as sf
from src.model.pydantic_model import BookTextBody
from src.nlp.tts.TTS import generate_audio_book as generate_audio_book_v2
import os
from src.utils.utils import preprocess_arabic_text

# Create a new router for the audiobook generator
router = APIRouter()

@router.post("/v2/text-to-speech")
async def text_to_speech_v2(payload: BookTextBody):
    """
    Converts the given text to speech and returns the audio as a WAV file.

    Args:
        payload (BookTextBody): The request payload containing the text to convert.

    Returns:
        JSONResponse: The audio file as a mp3 file.
    """
    audio_book_output_path = generate_audio_book_v2(payload.text, payload.book_name)
    return JSONResponse(content={"audio_book_output_path": audio_book_output_path})
