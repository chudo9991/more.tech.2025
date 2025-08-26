"""
Application configuration settings
"""
from typing import List
from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    
    # Database
    DATABASE_URL: str = "postgresql://interview_user:interview_pass@db:5432/interview_ai"
    
    # MinIO
    MINIO_ENDPOINT: str = "minio:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin123"
    MINIO_BUCKET_NAME: str = "interview-audio"
    
    # Service URLs
    STT_SERVICE_URL: str = "http://stt:8001"
    TTS_SERVICE_URL: str = "http://tts:8002"
    SCORING_SERVICE_URL: str = "http://scoring:8003"
    
    # CORS
    ALLOWED_HOSTS: List[str] = ["*"]
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    JWT_SECRET_KEY: str = "your-jwt-secret-key-change-in-production"
    
    # Audio Processing
    AUDIO_TTL_DAYS: int = 30
    MAX_AUDIO_DURATION_SECONDS: int = 300
    VAD_SILENCE_THRESHOLD_MS: int = 1800
    VAD_TIMEOUT_SECONDS: int = 60
    
    # SIP Provider
    SIP_PROVIDER_URL: str = "https://api.mango-office.ru"
    SIP_API_KEY: str = ""
    SIP_SECRET: str = ""
    
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
