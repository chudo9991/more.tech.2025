"""
Avatar service endpoints
"""
import time
from typing import Dict, Any
from fastapi import APIRouter, HTTPException, Depends

from app.schemas.avatar import (
    AvatarGenerateRequest, 
    AvatarResponse
)
# from app.services.avatar_service import AvatarService
from app.services.a2e_service import A2EService
from pydantic import BaseModel

router = APIRouter()

class TTSRequest(BaseModel):
    text: str
    voice_id: str = None
    speech_rate: float = 1.0

class StreamingAvatarRequest(BaseModel):
    avatar_id: str

class StreamingAvatarQuestionRequest(BaseModel):
    avatar_id: str
    question: str

class StreamingAvatarSpeakRequest(BaseModel):
    avatar_id: str
    text: str

class StreamingAvatarContextRequest(BaseModel):
    avatar_id: str
    context: str

class AvatarSettings(BaseModel):
    voice_id: str = None
    avatar_id: str = None
    resolution: int = 720
    speech_rate: float = 1.0
    quality: str = "high"

class AvatarStatus(BaseModel):
    service_status: str
    last_generation: str = None
    total_generations: int = 0
    errors_count: int = 0

class VideoGenerationRequest(BaseModel):
    text: str
    session_id: str
    voice_id: str = None
    avatar_id: str = None
    resolution: int = 720

class FallbackVideoRequest(BaseModel):
    text: str
    session_id: str
    voice_id: str = None
    avatar_id: str = None
    resolution: int = 720

@router.post("/generate")
async def generate_avatar_video(request: VideoGenerationRequest) -> Dict[str, Any]:
    """Generate avatar video from text"""
    try:
        print("=== Generate avatar video endpoint called ===")
        a2e_service = A2EService()
        video_url = await a2e_service.generate_avatar_video_from_text(
            text=request.text,
            voice_id=request.voice_id,
            avatar_id=request.avatar_id,
            resolution=request.resolution,
            title=f"Interview Session {request.session_id}"
        )
        
        if video_url:
            return {
                "success": True,
                "video_url": video_url,
                "session_id": request.session_id,
                "text": request.text
            }
        else:
            raise HTTPException(status_code=400, detail="Video generation failed")
            
    except Exception as e:
        print(f"Error in generate_avatar_video: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/fallback/generate-video")
async def generate_fallback_video(request: FallbackVideoRequest) -> Dict[str, Any]:
    """Generate fallback video when streaming is unavailable"""
    try:
        print("=== Generate fallback video endpoint called ===")
        print(f"Request: {request}")
        
        a2e_service = A2EService()
        video_url = await a2e_service.generate_avatar_video_from_text(
            text=request.text,
            voice_id=request.voice_id or a2e_service.default_voice_id,
            avatar_id=request.avatar_id or a2e_service.default_avatar_id,
            resolution=request.resolution or a2e_service.default_resolution,
            title=f"Interview {request.session_id[:20]}"
        )
        
        if video_url:
            return {
                "success": True,
                "video_url": video_url,
                "session_id": request.session_id,
                "text": request.text,
                "mode": "fallback_video"
            }
        else:
            raise HTTPException(status_code=400, detail="Fallback video generation failed")
            
    except Exception as e:
        print(f"Error in generate_fallback_video: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))





# @router.get("/{session_id}")
# async def get_avatar(session_id: str) -> Dict[str, Any]:
#     """Get avatar for session"""
#     try:
#         avatar_service = AvatarService()
#         avatar_url = await avatar_service.get_avatar_url(session_id)
#         
#         if avatar_url:
#             return {
#                 "avatar_url": avatar_url,
#                 "session_id": session_id
#             }
#         else:
#             raise HTTPException(status_code=404, detail="Avatar not found")
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))


@router.get("/healthz")
async def health_check() -> Dict[str, str]:
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "avatar",
        "version": "1.0.0"
    }

# A2E API Integration Endpoints

