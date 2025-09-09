"""
Avatar service endpoints - D-ID only
"""
import time
from typing import Dict, Any
from fastapi import APIRouter, HTTPException, Depends

from app.schemas.avatar import (
    AvatarGenerateRequest, 
    AvatarResponse
)
from app.services.did_streaming_service import DIDStreamingService
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
    resolution: int = 720  # 1:1 format (720x720)
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
    resolution: int = 720  # 1:1 format (720x720)

class FallbackVideoRequest(BaseModel):
    text: str
    session_id: str
    voice_id: str = None
    avatar_id: str = None
    resolution: int = 720  # 1:1 format (720x720)

@router.post("/generate")
async def generate_avatar_video(request: VideoGenerationRequest) -> Dict[str, Any]:
    """Generate avatar video from text using D-ID"""
    try:
        print("=== Generate avatar video endpoint called (D-ID) ===")
        did_service = DIDStreamingService()
        
        # Create avatar if needed
        avatar_result = await did_service.create_avatar()
        if not avatar_result.get("success"):
            raise HTTPException(status_code=400, detail="Failed to create avatar")
        
        avatar_id = avatar_result["avatar_id"]
        
        # Get streaming token (session)
        token_result = await did_service.get_streaming_token(avatar_id)
        if not token_result.get("success"):
            raise HTTPException(status_code=400, detail="Failed to create streaming session")
        
        # Make avatar speak
        speak_success = await did_service.speak_streaming_directly(avatar_id, request.text)
        if not speak_success:
            raise HTTPException(status_code=400, detail="Failed to make avatar speak")
        
        return {
            "success": True,
            "avatar_id": avatar_id,
            "session_id": request.session_id,
            "text": request.text,
            "stream_url": token_result.get("stream_url"),
            "mode": "d-id_streaming"
        }
            
    except Exception as e:
        print(f"Error in generate_avatar_video: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/fallback/generate-video")
async def generate_fallback_video(request: FallbackVideoRequest) -> Dict[str, Any]:
    """Generate fallback video using D-ID when streaming is unavailable"""
    try:
        print("=== Generate fallback video endpoint called (D-ID) ===")
        print(f"Request: {request}")
        
        did_service = DIDStreamingService()
        
        # Create avatar
        avatar_result = await did_service.create_avatar()
        if not avatar_result.get("success"):
            raise HTTPException(status_code=400, detail="Failed to create avatar")
        
        avatar_id = avatar_result["avatar_id"]
        
        # Try to get streaming session
        token_result = await did_service.get_streaming_token(avatar_id)
        if token_result.get("success"):
            # Make avatar speak
            speak_success = await did_service.speak_streaming_directly(avatar_id, request.text)
            if speak_success:
                return {
                    "success": True,
                    "avatar_id": avatar_id,
                    "session_id": request.session_id,
                    "text": request.text,
                    "stream_url": token_result.get("stream_url"),
                    "mode": "d-id_fallback"
                }
        
        raise HTTPException(status_code=400, detail="D-ID fallback video generation failed")
            
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

# D-ID API Integration Endpoints

@router.get("/voices")
async def get_available_voices() -> Dict[str, Any]:
    """Get available voices for D-ID"""
    try:
        print("=== Get voices endpoint called (D-ID) ===")
        # D-ID uses ElevenLabs voices
        voices = [
            {
                "id": "Dimf6681ffz3PTVPPAEX",
                "name": "D-ID Default Voice",
                "provider": "elevenlabs",
                "language": "ru-RU"
            }
        ]
        return {
            "voices": voices,
            "count": len(voices),
            "provider": "d-id"
        }
    except Exception as e:
        print(f"Error in get_available_voices: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/tts")
