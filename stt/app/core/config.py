"""
STT service configuration settings
"""
from typing import List
from pydantic_settings import BaseSettings
from pydantic import validator


class Settings(BaseSettings):
    """STT service settings"""
    
    # Application
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    
    # MinIO
    MINIO_ENDPOINT: str = "minio:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin123"
    MINIO_BUCKET_NAME: str = "audio-files"
    
    # CORS
    ALLOWED_HOSTS: List[str] = ["*"]
    
    # Audio Processing
    VAD_SILENCE_THRESHOLD_MS: int = 1800
    VAD_TIMEOUT_SECONDS: int = 60
    MAX_AUDIO_DURATION_SECONDS: int = 300
    
    # Whisper settings
    WHISPER_MODEL: str = "small"
    WHISPER_LANGUAGE: str = "ru"
    VAD_ENABLED: bool = True
    VAD_AGGRESSIVENESS: int = 2
    
    # Logging
    SENTRY_DSN: str = ""
    
    @validator("ALLOWED_HOSTS", pre=True)
    def assemble_cors_origins(cls, v):
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create settings instance
settings = Settings()
