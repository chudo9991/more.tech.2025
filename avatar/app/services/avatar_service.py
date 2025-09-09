"""
Avatar generation service
"""
import asyncio
import tempfile
import os
import hashlib
import time
from typing import Dict, Any, Optional, List
import httpx
from PIL import Image
import io

from app.core.config import settings
from app.services.did_streaming_service import DIDStreamingService


class AvatarService:
    def __init__(self):
        print("AvatarService: Initializing...")
        self.cache = {}
        self._init_minio_client()
        print("AvatarService: Creating D-ID service...")
        self.did_service = DIDStreamingService()
        print("AvatarService: Initialization complete")

    def _init_minio_client(self):
        """Initialize MinIO client for avatar storage"""
        try:
            # In production, this would initialize MinIO client
            # For now, we'll use local file storage
            self.storage_dir = "/tmp/avatars"
            os.makedirs(self.storage_dir, exist_ok=True)
        except Exception as e:
            print(f"Failed to initialize storage: {e}")

    async def generate_avatar(
        self,
        session_id: str,
        style: str = "professional",
        gender: Optional[str] = None,
        age_range: Optional[str] = None,
        profession: Optional[str] = None,
        custom_prompt: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate avatar for interview session"""
        try:
            # Check cache first
            cache_key = self._generate_cache_key(session_id, style, gender, age_range, profession)
            if cache_key in self.cache:
                return self.cache[cache_key]

            # Generate avatar using AI model
            avatar_data = await self._generate_avatar_image(
                style, gender, age_range, profession, custom_prompt
            )
            
            # Save avatar and get URL
            avatar_url = await self._save_avatar(avatar_data, session_id, cache_key)
            
            result = {
                "avatar_url": avatar_url,
                "session_id": session_id,
                "style": style,
                "metadata": {
                    "gender": gender,
                    "age_range": age_range,
                    "profession": profession,
                    "generated_at": asyncio.get_event_loop().time()
                }
            }
            
            # Cache result
            self.cache[cache_key] = result
            
            return result
            
        except Exception as e:
            raise Exception(f"Avatar generation failed: {str(e)}")

    async def update_avatar_emotion(
        self,
        session_id: str,
        emotion: str = "neutral",
        expression: Optional[str] = None
    ) -> Dict[str, Any]:
        """Update avatar emotion/expression"""
        try:
            # Generate new avatar with updated emotion
            prompt = self._create_emotion_prompt(emotion, expression)
            
            avatar_data = await self._generate_avatar_image(
                style="professional",
                custom_prompt=prompt
            )
            
            # Save updated avatar
            avatar_url = await self._save_avatar(
                avatar_data, 
                session_id, 
                f"{session_id}_emotion_{emotion}"
            )
            
            return {
                "avatar_url": avatar_url,
                "session_id": session_id,
                "emotion": emotion,
                "metadata": {
                    "expression": expression,
                    "updated_at": asyncio.get_event_loop().time()
                }
            }
            
        except Exception as e:
            raise Exception(f"Avatar emotion update failed: {str(e)}")

    def _generate_cache_key(
        self,
        session_id: str,
        style: str,
        gender: Optional[str],
        age_range: Optional[str],
        profession: Optional[str]
    ) -> str:
        """Generate cache key for avatar"""
        content = f"{session_id}_{style}_{gender}_{age_range}_{profession}"
        return hashlib.md5(content.encode()).hexdigest()

    async def _generate_avatar_image(
        self,
        style: str,
        gender: Optional[str] = None,
        age_range: Optional[str] = None,
        profession: Optional[str] = None,
        custom_prompt: Optional[str] = None
    ) -> bytes:
        """Generate avatar image using AI model"""
        try:
            # Create prompt for avatar generation
            prompt = self._create_avatar_prompt(
                style, gender, age_range, profession, custom_prompt
            )
            
            # In production, this would call a real AI image generation API
            # For now, we'll create a placeholder image
            avatar_data = await self._create_placeholder_avatar(prompt)
            
            return avatar_data
            
        except Exception as e:
            print(f"Avatar generation failed: {e}")
            # Return default avatar
            return await self._create_default_avatar()

    def _create_avatar_prompt(
        self,
        style: str,
        gender: Optional[str] = None,
        age_range: Optional[str] = None,
        profession: Optional[str] = None,
        custom_prompt: Optional[str] = None
    ) -> str:
        """Create prompt for avatar generation"""
        base_prompt = f"Professional {style} portrait"
        
        if gender:
            base_prompt += f", {gender}"
        if age_range:
            base_prompt += f", {age_range} years old"
        if profession:
            base_prompt += f", {profession}"
        
        if custom_prompt:
            base_prompt += f", {custom_prompt}"
        
        base_prompt += ", high quality, professional lighting, neutral background"
        
        return base_prompt

    def _create_emotion_prompt(self, emotion: str, expression: Optional[str] = None) -> str:
        """Create prompt for emotion update"""
        emotion_map = {
            "neutral": "neutral expression",
            "positive": "friendly smile",
            "concerned": "slightly concerned expression",
            "excited": "enthusiastic expression"
        }
        
        emotion_prompt = emotion_map.get(emotion, "neutral expression")
        
        if expression:
            emotion_prompt += f", {expression}"
        
        return f"Professional portrait with {emotion_prompt}, high quality"

    async def _create_placeholder_avatar(self, prompt: str) -> bytes:
        """Create placeholder avatar image"""
        try:
            # Create a simple colored rectangle as placeholder
            width, height = 512, 512
            
            # Create image with gradient background
            image = Image.new('RGB', (width, height), color='#4A90E2')
            
            # Convert to bytes
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()
            
            return img_byte_arr
            
        except Exception as e:
            print(f"Placeholder avatar creation failed: {e}")
            return await self._create_default_avatar()

    async def _create_default_avatar(self) -> bytes:
        """Create default avatar image"""
        try:
            # Create a simple default avatar
            width, height = 512, 512
            image = Image.new('RGB', (width, height), color='#E0E0E0')
            
            # Convert to bytes
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()
            
            return img_byte_arr
            
        except Exception as e:
            print(f"Default avatar creation failed: {e}")
            # Return minimal image
            return b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\tpHYs\x00\x00\x0b\x13\x00\x00\x0b\x13\x01\x00\x9a\x9c\x18\x00\x00\x00\x0cIDATx\x9cc```\x00\x00\x00\x04\x00\x01\xf5\xd7\xd4\xc2\x00\x00\x00\x00IEND\xaeB`\x82'

    async def _save_avatar(self, avatar_data: bytes, session_id: str, cache_key: str) -> str:
        """Save avatar to storage and return URL"""
        try:
            # Create filename
            filename = f"avatar_{session_id}_{cache_key}.png"
            filepath = os.path.join(self.storage_dir, filename)
            
            # Save avatar
            with open(filepath, 'wb') as f:
                f.write(avatar_data)
            
            # In production, this would upload to MinIO/S3 and return presigned URL
            # For now, return local file path
            return f"file://{filepath}"
            
        except Exception as e:
            print(f"Avatar save failed: {e}")
            return ""

    async def get_avatar_url(self, session_id: str) -> Optional[str]:
        """Get avatar URL for session"""
        try:
            # Look for existing avatar
            for cache_key, result in self.cache.items():
                if result["session_id"] == session_id:
                    return result["avatar_url"]
            
            return None
            
        except Exception as e:
            print(f"Avatar URL retrieval failed: {e}")
            return None

    # D-ID API Integration Methods
    
    async def get_available_voices(self) -> List[Dict[str, Any]]:
        """Get available voices for D-ID"""
        return [
            {
                "id": "Dimf6681ffz3PTVPPAEX",
                "name": "D-ID Default Voice",
                "provider": "elevenlabs",
                "language": "ru-RU"
            }
        ]

    async def generate_tts(self, text: str, voice_id: Optional[str] = None, speech_rate: Optional[float] = None) -> Optional[str]:
        """Generate TTS using D-ID (via streaming)"""
        avatar_result = await self.did_service.create_avatar()
        if not avatar_result.get("success"):
            return None
        
        avatar_id = avatar_result["avatar_id"]
        token_result = await self.did_service.get_streaming_token(avatar_id)
        if not token_result.get("success"):
            return None
        
        speak_success = await self.did_service.speak_streaming_directly(avatar_id, text)
        return token_result.get("stream_url") if speak_success else None

    async def generate_avatar_video(
        self,
        text: str,
        session_id: str,
        voice_id: Optional[str] = None,
        avatar_id: Optional[str] = None,
        resolution: Optional[int] = None
    ) -> Dict[str, Any]:
        """Generate avatar video using D-ID"""
        try:
            # Create avatar
            avatar_result = await self.did_service.create_avatar()
            if not avatar_result.get("success"):
                return None
            
            did_avatar_id = avatar_result["avatar_id"]
            
            # Get streaming session
            token_result = await self.did_service.get_streaming_token(did_avatar_id)
            if not token_result.get("success"):
                return None
            
            # Make avatar speak
            speak_success = await self.did_service.speak_streaming_directly(did_avatar_id, text)
            if speak_success:
                result = {
                    "video_url": token_result.get("stream_url"),
                    "session_id": session_id,
                    "text": text,
                    "voice_id": voice_id or "Dimf6681ffz3PTVPPAEX",
                    "avatar_id": did_avatar_id,
                    "resolution": resolution or 720,
                    "generated_at": asyncio.get_event_loop().time()
                }
                
                # Cache result
                cache_key = f"video_{session_id}_{hash(text)}"
                self.cache[cache_key] = result
                
                return result
            else:
                raise Exception("Video generation failed")
                
        except Exception as e:
            raise Exception(f"Avatar video generation failed: {str(e)}")

    async def check_video_status(self, task_id: str) -> Dict[str, Any]:
        """Check D-ID talk status"""
        return await self.did_service.get_talk_status(task_id)

    async def get_did_service_status(self) -> Dict[str, Any]:
        """Get D-ID service status"""
        return await self.did_service.get_streaming_status()
