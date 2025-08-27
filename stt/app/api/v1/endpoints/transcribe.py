"""
Transcription endpoints for STT service
"""
from typing import Dict, Any
from fastapi import APIRouter, HTTPException, UploadFile, File, Form

from app.schemas.transcribe import TranscribeRequest, TranscribeResponse
from app.services.transcribe_service import TranscribeService

router = APIRouter()


@router.post("/transcribe", response_model=TranscribeResponse)
async def transcribe_audio(
    request: TranscribeRequest
) -> Dict[str, Any]:
    """Transcribe audio file to text"""
    try:
        transcribe_service = TranscribeService()
        result = await transcribe_service.transcribe(
            audio_url=request.audio_url,
            language=request.language,
            vad_enabled=request.vad_enabled
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/transcribe-file")
async def transcribe_audio_file(
    audio: UploadFile = File(...),
    session_id: str = Form(...)
) -> Dict[str, Any]:
    """Transcribe uploaded audio file to text"""
    try:
        print(f"Received audio file: {audio.filename}, size: {audio.size}")
        
        # Read audio file
        audio_data = await audio.read()
        print(f"Read {len(audio_data)} bytes of audio data")
        
        # Generate filename (remove codecs part)
        base_filename = audio.filename
        if ';codecs=' in base_filename:
            base_filename = base_filename.split(';codecs=')[0]
        filename = f"{session_id}_{base_filename}"
        print(f"Generated filename: {filename}")
        
        # Save to MinIO
        transcribe_service = TranscribeService()
        print("Saving audio to MinIO...")
        minio_url = await transcribe_service.save_audio_to_minio(audio_data, filename)
        print(f"Audio saved to MinIO: {minio_url}")
        
        # Transcribe audio
        print("Starting transcription...")
        result = await transcribe_service.transcribe(
            audio_url=minio_url,
            language="ru",
            vad_enabled=True
        )
        print(f"Transcription completed: {result}")
        
        return result
    except Exception as e:
        print(f"Error in transcribe_audio_file: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
