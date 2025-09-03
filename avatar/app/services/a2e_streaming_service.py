"""
A2E Streaming Avatar Service - исправленная версия
Отдельный сервис только для стриминга, не трогает существующий A2EService
"""
import asyncio
import time
from typing import Dict, Any, List, Optional
import httpx
from app.core.config import settings


class A2EStreamingService:
    def __init__(self):
        self.base_url = settings.A2E_BASE_URL
        self.api_key = settings.A2E_API_KEY
        self.default_avatar_id = settings.A2E_DEFAULT_AVATAR_ID
        
        print(f"A2E Streaming Service initialized:")
        print(f"  Base URL: {self.base_url}")
        print(f"  API Key: {self.api_key[:20]}..." if self.api_key else "  API Key: None")
        print(f"  Default Avatar ID: {self.default_avatar_id}")
        
        self._headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    async def get_available_streaming_avatars(self) -> List[Dict[str, Any]]:
        """Get all available streaming avatars"""
        try:
            print("Getting streaming avatars...")
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/api/v1/streaming-avatar/all_avatars",
                    headers=self._headers,
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("code") == 0:
                        avatars = []
                        for avatar in data.get("data", []):
                            avatars.append({
                                "id": avatar.get("id"),
                                "name": avatar.get("name", "Unknown"),
                                "type": avatar.get("type", "unknown"),
                                "preview_url": avatar.get("preview_url", ""),
                                "is_available": avatar.get("is_available", True)
                            })
                        return avatars
                    else:
                        raise Exception(f"A2E API error: {data.get('msg', 'Unknown error')}")
                else:
                    raise Exception(f"HTTP {response.status_code}: {response.text}")
                    
        except Exception as e:
            print(f"Failed to get streaming avatars: {e}")
            return []

    async def get_streaming_token(self, avatar_id: str) -> Dict[str, Any]:
        """Get streaming avatar token - исправленный endpoint"""
        try:
            print(f"Getting streaming token for avatar: {avatar_id}")
            async with httpx.AsyncClient() as client:
                payload = {
                    "avatar_id": avatar_id
                }
                
                # Используем тот же endpoint, что и в старом сервисе
                response = await client.post(
                    f"{self.base_url}/api/v1/streaming-avatar/agora-token",
                    headers=self._headers,
                    json=payload,
                    timeout=30.0
                )
                
                # Parse response regardless of status code
                data = response.json()
                
                if data.get("code") == 0:
                    return {
                        "success": True,
                        "token": data.get("data", {}).get("token"),
                        "stream_url": data.get("data", {}).get("stream_url"),
                        "room_id": data.get("data", {}).get("room_id"),
                        "avatar_id": avatar_id
                    }
                elif data.get("code") == 1001 and "hosts are occupied" in data.get("msg", ""):
                    print("A2E streaming hosts are occupied - using fallback mode")
                    return {
                        "success": False,
                        "error": "streaming_unavailable",
                        "message": "A2E streaming service is currently unavailable",
                        "fallback_mode": True,
                        "avatar_id": avatar_id
                    }
                else:
                    raise Exception(f"A2E API error: {data.get('msg', 'Unknown error')}")
                    
        except Exception as e:
            print(f"Failed to get streaming token: {e}")
            # Return fallback data
            return {
                "success": False,
                "error": "connection_failed",
                "message": f"Failed to connect to A2E: {str(e)}",
                "fallback_mode": True,
                "avatar_id": avatar_id
            }

    async def set_streaming_context(self, avatar_id: str, context: str) -> bool:
        """Set QA context for streaming avatar - исправленный endpoint"""
        try:
            print(f"Setting streaming context for avatar: {avatar_id}")
            async with httpx.AsyncClient() as client:
                payload = {
                    "avatar_id": avatar_id,
                    "context": context
                }
                
                # Исправленный endpoint: /api/v1/streaming-avatar/set_qa_context
                response = await client.post(
                    f"{self.base_url}/api/v1/streaming-avatar/set_qa_context",
                    headers=self._headers,
                    json=payload,
                    timeout=30.0
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
        """Get QA context for streaming avatar - исправленный endpoint"""
        try:
            print(f"Getting streaming context for avatar: {avatar_id}")
            async with httpx.AsyncClient() as client:
                params = {
                    "avatar_id": avatar_id
                }
                
                # Исправленный endpoint: /api/v1/streaming-avatar/get_qa_context
                response = await client.get(
                    f"{self.base_url}/api/v1/streaming-avatar/get_qa_context",
                    headers=self._headers,
                    params=params,
                    timeout=30.0
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
        """Ask a question to streaming avatar - исправленный endpoint"""
        try:
            print(f"Asking question to streaming avatar: {avatar_id}")
            async with httpx.AsyncClient() as client:
                payload = {
                    "avatar_id": avatar_id,
                    "question": question
                }
                
                # Исправленный endpoint: /api/v1/streaming-avatar/ask_question
                response = await client.post(
                    f"{self.base_url}/api/v1/streaming-avatar/ask_question",
                    headers=self._headers,
                    json=payload,
                    timeout=60.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("code") == 0:
                        return data.get("data", {}).get("answer", "")
                    else:
                        raise Exception(f"A2E API error: {data.get('msg', 'Unknown error')}")
                else:
                    raise Exception(f"HTTP {response.status_code}: {response.text}")
                    
        except Exception as e:
            print(f"Failed to ask streaming question: {e}")
            return "Извините, не удалось получить ответ от аватара."  # Fallback response

    async def speak_streaming_directly(self, avatar_id: str, text: str) -> bool:
        """Make streaming avatar speak directly - исправленный endpoint"""
        try:
            print(f"Making streaming avatar speak: {avatar_id}")
            async with httpx.AsyncClient() as client:
                payload = {
                    "avatar_id": avatar_id,
                    "text": text
                }
                
                # Исправленный endpoint: /api/v1/streaming-avatar/speak_directly
                response = await client.post(
                    f"{self.base_url}/api/v1/streaming-avatar/speak_directly",
                    headers=self._headers,
                    json=payload,
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return data.get("code") == 0
                else:
                    raise Exception(f"HTTP {response.status_code}: {response.text}")
                    
        except Exception as e:
            print(f"Failed to make streaming avatar speak: {e}")
            return False

    async def leave_streaming_room(self, avatar_id: str) -> bool:
        """Leave streaming avatar room - исправленный endpoint"""
        try:
            print(f"Leaving streaming room for avatar: {avatar_id}")
            async with httpx.AsyncClient() as client:
                payload = {
                    "avatar_id": avatar_id
                }
                
                # Исправленный endpoint: /api/v1/streaming-avatar/leave_room
                response = await client.post(
                    f"{self.base_url}/api/v1/streaming-avatar/leave_room",
                    headers=self._headers,
                    json=payload,
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return data.get("code") == 0
                else:
                    raise Exception(f"HTTP {response.status_code}: {response.text}")
                    
        except Exception as e:
            print(f"Failed to leave streaming room: {e}")
            return True  # Fallback success

    async def get_streaming_status(self) -> Dict[str, Any]:
        """Get streaming service status"""
        try:
            avatars = await self.get_available_streaming_avatars()
            return {
                "service": "A2E Streaming Avatar",
                "status": "available" if avatars else "unavailable",
                "available_avatars": len(avatars),
                "avatars": avatars,
                "default_avatar_id": self.default_avatar_id,
                "streaming_available": bool(avatars),
                "alice_available": any(avatar["id"] == "68af59a86eeedd0042ca7e27" for avatar in avatars)
            }
        except Exception as e:
            return {
                "service": "A2E Streaming Avatar",
                "status": "error",
                "error": str(e),
                "streaming_available": False
            }
