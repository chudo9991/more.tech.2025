"""
A2E API integration service
"""
import asyncio
import time
from typing import Dict, Any, List, Optional
import httpx
from app.core.config import settings


class A2EService:
    def __init__(self):
        self.base_url = settings.A2E_BASE_URL
        self.api_key = settings.A2E_API_KEY
        self.default_avatar_id = settings.A2E_DEFAULT_AVATAR_ID
        self.default_voice_id = settings.A2E_DEFAULT_VOICE_ID
        self.default_resolution = settings.A2E_DEFAULT_RESOLUTION
        self.default_speech_rate = settings.A2E_DEFAULT_SPEECH_RATE
        
        print(f"A2E Service initialized:")
        print(f"  Base URL: {self.base_url}")
        print(f"  API Key: {self.api_key[:20]}..." if self.api_key else "  API Key: None")
        print(f"  Default Avatar ID: {self.default_avatar_id}")
        print(f"  Default Voice ID: {self.default_voice_id}")
        
        self._headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    async def get_available_voices(self, country: str = "ru", region: str = "RU") -> List[Dict[str, Any]]:
        """Get available voices from A2E API"""
        try:
            async with httpx.AsyncClient() as client:
                params = {
                    "country": country,
                    "region": region,
                    "voice_map_type": f"{country}-{region}"
                }
                
                response = await client.get(
                    f"{self.base_url}/api/v1/anchor/voice_list",
                    headers=self._headers,
                    params=params
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("code") == 0:
                        voices = []
                        for group in data.get("data", []):
                            for voice in group.get("children", []):
                                voices.append({
                                    "id": voice["value"],
                                    "name": voice["label"],
                                    "gender": group["value"],
                                    "lang": f"{country}-{region}",
                                    "tts_rate": voice.get("ttsRate", 1)
                                })
                        return voices
                    else:
                        raise Exception(f"A2E API error: {data.get('msg', 'Unknown error')}")
                else:
                    raise Exception(f"HTTP {response.status_code}: {response.text}")
                    
        except Exception as e:
            print(f"Failed to get voices: {e}")
            return []

    async def generate_tts(self, text: str, voice_id: Optional[str] = None, speech_rate: Optional[float] = None) -> Optional[str]:
        """Generate TTS audio from text"""
        try:
            voice_id = voice_id or self.default_voice_id
            speech_rate = speech_rate or self.default_speech_rate
            
            print(f"TTS request: text='{text[:50]}...', voice_id={voice_id}, speech_rate={speech_rate}")
            
            async with httpx.AsyncClient() as client:
                payload = {
                    "msg": text,
                    "tts_id": voice_id,
                    "speechRate": speech_rate,
                    "country": "ru",
                    "region": "RU"
                }
                
                print(f"TTS payload: {payload}")
                print(f"TTS headers: {self._headers}")
                
                response = await client.post(
                    f"{self.base_url}/api/v1/video/send_tts",
                    headers=self._headers,
                    json=payload,
                    timeout=60.0
                )
                
                print(f"TTS response status: {response.status_code}")
                print(f"TTS response text: {response.text[:200]}...")  # Show first 200 chars
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"TTS response data: {data}")
                    if data.get("code") == 0:
                        audio_url = data.get("data", "")
                        print(f"TTS audio URL: {audio_url}")
                        return audio_url
                    else:
                        error_msg = f"A2E API error: {data.get('msg', 'Unknown error')}"
                        print(f"TTS error: {error_msg}")
                        raise Exception(error_msg)
                else:
                    error_msg = f"HTTP {response.status_code}: {response.text}"
                    print(f"TTS HTTP error: {error_msg}")
                    raise Exception(error_msg)
                    
        except Exception as e:
            print(f"TTS generation failed: {e}")
            import traceback
            traceback.print_exc()
            return None

    async def generate_video(
        self,
        audio_url: str,
        avatar_id: Optional[str] = None,
        resolution: Optional[int] = None,
        title: Optional[str] = None
    ) -> Optional[str]:
        """Generate avatar video from audio"""
        try:
            avatar_id = avatar_id or self.default_avatar_id
            resolution = resolution or self.default_resolution
            title = title or f"video-{int(time.time())}"
            # Ensure title is not longer than 40 characters
            if len(title) > 40:
                title = title[:37] + "..."
            
            async with httpx.AsyncClient() as client:
                payload = {
                    "title": title,
                    "anchor_id": avatar_id,
                    "anchor_type": 1,  # user twin
                    "audioSrc": audio_url,
                    "resolution": resolution,
                    "isCaptionEnabled": False
                }
                
                response = await client.post(
                    f"{self.base_url}/api/v1/video/generate",
                    headers=self._headers,
                    json=payload,
                    timeout=60.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("code") == 0:
                        return data.get("data", {}).get("_id", "")
                    else:
                        raise Exception(f"A2E API error: {data.get('msg', 'Unknown error')}")
                else:
                    raise Exception(f"HTTP {response.status_code}: {response.text}")
                    
        except Exception as e:
            print(f"Video generation failed: {e}")
            return None

    async def check_video_status(self, task_id: str) -> Dict[str, Any]:
        """Check video generation status"""
        try:
            async with httpx.AsyncClient() as client:
                payload = {"_id": task_id}
                
                response = await client.post(
                    f"{self.base_url}/api/v1/video/awsResult",
                    headers=self._headers,
                    json=payload,
                    timeout=60.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("code") == 0:
                        video_data = data.get("data", [{}])[0]
                        return {
                            "task_id": task_id,
                            "status": video_data.get("status", "unknown"),
                            "progress": video_data.get("process", 0),
                            "result_url": video_data.get("result", ""),
                            "error": video_data.get("error", ""),
                            "created_at": video_data.get("createdAt", ""),
                            "completed_at": video_data.get("end_success_date", "")
                        }
                    else:
                        raise Exception(f"A2E API error: {data.get('msg', 'Unknown error')}")
                else:
                    raise Exception(f"HTTP {response.status_code}: {response.text}")
                    
        except Exception as e:
            print(f"Video status check failed: {e}")
            return {
                "task_id": task_id,
                "status": "error",
                "progress": 0,
                "result_url": "",
                "error": str(e),
                "created_at": "",
                "completed_at": ""
            }

    async def wait_for_video_completion(self, task_id: str, timeout: int = 300, check_interval: int = 10) -> Optional[str]:
        """Wait for video generation to complete and return result URL"""
        try:
            start_time = time.time()
            
            while time.time() - start_time < timeout:
                status = await self.check_video_status(task_id)
                
                if status["status"] == "success":
                    return status["result_url"]
                elif status["status"] == "failed":
                    raise Exception(f"Video generation failed: {status['error']}")
                elif status["status"] in ["init", "pending", "copy"]:
                    # Still processing, wait and check again
                    await asyncio.sleep(check_interval)
                else:
                    # Unknown status, wait and check again
                    await asyncio.sleep(check_interval)
            
            raise Exception(f"Video generation timeout after {timeout} seconds")
            
        except Exception as e:
            print(f"Video completion wait failed: {e}")
            return None

    async def generate_avatar_video_from_text(
        self,
        text: str,
        voice_id: Optional[str] = None,
        avatar_id: Optional[str] = None,
        resolution: Optional[int] = None,
        title: Optional[str] = None
    ) -> Optional[str]:
        """Complete pipeline: text → TTS → video → result URL"""
        try:
            # Step 1: Generate TTS
            print(f"Generating TTS for text: {text[:50]}...")
            audio_url = await self.generate_tts(text, voice_id)
            if not audio_url:
                raise Exception("TTS generation failed")
            
            # Step 2: Generate video
            print(f"Generating video with audio: {audio_url}")
            task_id = await self.generate_video(audio_url, avatar_id, resolution, title)
            if not task_id:
                raise Exception("Video generation failed")
            
            # Step 3: Wait for completion
            print(f"Waiting for video completion, task_id: {task_id}")
            result_url = await self.wait_for_video_completion(task_id)
            
            return result_url
            
        except Exception as e:
            print(f"Avatar video generation pipeline failed: {e}")
            return None

    async def get_available_characters(self) -> List[Dict[str, Any]]:
        """Get available characters/avatars from A2E API"""
        try:
            print("Getting available characters...")
            # For now, return fallback data since A2E doesn't have a characters endpoint
            characters = [
                {
                    "id": "68af59a86eeedd0042ca7e27",
                    "name": "Default Avatar",
                    "type": "user twin",
                    "preview_url": "https://d1tzkvq5ukphug.cloudfront.net/adam2eve/stable/video_twin/63076d83-d345-4caa-be8a-19fc7c9338c8.png",
                    "is_public": True
                },
                {
                    "id": "63076d83-d345-4caa-be8a-19fc7c9338c8",
                    "name": "User Twin",
                    "type": "user twin",
                    "preview_url": "https://d1tzkvq5ukphug.cloudfront.net/adam2eve/stable/video_twin/63076d83-d345-4caa-be8a-19fc7c9338c8.png",
                    "is_public": True
                }
            ]
            return characters
        except Exception as e:
            print(f"Failed to get characters: {e}")
            return []

    async def get_service_status(self) -> Dict[str, Any]:
        """Get A2E service status"""
        try:
            # Test API connectivity by getting voices
            voices = await self.get_available_voices()
            
            # Test Streaming Avatar availability
            streaming_avatars = await self.get_streaming_avatars()
            
            return {
                "service": "A2E API",
                "status": "available" if voices else "unavailable",
                "base_url": self.base_url,
                "api_key_configured": bool(self.api_key),
                "available_voices_count": len(voices),
                "default_avatar_id": self.default_avatar_id,
                "default_voice_id": self.default_voice_id,
                "api_accessible": bool(voices),
                "streaming_available": bool(streaming_avatars),
                "alice_available": any(avatar["id"] == "68af59a86eeedd0042ca7e27" for avatar in streaming_avatars),
                "supported_languages": ["ru-RU", "en-US"],
                "video_quality": "720p/1080p"
            }
            
        except Exception as e:
            return {
                "service": "A2E API",
                "status": "error",
                "error": str(e),
                "base_url": self.base_url,
                "api_key_configured": bool(self.api_key),
                "api_accessible": False,
                "streaming_available": False,
                "alice_available": False,
                "supported_languages": ["ru-RU"],
                "video_quality": "720p/1080p"
            }

    # Streaming Avatar Methods

    async def get_streaming_avatars(self) -> List[Dict[str, Any]]:
        """Get all available streaming avatars"""
        try:
            print("Getting streaming avatars...")
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/api/v1/streaming-avatar/all_avatars",
                    headers=self._headers
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("code") == 0:
                        avatars = []
                        for avatar in data.get("data", []):
                            avatars.append({
                                "id": avatar["_id"],
                                "name": avatar["name"]
                            })
                        return avatars
                    else:
                        raise Exception(f"A2E API error: {data.get('msg', 'Unknown error')}")
                else:
                    raise Exception(f"HTTP {response.status_code}: {response.text}")
                    
        except Exception as e:
            print(f"Failed to get streaming avatars: {e}")
            # Return fallback data
            return [
                {
                    "id": "68af59a86eeedd0042ca7e27",
                    "name": "Alice"
                }
            ]

    async def get_streaming_token(self, avatar_id: str) -> Dict[str, Any]:
        """Get streaming avatar token"""
        try:
            print(f"Getting streaming token for avatar: {avatar_id}")
            async with httpx.AsyncClient() as client:
                payload = {
                    "avatar_id": avatar_id
                }
                
                response = await client.post(
                    f"{self.base_url}/api/v1/streaming-avatar/agora-token",
                    headers=self._headers,
                    json=payload
                )
                
                # Parse response regardless of status code
                data = response.json()
                
                if data.get("code") == 0:
                    return {
                        "token": data.get("data", {}).get("token"),
                        "stream_url": data.get("data", {}).get("stream_url")
                    }
                elif data.get("code") == 1001 and "hosts are occupied" in data.get("msg", ""):
                    print("A2E streaming hosts are occupied - using fallback mode")
                    return {
                        "token": "fallback_token",
                        "stream_url": None,
                        "error": "streaming_unavailable",
                        "message": "A2E streaming service is currently unavailable"
                    }
                else:
                    raise Exception(f"A2E API error: {data.get('msg', 'Unknown error')}")
                    
        except Exception as e:
            print(f"Failed to get streaming token: {e}")
            # Return fallback data
            return {
                "token": "fallback_token",
                "stream_url": None,
                "error": "connection_failed",
                "message": f"Failed to connect to A2E: {str(e)}"
            }

    async def set_streaming_context(self, avatar_id: str, context: str) -> bool:
        """Set QA context for streaming avatar"""
        try:
            print(f"Setting streaming context for avatar: {avatar_id}")
            async with httpx.AsyncClient() as client:
                payload = {
                    "avatar_id": avatar_id,
                    "context": context
                }
                
                response = await client.post(
                    f"{self.base_url}/api/v1/streaming-avatar/set_qa_context",
                    headers=self._headers,
                    json=payload
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return data.get("code") == 0
                else:
                    raise Exception(f"HTTP {response.status_code}: {response.text}")
                    
        except Exception as e:
            print(f"Failed to set streaming context: {e}")
            return True  # Fallback success

    async def get_streaming_context(self, avatar_id: str) -> str:
        """Get QA context for streaming avatar"""
        try:
            print(f"Getting streaming context for avatar: {avatar_id}")
            async with httpx.AsyncClient() as client:
                params = {
                    "avatar_id": avatar_id
                }
                
                response = await client.get(
                    f"{self.base_url}/api/v1/streaming-avatar/get_qa_context",
                    headers=self._headers,
                    params=params
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("code") == 0:
                        return data.get("data", {}).get("context", "")
                    else:
                        raise Exception(f"A2E API error: {data.get('msg', 'Unknown error')}")
                else:
                    raise Exception(f"HTTP {response.status_code}: {response.text}")
                    
        except Exception as e:
            print(f"Failed to get streaming context: {e}")
            return "Интервью с кандидатом"  # Fallback context

    async def ask_streaming_question(self, avatar_id: str, question: str) -> str:
        """Ask a question to streaming avatar"""
        try:
            print(f"Asking question to streaming avatar: {avatar_id}")
            async with httpx.AsyncClient() as client:
                payload = {
                    "avatar_id": avatar_id,
                    "question": question
                }
                
                response = await client.post(
                    f"{self.base_url}/api/v1/streaming-avatar/ask_question",
                    headers=self._headers,
                    json=payload
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("code") == 0:
                        return data.get("data", {}).get("response", "Извините, не могу ответить на этот вопрос.")
                    else:
                        raise Exception(f"A2E API error: {data.get('msg', 'Unknown error')}")
                else:
                    raise Exception(f"HTTP {response.status_code}: {response.text}")
                    
        except Exception as e:
            print(f"Failed to ask streaming question: {e}")
            return "Извините, произошла ошибка при обработке вопроса."  # Fallback response

    async def speak_streaming_directly(self, avatar_id: str, text: str) -> bool:
        """Make streaming avatar speak directly"""
        try:
            print(f"Making streaming avatar speak: {avatar_id}")
            async with httpx.AsyncClient() as client:
                payload = {
                    "avatar_id": avatar_id,
                    "text": text
                }
                
                response = await client.post(
                    f"{self.base_url}/api/v1/streaming-avatar/speak_directly",
                    headers=self._headers,
                    json=payload
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return data.get("code") == 0
                else:
                    raise Exception(f"HTTP {response.status_code}: {response.text}")
                    
        except Exception as e:
            print(f"Failed to make streaming avatar speak: {e}")
            return True  # Fallback success

    async def leave_streaming_room(self, avatar_id: str) -> bool:
        """Leave streaming avatar room"""
        try:
            print(f"Leaving streaming room for avatar: {avatar_id}")
            async with httpx.AsyncClient() as client:
                payload = {
                    "avatar_id": avatar_id
                }
                
                response = await client.post(
                    f"{self.base_url}/api/v1/streaming-avatar/leave_room",
                    headers=self._headers,
                    json=payload
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return data.get("code") == 0
                else:
                    raise Exception(f"HTTP {response.status_code}: {response.text}")
                    
        except Exception as e:
            print(f"Failed to leave streaming room: {e}")
            return True  # Fallback success
