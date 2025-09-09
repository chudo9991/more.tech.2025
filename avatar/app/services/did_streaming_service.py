"""
D-ID Streaming Avatar Service
Provides D-ID streaming avatar functionality with interface compatible to A2E service
"""
import asyncio
import time
from typing import Dict, Any, List, Optional
import httpx
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)


class DIDStreamingService:
    """D-ID Streaming Avatar Service"""

    def __init__(self):
        """Initialize D-ID streaming service with configuration settings"""
        self.base_url = settings.DID_BASE_URL
        self.api_key = settings.DID_API_KEY
        self.default_avatar_image = settings.DID_DEFAULT_AVATAR_IMAGE
        self.default_presenter_id = settings.DID_DEFAULT_PRESENTER_ID
        self.default_agent_id = settings.DID_DEFAULT_AGENT_ID
        self.default_voice = settings.DID_DEFAULT_VOICE

        logger.info("D-ID Streaming Service initialized:")
        logger.info(f"  Base URL: {self.base_url}")
        logger.info(
            f"  API Key: {self.api_key[:20]}..." if self.api_key else "  API Key: None")
        logger.info(f"  Default Avatar Image: {self.default_avatar_image}")
        logger.info(f"  Default Presenter ID: {self.default_presenter_id}")
        logger.info(f"  Default Agent ID: {self.default_agent_id}")
        logger.info(f"  Default Voice: {self.default_voice}")

        # HTTP headers for D-ID API
        self._headers = {
            "Authorization": f"Basic {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        # Store active sessions
        self._active_sessions: Dict[str, Dict[str, Any]] = {}

    async def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        timeout: float = 30.0
    ) -> Dict[str, Any]:
        """Make HTTP request to D-ID API with error handling"""
        url = f"{self.base_url}{endpoint}"

        try:
            async with httpx.AsyncClient() as client:
                logger.debug(f"Making {method} request to {url}")

                if method.upper() == "GET":
                    response = await client.get(
                        url,
                        headers=self._headers,
                        timeout=timeout
                    )
                elif method.upper() == "POST":
                    response = await client.post(
                        url,
                        headers=self._headers,
                        json=data,
                        timeout=timeout
                    )
                elif method.upper() == "DELETE":
                    response = await client.delete(
                        url,
                        headers=self._headers,
                        timeout=timeout
                    )
                else:
                    raise ValueError(f"Unsupported HTTP method: {method}")

                # Log response details
                logger.debug(f"Response status: {response.status_code}")
                logger.debug(f"Response headers: {dict(response.headers)}")

                # Parse JSON response
                if response.headers.get("content-type", "").startswith("application/json"):
                    response_data = response.json()
                else:
                    response_data = {"text": response.text}

                # Check for HTTP errors
                if response.status_code >= 400:
                    error_msg = response_data.get("message", response.text)
                    logger.error(
                        f"D-ID API error {response.status_code}: {error_msg}")
                    raise Exception(
                        f"D-ID API error {response.status_code}: {error_msg}")

                return response_data

        except httpx.TimeoutException:
            logger.error(f"Timeout making request to {url}")
            raise Exception(f"Request timeout to D-ID API")
        except httpx.RequestError as e:
            logger.error(f"Request error to {url}: {e}")
            raise Exception(f"Network error connecting to D-ID API: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error making request to {url}: {e}")
            raise

    async def _upload_image_to_did(self, image_url: str) -> str:
        """Upload image to D-ID and return image ID"""
        try:
            logger.info(f"Uploading image to D-ID: {image_url}")

            data = {
                "source_url": image_url
            }

            response = await self._make_request("POST", "/images", data)

            image_id = response.get("id")
            if not image_id:
                raise Exception("No image ID returned from D-ID")

            logger.info(f"Image uploaded successfully, ID: {image_id}")
            return image_id

        except Exception as e:
            logger.error(f"Failed to upload image to D-ID: {e}")
            raise Exception(f"Failed to upload image: {str(e)}")

    async def get_streaming_status(self) -> Dict[str, Any]:
        """Get D-ID streaming service status"""
        try:
            # For D-ID, we just check if we have valid configuration
            # No need to make API call for status check
            if not self.api_key or not self.base_url:
                raise Exception("D-ID API configuration is missing")

            return {
                "service": "D-ID Streaming Avatar",
                "status": "available",
                "streaming_available": True,
                "default_avatar_image": self.default_avatar_image,
                "default_voice": self.default_voice,
                "active_sessions": len(self._active_sessions)
            }

        except Exception as e:
            logger.error(f"D-ID service status check failed: {e}")
            return {
                "service": "D-ID Streaming Avatar",
                "status": "error",
                "error": str(e),
                "streaming_available": False,
                "active_sessions": 0
            }

    def _generate_session_id(self, avatar_id: str) -> str:
        """Generate unique session ID for avatar"""
        timestamp = int(time.time())
        return f"did_session_{avatar_id}_{timestamp}"

    async def create_avatar(self, image_url: Optional[str] = None) -> Dict[str, Any]:
        """
        Create avatar in D-ID system

        Args:
            image_url: URL of the image to use for avatar. If None, uses default image.

        Returns:
            Dict containing avatar creation result with avatar_id
        """
        try:
            # Use provided image or default
            avatar_image_url = image_url or self.default_avatar_image

            logger.info(f"Creating D-ID avatar with image: {avatar_image_url}")

            # Upload image to D-ID first
            image_id = await self._upload_image_to_did(avatar_image_url)

            # For D-ID, the avatar is essentially the uploaded image
            # We'll use the image_id as avatar_id for consistency
            avatar_id = image_id

            logger.info(f"Avatar created successfully with ID: {avatar_id}")

            return {
                "success": True,
                "avatar_id": avatar_id,
                "image_id": image_id,
                "image_url": avatar_image_url,
                "voice": self.default_voice,
                "message": "Avatar created successfully"
            }

        except Exception as e:
            logger.error(f"Failed to create D-ID avatar: {e}")
            return {
                "success": False,
                "error": "avatar_creation_failed",
                "message": f"Failed to create avatar: {str(e)}",
                "avatar_id": None
            }

    async def get_available_streaming_avatars(self) -> List[Dict[str, Any]]:
        """
        Get available streaming avatars (D-ID compatible)
        For D-ID, we return the default avatar configuration
        """
        try:
            # For D-ID, we can create avatars on-demand with any image
            # Return default avatar info
            return [
                {
                    "id": "did_default_avatar",
                    "name": "D-ID Default Avatar",
                    "type": "streaming",
                    "preview_url": self.default_avatar_image,
                    "is_available": True,
                    "voice": self.default_voice
                }
            ]

        except Exception as e:
            logger.error(f"Failed to get D-ID streaming avatars: {e}")
            return []

    async def get_streaming_token(self, avatar_id: str) -> Dict[str, Any]:
        """
        Create D-ID streaming session

        Args:
            avatar_id: ID of the avatar

        Returns:
            Dict containing session info compatible with A2E interface
        """
        try:
            logger.info(f"Creating D-ID streaming session for avatar: {avatar_id}")

            # Create D-ID streaming session
            stream_data = {
                "source_url": self.default_avatar_image,
                "config": {
                    "stitch": True,
                    "fluent": True
                }
            }

            response = await self._make_request("POST", "/talks/streams", stream_data)

            stream_id = response.get("id")
            stream_url = response.get("stream_url")
            session_id = response.get("session_id")

            if not stream_id:
                raise Exception("No stream ID returned from D-ID API")

            # Store session info
            session_info = {
                "avatar_id": avatar_id,
                "stream_id": stream_id,
                "stream_url": stream_url,
                "session_id": session_id,
                "created_at": time.time(),
                "ready": True
            }

            self._active_sessions[avatar_id] = session_info

            logger.info(f"D-ID streaming session created successfully: {stream_id}")

            # Return A2E-compatible response
            return {
                "success": True,
                "token": stream_id,
                "stream_url": stream_url,
                "room_id": stream_id,
                "avatar_id": avatar_id,
                "session_id": session_id,
                "stream_id": stream_id
            }

        except Exception as e:
            logger.error(f"Failed to create D-ID streaming session: {e}")
            return {
                "success": False,
                "error": "session_failed",
                "message": f"Failed to create session: {str(e)}",
                "fallback_mode": True,
                "avatar_id": avatar_id
            }

    async def speak_streaming_directly(self, avatar_id: str, text: str) -> bool:
        """
        Send text to D-ID streaming session

        Args:
            avatar_id: ID of the avatar
            text: Text for avatar to speak

        Returns:
            bool: True if text was sent successfully, False otherwise
        """
        try:
            logger.info(f"Sending text to D-ID stream for avatar {avatar_id}: {text[:50]}...")

            # Get active session for this avatar
            session_info = self._active_sessions.get(avatar_id)
            if not session_info:
                raise Exception(f"No active session found for avatar {avatar_id}")

            stream_id = session_info.get("stream_id")
            if not stream_id:
                raise Exception(f"No stream ID found for avatar {avatar_id}")

            # Prepare streaming data for D-ID
            speak_data = {
                "script": {
                    "type": "text",
                    "input": text,
                    "provider": {
                        "type": "elevenlabs",
                        "voice_id": self.default_voice
                    }
                },
                "config": {
                    "stitch": True,
                    "fluent": True
                },
                "session_id": session_info.get("session_id")
            }

            # Send text to streaming session
            response = await self._make_request("POST", f"/talks/streams/{stream_id}", speak_data, timeout=30.0)

            # Store speak info in session
            session_info["last_speak_text"] = text
            session_info["last_speak_time"] = time.time()

            logger.info(f"Text sent to D-ID stream successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to send text to D-ID stream for avatar {avatar_id}: {e}")
            return False

    async def ask_streaming_question(self, avatar_id: str, question: str) -> str:
        """
        Ask a question to streaming avatar (D-ID compatible)
        For D-ID, this is essentially the same as speak_streaming_directly
        """
        try:
            logger.info(
                f"Processing question for D-ID avatar {avatar_id}: {question[:50]}...")

            # For D-ID, we just make the avatar speak the question
            # In a real implementation, this might involve LLM processing
            success = await self.speak_streaming_directly(avatar_id, question)

            if success:
                return "Вопрос передан аватару для произношения"
            else:
                return "Не удалось передать вопрос аватару"

        except Exception as e:
            logger.error(
                f"Failed to process question for D-ID avatar {avatar_id}: {e}")
            return "Извините, не удалось обработать вопрос"

    async def set_streaming_context(self, avatar_id: str, context: str) -> bool:
        """
        Set context for streaming avatar (D-ID compatible)
        For D-ID, we store context in session info
        """
        try:
            logger.info(f"Setting context for D-ID avatar {avatar_id}")

            session_info = self._active_sessions.get(avatar_id)
            if session_info:
                session_info["context"] = context
                logger.info("Context set successfully")
                return True
            else:
                logger.warning(
                    f"No active session found for avatar {avatar_id}")
                return False

        except Exception as e:
            logger.error(
                f"Failed to set context for D-ID avatar {avatar_id}: {e}")
            return False

    async def get_streaming_context(self, avatar_id: str) -> str:
        """
        Get context for streaming avatar (D-ID compatible)
        """
        try:
            session_info = self._active_sessions.get(avatar_id)
            if session_info and "context" in session_info:
                return session_info["context"]
            else:
                return "Интервью с кандидатом"  # Default context

        except Exception as e:
            logger.error(
                f"Failed to get context for D-ID avatar {avatar_id}: {e}")
            return "Интервью с кандидатом"  # Fallback context

    async def leave_streaming_room(self, avatar_id: str) -> bool:
        """
        Leave D-ID streaming session and cleanup resources

        Args:
            avatar_id: ID of the avatar

        Returns:
            bool: True if session was closed successfully, False otherwise
        """
        try:
            logger.info(f"Closing D-ID streaming session for avatar {avatar_id}")

            # Get active session for this avatar
            session_info = self._active_sessions.get(avatar_id)
            if not session_info:
                logger.warning(f"No active session found for avatar {avatar_id}")
                return True  # Consider it success if no session exists

            stream_id = session_info.get("stream_id")
            if stream_id:
                try:
                    # Delete D-ID streaming session
                    await self._make_request("DELETE", f"/talks/streams/{stream_id}", timeout=30.0)
                    logger.info(f"D-ID streaming session {stream_id} deleted successfully")
                except Exception as e:
                    logger.warning(f"Failed to delete D-ID streaming session {stream_id}: {e}")

            # Clean up local session data
            if avatar_id in self._active_sessions:
                del self._active_sessions[avatar_id]
                logger.info(f"Local session data cleaned up for avatar {avatar_id}")

            return True

        except Exception as e:
            logger.error(f"Failed to leave D-ID streaming session for avatar {avatar_id}: {e}")

            # Try to cleanup local data even if error occurred
            try:
                if avatar_id in self._active_sessions:
                    del self._active_sessions[avatar_id]
                    logger.info("Local session data cleaned up despite error")
            except Exception as cleanup_error:
                logger.error(f"Failed to cleanup local session data: {cleanup_error}")

            return True  # Return True for fallback compatibility

    async def get_talk_status(self, talk_id: str) -> Dict[str, Any]:
        """
        Get status of D-ID talk (video generation)

        Args:
            talk_id: ID of the talk

        Returns:
            Dict containing talk status and result URL if ready
        """
        try:
            logger.info(f"Getting D-ID talk status: {talk_id}")

            # Get talk status from D-ID API
            response = await self._make_request("GET", f"/talks/{talk_id}", timeout=30.0)

            status = response.get("status")
            result_url = response.get("result_url")

            logger.info(f"Talk {talk_id} status: {status}")

            return {
                "success": True,
                "talk_id": talk_id,
                "status": status,
                "result_url": result_url,
                "response": response
            }

        except Exception as e:
            logger.error(f"Failed to get talk status {talk_id}: {e}")
            return {
                "success": False,
                "talk_id": talk_id,
                "error": str(e)
            }

    async def get_last_video_url(self, avatar_id: str) -> str:
        """
        Get the URL of the last generated video for avatar

        Args:
            avatar_id: ID of the avatar

        Returns:
            str: URL of the last video or None if not available
        """
        try:
            session_info = self._active_sessions.get(avatar_id)
            if not session_info or "last_talk_id" not in session_info:
                return None

            talk_id = session_info["last_talk_id"]
            status_info = await self.get_talk_status(talk_id)

            if status_info.get("success") and status_info.get("status") == "done":
                return status_info.get("result_url")

            return None

        except Exception as e:
            logger.error(f"Failed to get last video URL for avatar {avatar_id}: {e}")
            return None

    def cleanup_expired_sessions(self, max_age_hours: int = 2) -> int:
        """
        Cleanup expired sessions (utility method)

        Args:
            max_age_hours: Maximum age of sessions in hours before cleanup

        Returns:
            int: Number of sessions cleaned up
        """
        try:
            current_time = time.time()
            max_age_seconds = max_age_hours * 3600
            expired_sessions = []

            for avatar_id, session_info in self._active_sessions.items():
                session_age = current_time - \
                    session_info.get("created_at", current_time)
                if session_age > max_age_seconds:
                    expired_sessions.append(avatar_id)

            # Cleanup expired sessions
            cleaned_count = 0
            for avatar_id in expired_sessions:
                try:
                    # Use asyncio to run the async cleanup method
                    asyncio.create_task(self.leave_streaming_room(avatar_id))
                    cleaned_count += 1
                except Exception as e:
                    logger.error(
                        f"Failed to cleanup expired session {avatar_id}: {e}")

            if cleaned_count > 0:
                logger.info(
                    f"Cleaned up {cleaned_count} expired D-ID sessions")

            return cleaned_count

        except Exception as e:
            logger.error(f"Failed to cleanup expired sessions: {e}")
            return 0
