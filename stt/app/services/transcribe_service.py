"""
Transcription service for STT
"""
import asyncio
import tempfile
import os
import io
from typing import Dict, Any, List
import whisper
import webrtcvad
import numpy as np
from pydub import AudioSegment
import librosa
from minio import Minio
from minio.error import S3Error

from app.core.config import settings


class TranscribeService:
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TranscribeService, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            print("Initializing TranscribeService...")
            self.model = None
            self.vad = None
            self.minio_client = None
            self._models_loaded = False
            print("Calling _init_minio...")
            self._init_minio()
            print("TranscribeService initialized")
            # Load models immediately to avoid download on first request
            self._load_models()
            self._initialized = True

    def _load_models(self):
        """Load Whisper and VAD models"""
        if self._models_loaded:
            print("Models already loaded, skipping...")
            return
            
        try:
            print(f"Loading Whisper model: {settings.WHISPER_MODEL}")
            
            # Check if model exists in cache
            import os
            cache_dir = os.path.expanduser("~/.cache/whisper")
            model_path = os.path.join(cache_dir, f"{settings.WHISPER_MODEL}.pt")
            
            if os.path.exists(model_path):
                print(f"Model found in cache: {model_path}")
                model_size = os.path.getsize(model_path)
                model_size_mb = model_size / (1024 * 1024)
                print(f"Model size: {model_size_mb:.1f} MB")
            else:
                print(f"Model not found in cache, downloading: {settings.WHISPER_MODEL}")
                print("This may take a few minutes on first run...")
            
            # Load Whisper model (will download if not cached)
            self.model = whisper.load_model(settings.WHISPER_MODEL)
            
            # Verify model was loaded
            if self.model is None:
                raise Exception("Failed to load Whisper model")
            
            # Get final model info
            if os.path.exists(model_path):
                model_size = os.path.getsize(model_path)
                model_size_mb = model_size / (1024 * 1024)
                print(f"Whisper model loaded successfully: {settings.WHISPER_MODEL} ({model_size_mb:.1f} MB)")
            else:
                print(f"Whisper model loaded successfully: {settings.WHISPER_MODEL}")
            
            # Initialize VAD
            self.vad = webrtcvad.Vad(settings.VAD_AGGRESSIVENESS)
            print(f"VAD initialized with aggressiveness: {settings.VAD_AGGRESSIVENESS}")
            
            # Mark models as loaded
            self._models_loaded = True
            print("All models loaded successfully!")
            
        except Exception as e:
            print(f"Error loading models: {e}")
            import traceback
            traceback.print_exc()
            raise Exception(f"Failed to load models: {str(e)}")

    def _init_minio(self):
        """Initialize MinIO client"""
        try:
            print(f"Initializing MinIO client with endpoint: {settings.MINIO_ENDPOINT}")
            print(f"MinIO access key: {settings.MINIO_ACCESS_KEY}")
            print(f"MinIO secret key: {settings.MINIO_SECRET_KEY}")
            
            self.minio_client = Minio(
                settings.MINIO_ENDPOINT,
                access_key=settings.MINIO_ACCESS_KEY,
                secret_key=settings.MINIO_SECRET_KEY,
                secure=False  # Use HTTP for local development
            )
            print(f"MinIO client initialized successfully: {settings.MINIO_ENDPOINT}")
            
            # Test connection
            buckets = list(self.minio_client.list_buckets())
            print(f"Available buckets: {[b.name for b in buckets]}")
            
        except Exception as e:
            print(f"Error initializing MinIO client: {e}")
            import traceback
            traceback.print_exc()
            self.minio_client = None

    async def transcribe(
        self, 
        audio_url: str, 
        language: str = "ru",
        vad_enabled: bool = True
    ) -> Dict[str, Any]:
        """Transcribe audio file to text with VAD"""
        try:
            # Ensure models are loaded
            if not self._models_loaded or self.model is None:
                self._load_models()
            
            print(f"Starting transcription for {audio_url}")
            
            # Download and process audio
            audio_data = await self._download_audio(audio_url)
            print(f"Audio data shape: {audio_data.shape}, dtype: {audio_data.dtype}")
            
            # Apply VAD if enabled
            if vad_enabled:
                audio_segments = self._apply_vad(audio_data)
                print(f"VAD segments: {len(audio_segments)}")
            else:
                audio_segments = [audio_data]

            # Transcribe each segment
            transcriptions = []
            for i, segment in enumerate(audio_segments):
                if len(segment) > 0:
                    print(f"Transcribing segment {i+1}/{len(audio_segments)}, length: {len(segment)}")
                    try:
                        result = self.model.transcribe(
                            segment,
                            language=language,
                            task="transcribe",
                            fp16=False,  # Use FP32 for better accuracy
                            temperature=0.0,  # No randomness
                            condition_on_previous_text=False,  # Don't condition on previous text
                            initial_prompt=None,  # No initial prompt
                            word_timestamps=False,  # Don't need word timestamps
                            compression_ratio_threshold=2.4,  # Filter out bad transcriptions
                            logprob_threshold=-1.0,  # Filter out low confidence
                            no_speech_threshold=0.6  # Filter out silence
                        )
                        transcriptions.append(result)
                        print(f"Segment {i+1} transcribed successfully: '{result['text']}'")
                    except Exception as seg_error:
                        print(f"Error transcribing segment {i+1}: {seg_error}")
                        raise seg_error

            # Combine results and filter out artifacts
            combined_text = " ".join([t["text"].strip() for t in transcriptions])
            
            # Filter out common subtitle artifacts
            artifacts_to_remove = [
                "Редактор субтитров",
                "Корректор",
                "А.Семкин",
                "А.Егорова",
                "Субтитры:",
                "Перевод:",
                "Редактор:"
            ]
            
            for artifact in artifacts_to_remove:
                combined_text = combined_text.replace(artifact, "")
            
            # Clean up extra spaces
            combined_text = " ".join(combined_text.split())
            
            print(f"Combined text: '{combined_text}'")
            
            # Calculate paralinguistic features
            paraling = self._calculate_paralinguistic(audio_data)
            
            return {
                "text": combined_text,
                "segments": transcriptions,
                "pre_answer_pause_s": paraling["pre_answer_pause_s"],
                "speech_rate_wpm": paraling["speech_rate_wpm"],
                "confidence": self._calculate_confidence(transcriptions),
                "audio_url": audio_url  # Return the MinIO URL
            }
            
        except Exception as e:
            print(f"Transcription error: {str(e)}")
            import traceback
            traceback.print_exc()
            raise Exception(f"Transcription failed: {str(e)}")

    async def save_audio_to_minio(self, audio_data: bytes, filename: str, bucket_name: str = "audio-files") -> str:
        """Save audio file to MinIO and return the object URL"""
        try:
            print(f"Starting save_audio_to_minio: filename={filename}, size={len(audio_data)} bytes")
            
            if not self.minio_client:
                raise Exception("MinIO client not initialized")

            # Ensure bucket exists
            if not self.minio_client.bucket_exists(bucket_name):
                print(f"Creating bucket: {bucket_name}")
                self.minio_client.make_bucket(bucket_name)
                print(f"Created bucket: {bucket_name}")
            else:
                print(f"Bucket {bucket_name} already exists")

            # Upload audio file
            print(f"Uploading file to MinIO: {bucket_name}/{filename}")
            audio_stream = io.BytesIO(audio_data)
            try:
                result = self.minio_client.put_object(
                    bucket_name, 
                    filename, 
                    audio_stream, 
                    length=len(audio_data),
                    content_type="audio/webm"
                )
                print(f"Upload result: {result}")
                print(f"Upload successful: {result.object_name}")
            except Exception as upload_error:
                print(f"Upload error: {upload_error}")
                raise upload_error
            
            # Verify file was uploaded
            try:
                stat = self.minio_client.stat_object(bucket_name, filename)
                print(f"File verified: {stat.object_name}, size: {stat.size}")
            except Exception as verify_error:
                print(f"Warning: Could not verify file upload: {verify_error}")
            
            # Return object URL
            object_url = f"minio://{bucket_name}/{filename}"
            print(f"Audio saved to MinIO: {object_url}")
            return object_url
            
        except Exception as e:
            print(f"Error saving audio to MinIO: {e}")
            import traceback
            traceback.print_exc()
            raise Exception(f"Failed to save audio to MinIO: {str(e)}")

    async def get_audio_from_minio(self, object_url: str) -> bytes:
        """Get audio file from MinIO"""
        try:
            if not self.minio_client:
                raise Exception("MinIO client not initialized")

            # Parse object URL: minio://bucket/object
            if object_url.startswith("minio://"):
                path = object_url[8:]  # Remove "minio://"
                bucket_name, object_name = path.split("/", 1)
            else:
                raise Exception(f"Invalid MinIO URL format: {object_url}")

            # Get object
            response = self.minio_client.get_object(bucket_name, object_name)
            audio_data = response.read()
            response.close()
            response.release_conn()
            
            return audio_data
            
        except Exception as e:
            print(f"Error getting audio from MinIO: {e}")
            raise Exception(f"Failed to get audio from MinIO: {str(e)}")

    async def _download_audio(self, audio_url: str) -> np.ndarray:
        """Download audio from URL and convert to numpy array"""
        try:
            print(f"Downloading audio from: {audio_url}")
            
            if audio_url.startswith("minio://"):
                # Get from MinIO
                audio_data = await self.get_audio_from_minio(audio_url)
                print(f"Retrieved {len(audio_data)} bytes from MinIO")
                
                # Convert WebM to WAV using pydub
                audio = AudioSegment.from_file(io.BytesIO(audio_data), format="webm")
                print(f"AudioSegment created: {len(audio)}ms, {audio.channels} channels, {audio.frame_rate}Hz")
                
                # Export as WAV to bytes with specific parameters
                wav_bytes = io.BytesIO()
                audio.export(wav_bytes, format="wav", parameters=["-ar", "16000", "-ac", "1"])
                wav_bytes.seek(0)
                print(f"WAV export completed: {wav_bytes.tell()} bytes")
                
                # Load with librosa and ensure float32 format
                audio_array, sample_rate = librosa.load(wav_bytes, sr=16000, dtype=np.float32)
                print(f"Librosa load: shape={audio_array.shape}, sr={sample_rate}, dtype={audio_array.dtype}")
                
                # Convert to torch tensor for Whisper
                import torch
                audio_tensor = torch.from_numpy(audio_array).float()
                print(f"Torch tensor: shape={audio_tensor.shape}, dtype={audio_tensor.dtype}")
                
                # Ensure the array is contiguous and in the right format
                audio_array = np.ascontiguousarray(audio_array, dtype=np.float32)
                print(f"Final audio array: shape={audio_array.shape}, dtype={audio_array.dtype}")
                return audio_array
            else:
                # Load audio using librosa (for other URLs)
                audio_data, sample_rate = librosa.load(audio_url, sr=16000, dtype=np.float32)
                audio_data = np.ascontiguousarray(audio_data, dtype=np.float32)
                return audio_data
        except Exception as e:
            # Fallback: create dummy audio for testing
            print(f"Could not load audio from {audio_url}: {e}")
            import traceback
            traceback.print_exc()
            # Create 1 second of silence at 16kHz
            return np.zeros(16000, dtype=np.float32)

    def _apply_vad(self, audio_data: np.ndarray) -> List[np.ndarray]:
        """Apply Voice Activity Detection to audio"""
        if self.vad is None:
            return [audio_data]

        try:
            print(f"VAD input: shape={audio_data.shape}, dtype={audio_data.dtype}")
            
            # Convert to 16-bit PCM for VAD
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
                            # Convert back to float32 for Whisper
                            segment_float = np.array(current_segment, dtype=np.float32) / 32767.0
                            segments.append(segment_float)
                            current_segment = []
            
            # Add remaining segment
            if len(current_segment) > 0:
                # Convert back to float32 for Whisper
                segment_float = np.array(current_segment, dtype=np.float32) / 32767.0
                segments.append(segment_float)
            
            print(f"VAD output: {len(segments)} segments")
            for i, seg in enumerate(segments):
                print(f"  Segment {i+1}: shape={seg.shape}, dtype={seg.dtype}")
            
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

    def get_model_status(self) -> Dict[str, Any]:
        """Get model loading status and information"""
        import os
        
        try:
            cache_dir = os.path.expanduser("~/.cache/whisper")
            model_path = os.path.join(cache_dir, f"{settings.WHISPER_MODEL}.pt")
            
            status = {
                "whisper_model": settings.WHISPER_MODEL,
                "model_loaded": self._models_loaded,
                "model_exists": os.path.exists(model_path),
                "vad_loaded": self.vad is not None,
                "minio_connected": self.minio_client is not None
            }
            
            if os.path.exists(model_path):
                model_size = os.path.getsize(model_path)
                status["model_size_mb"] = round(model_size / (1024 * 1024), 1)
                status["model_path"] = model_path
            else:
                status["model_size_mb"] = 0
                status["model_path"] = None
            
            return status
            
        except Exception as e:
            return {
                "error": str(e),
                "whisper_model": settings.WHISPER_MODEL,
                "model_loaded": False,
                "model_exists": False,
                "vad_loaded": False,
                "minio_connected": False
            }

    def clear_model_cache(self) -> Dict[str, Any]:
        """Clear Whisper model cache"""
        import os
        import shutil
        
        try:
            cache_dir = os.path.expanduser("~/.cache/whisper")
            model_path = os.path.join(cache_dir, f"{settings.WHISPER_MODEL}.pt")
            
            if os.path.exists(model_path):
                os.remove(model_path)
                print(f"Removed cached model: {model_path}")
                
                # Reset loaded flag
                self._models_loaded = False
                self.model = None
                
                return {
                    "message": "Model cache cleared successfully",
                    "removed_file": model_path,
                    "model_loaded": False
                }
            else:
                return {
                    "message": "No cached model found",
                    "model_loaded": False
                }
                
        except Exception as e:
            return {
                "error": str(e),
                "message": "Failed to clear model cache"
            }
