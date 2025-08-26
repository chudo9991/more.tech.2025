"""
TTS service configuration settings
"""
from typing import List
from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    """TTS service settings"""
    
    # Application
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    
    # MinIO
    MINIO_ENDPOINT: str = "minio:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin123"
    MINIO_BUCKET_NAME: str = "interview-audio"
    
    # CORS
    ALLOWED_HOSTS: List[str] = ["*"]
    
    # TTS settings
    TTS_MODEL: str = "tts_models/ru/mai/tacotron2-DDC"
    TTS_VOICE: str = "default"
    TTS_SPEAKER: str = "default"
    
    # Cache settings
    ENABLE_AUDIO_CACHE: bool = True
    CACHE_TTL_HOURS: int = 24
    CACHE_DIR: str = "/tmp/tts_cache"
    
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
