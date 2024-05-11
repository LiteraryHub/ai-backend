from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
import io
from src.model.pydantic_model import BookTextBody
from src.nlp.tts.TTS import generate_audio_book as generate_audio_book_v2
from src.utils.utils import preprocess_arabic_text

# Create a new router for the audiobook generator
router = APIRouter()


@router.post("/v2/text-to-speech", response_class=StreamingResponse)
async def text_to_speech_v2(payload: BookTextBody):
    """
    Converts the given text to speech and returns the audio as a WAV file.

    Args:
        payload (BookTextBody): The request payload containing the text to convert.

    Returns:
        StreamingResponse: The audio file as a WAV file.
    """
    # Generate audio from text
    audio_segment = generate_audio_book_v2(preprocess_arabic_text(payload.text), payload.book_name)

    # Convert the Pydub audio segment to a byte stream
    byte_io = io.BytesIO()
    audio_segment.export(byte_io, format="wav")
    byte_io.seek(0)  # Go to the beginning of the BytesIO buffer

    # Return the audio file
    return StreamingResponse(byte_io, media_type="audio/wav")