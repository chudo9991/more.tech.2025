"""
Speech synthesis service for TTS
"""
import asyncio
import tempfile
import os
import hashlib
from typing import Dict, Any, Optional
from TTS.api import TTS
import numpy as np
from pydub import AudioSegment
import librosa

from app.core.config import settings


class SynthesizeService:
    def __init__(self):
        self.tts_model = None
        self.cache = {}
        self._load_model()

    def _load_model(self):
        """Load TTS model"""
        try:
            # Initialize TTS model
            self.tts_model = TTS(settings.TTS_MODEL)
        except Exception as e:
            print(f"Error loading TTS model: {e}")

    async def synthesize(
        self,
        text: str,
        voice: str = "default",
        speaker: str = "default",
        language: str = "ru"
    ) -> Dict[str, Any]:
        """Synthesize text to speech"""
        try:
            # Check cache first
            cache_key = self._generate_cache_key(text, voice, speaker, language)
            if settings.ENABLE_AUDIO_CACHE and cache_key in self.cache:
                return self.cache[cache_key]

            # Generate audio
            audio_data = await self._generate_audio(text, voice, speaker, language)
            
            # Save to file and get URL
            audio_url = await self._save_audio(audio_data, cache_key)
            
            # Calculate duration
            duration_ms = self._calculate_duration(audio_data)
            
            result = {
                "audio_url": audio_url,
                "duration_ms": duration_ms,
                "text_length": len(text)
            }
            
            # Cache result
            if settings.ENABLE_AUDIO_CACHE:
                self.cache[cache_key] = result
            
            return result
            
        except Exception as e:
            raise Exception(f"Speech synthesis failed: {str(e)}")

    def _generate_cache_key(self, text: str, voice: str, speaker: str, language: str) -> str:
        """Generate cache key for audio"""
        content = f"{text}_{voice}_{speaker}_{language}"
        return hashlib.md5(content.encode()).hexdigest()

    async def _generate_audio(
        self, 
        text: str, 
        voice: str, 
        speaker: str, 
        language: str
    ) -> np.ndarray:
        """Generate audio using TTS model"""
        if self.tts_model is None:
            # Fallback: generate silence
            return np.zeros(16000)  # 1 second of silence
        
        try:
            # Synthesize speech
            audio_data = self.tts_model.tts(
                text=text,
                speaker=speaker,
                language=language
            )
            
            # Convert to numpy array if needed
            if isinstance(audio_data, list):
                audio_data = np.array(audio_data)
            
            return audio_data
            
        except Exception as e:
            print(f"TTS generation failed: {e}")
            # Return silence as fallback
            return np.zeros(16000)

    async def _save_audio(self, audio_data: np.ndarray, cache_key: str) -> str:
        """Save audio to file and return URL"""
        try:
            # Create temporary file
            temp_dir = "/tmp/tts_cache"
            os.makedirs(temp_dir, exist_ok=True)
            
            filename = f"{cache_key}.wav"
            filepath = os.path.join(temp_dir, filename)
            
            # Save audio as WAV
            import soundfile as sf
            sf.write(filepath, audio_data, 22050)
            
            # In production, this would upload to MinIO/S3
            # For now, return local file path
            return f"file://{filepath}"
            
        except Exception as e:
            print(f"Audio save failed: {e}")
            return ""

    def _calculate_duration(self, audio_data: np.ndarray) -> int:
        """Calculate audio duration in milliseconds"""
        try:
            # Assuming 22.05kHz sample rate
            sample_rate = 22050
            duration_s = len(audio_data) / sample_rate
            return int(duration_s * 1000)
        except Exception as e:
            print(f"Duration calculation failed: {e}")
            return 1000  # Default 1 second

    async def pregenerate_questions(self, questions: list) -> Dict[str, str]:
        """Pregenerate audio for common questions"""
        results = {}
        
        for question in questions:
            try:
                result = await self.synthesize(
                    text=question["text"],
                    voice=question.get("voice", "default"),
                    language=question.get("language", "ru")
                )
                results[question["id"]] = result["audio_url"]
            except Exception as e:
                print(f"Failed to pregenerate question {question['id']}: {e}")
        
        return results
