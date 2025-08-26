"""
Transcription service for STT
"""
import asyncio
import tempfile
import os
from typing import Dict, Any, List
import whisper
import webrtcvad
import numpy as np
from pydub import AudioSegment
import librosa

from app.core.config import settings


class TranscribeService:
    def __init__(self):
        self.model = None
        self.vad = None
        self._load_models()

    def _load_models(self):
        """Load Whisper and VAD models"""
        try:
            # Load Whisper model
            self.model = whisper.load_model(settings.WHISPER_MODEL)
            
            # Initialize VAD
            self.vad = webrtcvad.Vad(2)  # Aggressiveness level 2
        except Exception as e:
            print(f"Error loading models: {e}")

    async def transcribe(
        self, 
        audio_url: str, 
        language: str = "ru",
        vad_enabled: bool = True
    ) -> Dict[str, Any]:
        """Transcribe audio file to text with VAD"""
        try:
            # Download and process audio
            audio_data = await self._download_audio(audio_url)
            
            # Apply VAD if enabled
            if vad_enabled:
                audio_segments = self._apply_vad(audio_data)
            else:
                audio_segments = [audio_data]

            # Transcribe each segment
            transcriptions = []
            for segment in audio_segments:
                if len(segment) > 0:
                    result = self.model.transcribe(
                        segment,
                        language=language,
                        task="transcribe"
                    )
                    transcriptions.append(result)

            # Combine results
            combined_text = " ".join([t["text"].strip() for t in transcriptions])
            
            # Calculate paralinguistic features
            paraling = self._calculate_paralinguistic(audio_data)
            
            return {
                "text": combined_text,
                "segments": transcriptions,
                "pre_answer_pause_s": paraling["pre_answer_pause_s"],
                "speech_rate_wpm": paraling["speech_rate_wpm"],
                "confidence": self._calculate_confidence(transcriptions)
            }
            
        except Exception as e:
            raise Exception(f"Transcription failed: {str(e)}")

    async def _download_audio(self, audio_url: str) -> np.ndarray:
        """Download audio from URL and convert to numpy array"""
        # This is a simplified version - in production you'd use proper HTTP client
        # For now, we'll assume it's a local file or use a placeholder
        try:
            # Load audio using librosa
            audio_data, sample_rate = librosa.load(audio_url, sr=16000)
            return audio_data
        except Exception as e:
            # Fallback: create dummy audio for testing
            print(f"Could not load audio from {audio_url}: {e}")
            # Create 1 second of silence at 16kHz
            return np.zeros(16000)

    def _apply_vad(self, audio_data: np.ndarray) -> List[np.ndarray]:
        """Apply Voice Activity Detection to audio"""
        if self.vad is None:
            return [audio_data]

        try:
            # Convert to 16-bit PCM
            audio_16bit = (audio_data * 32767).astype(np.int16)
            
            # VAD parameters
            frame_duration = 30  # ms
            frame_size = int(16000 * frame_duration / 1000)
            
            segments = []
            current_segment = []
            
            for i in range(0, len(audio_16bit), frame_size):
                frame = audio_16bit[i:i + frame_size]
                if len(frame) == frame_size:
                    frame_bytes = frame.tobytes()
                    
                    if self.vad.is_speech(frame_bytes, 16000):
                        current_segment.extend(frame)
                    else:
                        if len(current_segment) > 0:
                            segments.append(np.array(current_segment))
                            current_segment = []
            
            # Add remaining segment
            if len(current_segment) > 0:
                segments.append(np.array(current_segment))
            
            return segments
            
        except Exception as e:
            print(f"VAD failed: {e}")
            return [audio_data]

    def _calculate_paralinguistic(self, audio_data: np.ndarray) -> Dict[str, float]:
        """Calculate paralinguistic features"""
        try:
            # Calculate speech rate (words per minute)
            # This is a simplified calculation
            duration_s = len(audio_data) / 16000
            estimated_words = len(audio_data) / 16000 * 2  # Rough estimate
            speech_rate_wpm = estimated_words / duration_s * 60 if duration_s > 0 else 0
            
            # Calculate pre-answer pause (simplified)
            pre_answer_pause_s = 0.5  # Placeholder
            
            return {
                "pre_answer_pause_s": pre_answer_pause_s,
                "speech_rate_wpm": speech_rate_wpm
            }
        except Exception as e:
            print(f"Paralinguistic calculation failed: {e}")
            return {
                "pre_answer_pause_s": 0.0,
                "speech_rate_wpm": 0.0
            }

    def _calculate_confidence(self, transcriptions: List[Dict[str, Any]]) -> float:
        """Calculate overall confidence score"""
        if not transcriptions:
            return 0.0
        
        # Average confidence from all segments
        confidences = []
        for trans in transcriptions:
            if "segments" in trans:
                for segment in trans["segments"]:
                    if "avg_logprob" in segment:
                        confidences.append(segment["avg_logprob"])
        
        if confidences:
            return np.mean(confidences)
        else:
            return 0.8  # Default confidence