@router.get("/voices")
async def get_available_voices(country: str = "ru", region: str = "RU") -> Dict[str, Any]:
    """Get available voices from A2E API"""
    try:
        print("=== Get voices endpoint called ===")
        a2e_service = A2EService()
        voices = await a2e_service.get_available_voices(country, region)
        return {
            "voices": voices,
            "count": len(voices),
            "country": country,
            "region": region
        }
    except Exception as e:
        print(f"Error in get_available_voices: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))



@router.post("/tts")
async def generate_tts(request: TTSRequest) -> Dict[str, Any]:
    """Generate TTS audio from text"""
    try:
        print("=== TTS endpoint called ===")
        a2e_service = A2EService()
        audio_url = await a2e_service.generate_tts(request.text, request.voice_id, request.speech_rate)
        
        if audio_url:
            return {
                "audio_url": audio_url,
                "text": request.text,
                "voice_id": request.voice_id,
                "speech_rate": request.speech_rate
            }
        else:
            raise HTTPException(status_code=400, detail="TTS generation failed")
    except Exception as e:
        print(f"Error in generate_tts: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))

class VideoStatusRequest(BaseModel):
    task_id: str

class AvatarSettings(BaseModel):
    voice_id: str = "66d3f6a704d077b1432fb7d3"  # Anna
    avatar_id: str = "68af59a86eeedd0042ca7e27"  # Default avatar
    resolution: int = 720
    speech_rate: float = 1.0
    language: str = "ru-RU"

class AvatarGeneration(BaseModel):
    session_id: str
    text: str
    video_url: str
    voice_id: str
    avatar_id: str
    resolution: int
    generated_at: float
    status: str = "completed"

@router.post("/video-status")
async def check_video_status(request: VideoStatusRequest) -> Dict[str, Any]:
    """Check video generation status"""
    try:
        print("=== Video status endpoint called ===")
        a2e_service = A2EService()
        status = await a2e_service.check_video_status(request.task_id)
        return status
    except Exception as e:
        print(f"Error in check_video_status: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/settings")
async def get_avatar_settings() -> Dict[str, Any]:
    """Get avatar settings"""
    try:
        print("=== Get settings endpoint called ===")
        # В реальном приложении здесь была бы база данных
        settings = AvatarSettings()
        return {
            "voice_id": settings.voice_id,
            "avatar_id": settings.avatar_id,
            "resolution": settings.resolution,
            "speech_rate": settings.speech_rate,
            "language": settings.language
        }
    except Exception as e:
        print(f"Error in get_avatar_settings: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/settings")
async def update_avatar_settings(settings: AvatarSettings) -> Dict[str, Any]:
    """Update avatar settings"""
    try:
        print("=== Update settings endpoint called ===")
        # В реальном приложении здесь была бы база данных
        return {
            "message": "Settings updated successfully",
            "settings": {
                "voice_id": settings.voice_id,
                "avatar_id": settings.avatar_id,
                "resolution": settings.resolution,
                "speech_rate": settings.speech_rate,
                "language": settings.language
            }
        }
    except Exception as e:
        print(f"Error in update_avatar_settings: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/characters")
async def get_available_characters() -> Dict[str, Any]:
    """Get available characters/avatars"""
    try:
        print("=== Get characters endpoint called ===")
        a2e_service = A2EService()
        characters = await a2e_service.get_available_characters()
        return {
            "characters": characters,
            "count": len(characters)
        }
    except Exception as e:
        print(f"Error in get_available_characters: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/status")
async def get_avatar_status() -> Dict[str, Any]:
    """Get avatar service status"""
    try:
        print("=== Get avatar status endpoint called ===")
        a2e_service = A2EService()
        status = await a2e_service.get_service_status()
        
        # Add additional status information
        status.update({
            "service_type": "A2E Avatar Service",
            "last_generation": None,  # Would be stored in database
            "total_generations": 0,   # Would be stored in database
            "errors_count": 0         # Would be stored in database
        })
        
        return status
    except Exception as e:
        print(f"Error in get_avatar_status: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/settings")
async def get_avatar_settings() -> Dict[str, Any]:
    """Get current avatar settings"""
    try:
        print("=== Get avatar settings endpoint called ===")
        a2e_service = A2EService()
        
        return {
            "voice_id": a2e_service.default_voice_id,
            "avatar_id": a2e_service.default_avatar_id,
            "resolution": a2e_service.default_resolution,
            "speech_rate": a2e_service.default_speech_rate,
            "quality": "high"
        }
    except Exception as e:
        print(f"Error in get_avatar_settings: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/settings")
async def update_avatar_settings(settings: AvatarSettings) -> Dict[str, Any]:
    """Update avatar settings"""
    try:
        print("=== Update avatar settings endpoint called ===")
        print(f"Settings: {settings}")
        
        # In a real application, these would be saved to database
        # For now, we just return the updated settings
        
        return {
            "success": True,
            "settings": {
                "voice_id": settings.voice_id,
                "avatar_id": settings.avatar_id,
                "resolution": settings.resolution,
                "speech_rate": settings.speech_rate,
                "quality": settings.quality
            },
            "message": "Settings updated successfully"
        }
    except Exception as e:
        print(f"Error in update_avatar_settings: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/languages")
async def get_supported_languages() -> Dict[str, Any]:
    """Get supported languages"""
    try:
        print("=== Get languages endpoint called ===")
        languages = [
            {
                "code": "ru-RU",
                "name": "Russian",
                "voices_count": 6
            },
            {
                "code": "en-US", 
                "name": "English (US)",
                "voices_count": 0
            }
        ]
        return {
            "languages": languages,
            "count": len(languages)
        }
    except Exception as e:
        print(f"Error in get_supported_languages: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/streaming")
async def setup_streaming_avatar() -> Dict[str, Any]:
    """Setup streaming avatar for interactivity"""
    try:
        print("=== Setup streaming endpoint called ===")
        # В реальном приложении здесь была бы настройка RTSP стрима
        return {
            "message": "Streaming avatar setup initiated",
            "status": "pending",
            "stream_url": None,
            "note": "RTSP streaming not yet implemented"
        }
    except Exception as e:
        print(f"Error in setup_streaming_avatar: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/a2e-status")
async def get_a2e_status() -> Dict[str, Any]:
    """Get A2E service status"""
    print("=== A2E Status endpoint called ===")
    try:
        print("Creating A2E service directly...")
        a2e_service = A2EService()
        print("Getting A2E service status...")
        status = await a2e_service.get_service_status()
        print(f"A2E status: {status}")
        return status
    except Exception as e:
        print(f"Error in get_a2e_status: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/test")
async def test_endpoint() -> Dict[str, str]:
    """Test endpoint"""
    print("=== Test endpoint called ===")
    return {"message": "Test endpoint works!"}

@router.get("/test-simple")
async def test_simple() -> Dict[str, str]:
    """Simple test endpoint"""
    return {"message": "Simple test works!"}

@router.get("/test-a2e")
async def test_a2e() -> Dict[str, Any]:
    """Test A2E service directly"""
    try:
        print("=== Test A2E endpoint called ===")
        a2e_service = A2EService()
        print("A2E service created successfully")
        return {
            "message": "A2E service test",
            "base_url": a2e_service.base_url,
            "api_key_configured": bool(a2e_service.api_key)
        }
    except Exception as e:
        print(f"Error in test_a2e: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))

# Streaming Avatar Endpoints

@router.get("/streaming-avatars")
async def get_streaming_avatars() -> Dict[str, Any]:
    """Get all available streaming avatars"""
    try:
        print("=== Get streaming avatars endpoint called ===")
        a2e_service = A2EService()
        avatars = await a2e_service.get_streaming_avatars()
        return {
            "avatars": avatars,
            "count": len(avatars)
        }
    except Exception as e:
        print(f"Error in get_streaming_avatars: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/streaming/get-token")
async def get_streaming_token(request: StreamingAvatarRequest) -> Dict[str, Any]:
    """Get streaming avatar token"""
    try:
        print("=== Get streaming token endpoint called ===")
        print(f"Request: {request}")
        a2e_service = A2EService()
        token_data = await a2e_service.get_streaming_token(request.avatar_id)
        
        # Check if there's an error in the response
        if token_data.get("error"):
            if token_data.get("error") == "streaming_unavailable":
                return {
                    "success": False,
                    "error": token_data.get("error"),
                    "message": token_data.get("message"),
                    "avatar_id": request.avatar_id,
                    "stream_url": None,
                    "fallback_mode": True,
                    "fallback_endpoint": "/api/v1/avatar/fallback/generate-video"
                }
            else:
                return {
                    "success": False,
                    "error": token_data.get("error"),
                    "message": token_data.get("message"),
                    "avatar_id": request.avatar_id,
                    "stream_url": None
                }
        
        return {
            "success": True,
            "token": token_data.get("token"),
            "stream_url": token_data.get("stream_url"),
            "avatar_id": request.avatar_id,
            "fallback_mode": False
        }
    except Exception as e:
        print(f"Error in get_streaming_token: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/streaming/set-context")
async def set_streaming_context(request: StreamingAvatarContextRequest) -> Dict[str, Any]:
    """Set QA context for streaming avatar"""
    try:
        print("=== Set streaming context endpoint called ===")
        print(f"Request: {request}")
        a2e_service = A2EService()
        result = await a2e_service.set_streaming_context(request.avatar_id, request.context)
        return {
            "success": result,
            "avatar_id": request.avatar_id,
            "context": request.context
        }
    except Exception as e:
        print(f"Error in set_streaming_context: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/streaming/get-context")
async def get_streaming_context(avatar_id: str) -> Dict[str, Any]:
    """Get QA context for streaming avatar"""
    try:
        print("=== Get streaming context endpoint called ===")
        print(f"Avatar ID: {avatar_id}")
        a2e_service = A2EService()
        context = await a2e_service.get_streaming_context(avatar_id)
        return {
            "success": True,
            "avatar_id": avatar_id,
            "context": context
        }
    except Exception as e:
        print(f"Error in get_streaming_context: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/streaming/ask-question")
async def ask_streaming_question(request: StreamingAvatarQuestionRequest) -> Dict[str, Any]:
    """Ask a question to streaming avatar"""
    try:
        print("=== Ask streaming question endpoint called ===")
        print(f"Request: {request}")
        a2e_service = A2EService()
        response = await a2e_service.ask_streaming_question(request.avatar_id, request.question)
        return {
            "success": True,
            "avatar_id": request.avatar_id,
            "question": request.question,
            "response": response
        }
    except Exception as e:
        print(f"Error in ask_streaming_question: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/streaming/speak")
async def speak_streaming_directly(request: StreamingAvatarSpeakRequest) -> Dict[str, Any]:
    """Make streaming avatar speak directly"""
    try:
        print("=== Speak streaming directly endpoint called ===")
        print(f"Request: {request}")
        a2e_service = A2EService()
        result = await a2e_service.speak_streaming_directly(request.avatar_id, request.text)
        return {
            "success": True,
            "avatar_id": request.avatar_id,
            "text": request.text,
            "result": result
        }
    except Exception as e:
        print(f"Error in speak_streaming_directly: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/streaming/leave-room")
async def leave_streaming_room(request: StreamingAvatarRequest) -> Dict[str, Any]:
    """Leave streaming avatar room"""
    try:
        print("=== Leave streaming room endpoint called ===")
        print(f"Request: {request}")
        a2e_service = A2EService()
        result = await a2e_service.leave_streaming_room(request.avatar_id)
        return {
            "success": result,
            "avatar_id": request.avatar_id
        }
    except Exception as e:
        print(f"Error in leave_streaming_room: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))