async def generate_tts(request: TTSRequest) -> Dict[str, Any]:
    """Generate TTS using D-ID (via streaming)"""
    try:
        print("=== TTS endpoint called (D-ID) ===")
        did_service = DIDStreamingService()
        
        # For D-ID, TTS is integrated into streaming
        # We'll create a temporary avatar and make it speak
        avatar_result = await did_service.create_avatar()
        if not avatar_result.get("success"):
            raise HTTPException(status_code=400, detail="Failed to create avatar for TTS")
        
        avatar_id = avatar_result["avatar_id"]
        
        # Get streaming session
        token_result = await did_service.get_streaming_token(avatar_id)
        if not token_result.get("success"):
            raise HTTPException(status_code=400, detail="Failed to create streaming session for TTS")
        
        # Make avatar speak (this generates the TTS)
        speak_success = await did_service.speak_streaming_directly(avatar_id, request.text)
        
        if speak_success:
            return {
                "success": True,
                "text": request.text,
                "voice_id": request.voice_id,
                "avatar_id": avatar_id,
                "stream_url": token_result.get("stream_url"),
                "provider": "d-id"
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
    resolution: int = 720  # 1:1 format (720x720)
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

@router.get("/settings")
async def get_avatar_settings() -> Dict[str, Any]:
    """Get avatar settings for D-ID"""
    try:
        print("=== Get settings endpoint called (D-ID) ===")
        from app.core.config import settings
        
        return {
            "voice_id": settings.DID_DEFAULT_VOICE,
            "avatar_image": settings.DID_DEFAULT_AVATAR_IMAGE,
            "agent_id": settings.DID_DEFAULT_AGENT_ID,
            "provider": "d-id"
        }
    except Exception as e:
        print(f"Error in get_avatar_settings: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/settings")
async def update_avatar_settings(settings: AvatarSettings) -> Dict[str, Any]:
    """Update avatar settings for D-ID"""
    try:
        print("=== Update settings endpoint called (D-ID) ===")
        print(f"Settings: {settings}")
        
        return {
            "success": True,
            "settings": {
                "voice_id": settings.voice_id,
                "avatar_id": settings.avatar_id,
                "provider": "d-id"
            },
            "message": "D-ID settings updated successfully"
        }
    except Exception as e:
        print(f"Error in update_avatar_settings: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/characters")
async def get_available_characters() -> Dict[str, Any]:
    """Get available D-ID avatars"""
    try:
        print("=== Get characters endpoint called (D-ID) ===")
        did_service = DIDStreamingService()
        characters = await did_service.get_available_streaming_avatars()
        return {
            "characters": characters,
            "count": len(characters),
            "provider": "d-id"
        }
    except Exception as e:
        print(f"Error in get_available_characters: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/status")
async def get_avatar_status() -> Dict[str, Any]:
    """Get D-ID avatar service status"""
    try:
        print("=== Get avatar status endpoint called (D-ID) ===")
        did_service = DIDStreamingService()
        status = await did_service.get_streaming_status()
        
        status.update({
            "service_type": "D-ID Avatar Service",
            "provider": "d-id"
        })
        
        return status
    except Exception as e:
        print(f"Error in get_avatar_status: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/languages")
async def get_supported_languages() -> Dict[str, Any]:
    """Get supported languages for D-ID"""
    try:
        print("=== Get languages endpoint called (D-ID) ===")
        languages = [
            {
                "code": "ru-RU",
                "name": "Russian",
                "provider": "d-id"
            },
            {
                "code": "en-US", 
                "name": "English (US)",
                "provider": "d-id"
            }
        ]
        return {
            "languages": languages,
            "count": len(languages),
            "provider": "d-id"
        }
    except Exception as e:
        print(f"Error in get_supported_languages: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/test")
async def test_endpoint() -> Dict[str, str]:
    """Test endpoint"""
    print("=== Test endpoint called ===")
    return {"message": "Test endpoint works!", "provider": "d-id"}

@router.get("/test-did")
async def test_did() -> Dict[str, Any]:
    """Test D-ID service directly"""
    try:
        print("=== Test D-ID endpoint called ===")
        did_service = DIDStreamingService()
        status = await did_service.get_streaming_status()
        return {
            "message": "D-ID service test",
            "status": status,
            "provider": "d-id"
        }
    except Exception as e:
        print(f"Error in test_did: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))

# D-ID Streaming Avatar Endpoints

@router.get("/streaming/avatars")
async def get_streaming_avatars() -> Dict[str, Any]:
    """Get all available D-ID streaming avatars"""
    try:
        print("=== Get streaming avatars endpoint called (D-ID) ===")
        streaming_service = DIDStreamingService()
        avatars = await streaming_service.get_available_streaming_avatars()
        return {
            "success": True,
            "avatars": avatars,
            "total_count": len(avatars),
            "provider": "d-id"
        }
    except Exception as e:
        print(f"Error in get_streaming_avatars: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/streaming/get-token")
async def get_streaming_token(request: StreamingAvatarRequest) -> Dict[str, Any]:
    """Get D-ID streaming avatar token"""
    try:
        print("=== Get streaming token endpoint called (D-ID) ===")
        print(f"Request: {request}")
        streaming_service = DIDStreamingService()
        token_data = await streaming_service.get_streaming_token(request.avatar_id)
        
        # Check if there's an error in the response
        if not token_data.get("success"):
            if token_data.get("fallback_mode"):
                return {
                    "success": False,
                    "error": token_data.get("error"),
                    "message": token_data.get("message"),
                    "avatar_id": request.avatar_id,
                    "stream_url": None,
                    "fallback_mode": True,
                    "fallback_endpoint": "/api/v1/avatar/fallback/generate-video",
                    "provider": "d-id"
                }
            else:
                return {
                    "success": False,
                    "error": token_data.get("error"),
                    "message": token_data.get("message"),
                    "avatar_id": request.avatar_id,
                    "stream_url": None,
                    "provider": "d-id"
                }
        
        return {
            "success": True,
            "token": token_data.get("token"),
            "stream_url": token_data.get("stream_url"),
            "room_id": token_data.get("room_id"),
            "avatar_id": request.avatar_id,
            "fallback_mode": False,
            "provider": "d-id"
        }
    except Exception as e:
        print(f"Error in get_streaming_token: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/streaming/set-context")
async def set_streaming_context(request: StreamingAvatarContextRequest) -> Dict[str, Any]:
    """Set QA context for D-ID streaming avatar"""
    try:
        print("=== Set streaming context endpoint called (D-ID) ===")
        print(f"Request: {request}")
        streaming_service = DIDStreamingService()
        result = await streaming_service.set_streaming_context(request.avatar_id, request.context)
        return {
            "success": result,
            "avatar_id": request.avatar_id,
            "context": request.context,
            "provider": "d-id"
        }
    except Exception as e:
        print(f"Error in set_streaming_context: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/streaming/get-context")
async def get_streaming_context(avatar_id: str) -> Dict[str, Any]:
    """Get QA context for D-ID streaming avatar"""
    try:
        print("=== Get streaming context endpoint called (D-ID) ===")
        print(f"Avatar ID: {avatar_id}")
        streaming_service = DIDStreamingService()
        context = await streaming_service.get_streaming_context(avatar_id)
        return {
            "success": True,
            "avatar_id": avatar_id,
            "context": context,
            "provider": "d-id"
        }
    except Exception as e:
        print(f"Error in get_streaming_context: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/streaming/ask-question")
async def ask_streaming_question(request: StreamingAvatarQuestionRequest) -> Dict[str, Any]:
    """Ask a question to D-ID streaming avatar"""
    try:
        print("=== Ask streaming question endpoint called (D-ID) ===")
        print(f"Request: {request}")
        streaming_service = DIDStreamingService()
        response = await streaming_service.ask_streaming_question(request.avatar_id, request.question)
        return {
            "success": True,
            "avatar_id": request.avatar_id,
            "question": request.question,
            "response": response,
            "provider": "d-id"
        }
    except Exception as e:
        print(f"Error in ask_streaming_question: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/streaming/speak")
async def speak_streaming_directly(request: StreamingAvatarSpeakRequest) -> Dict[str, Any]:
    """Make D-ID streaming avatar speak directly"""
    try:
        print("=== Speak streaming directly endpoint called (D-ID) ===")
        print(f"Request: {request}")
        streaming_service = DIDStreamingService()
        result = await streaming_service.speak_streaming_directly(request.avatar_id, request.text)
        return {
            "success": True,
            "avatar_id": request.avatar_id,
            "text": request.text,
            "result": result,
            "provider": "d-id"
        }
    except Exception as e:
        print(f"Error in speak_streaming_directly: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/streaming/leave-room")
async def leave_streaming_room(request: StreamingAvatarRequest) -> Dict[str, Any]:
    """Leave D-ID streaming avatar room"""
    try:
        print("=== Leave streaming room endpoint called (D-ID) ===")
        print(f"Request: {request}")
        streaming_service = DIDStreamingService()
        result = await streaming_service.leave_streaming_room(request.avatar_id)
        return {
            "success": result,
            "avatar_id": request.avatar_id,
            "provider": "d-id"
        }
    except Exception as e:
        print(f"Error in leave_streaming_room: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/streaming/status")
async def get_streaming_status() -> Dict[str, Any]:
    """Get D-ID streaming service status"""
    try:
        print("=== Get streaming status endpoint called (D-ID) ===")
        streaming_service = DIDStreamingService()
        status = await streaming_service.get_streaming_status()
        return {
            "success": True,
            "status": status,
            "provider": "d-id"
        }
    except Exception as e:
        print(f"Error in get_streaming_status: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))
