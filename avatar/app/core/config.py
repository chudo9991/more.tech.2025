"""
Avatar service configuration settings
"""
from typing import List
from pydantic_settings import BaseSettings
from pydantic import validator


class Settings(BaseSettings):
    """Avatar service settings"""
    
    # Application
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    
    # MinIO
    MINIO_ENDPOINT: str = "minio:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin123"
    MINIO_BUCKET_NAME: str = "interview-avatars"
    
    # Avatar settings
    AVATAR_MODEL: str = "stable-diffusion-xl-base-1.0"
    AVATAR_STYLE: str = "professional"
    AVATAR_SIZE: str = "512x512"
    AVATAR_CACHE_TTL_HOURS: int = 24
    
    # A2E API settings
    A2E_API_KEY: str = ""
    A2E_BASE_URL: str = "https://video.a2e.ai"
    A2E_DEFAULT_AVATAR_ID: str = "68af59a86eeedd0042ca7e27"  # Default Avatar (working for video)
    A2E_DEFAULT_VOICE_ID: str = "66d3f6a704d077b1432fb7d3"  # Nadia
    A2E_DEFAULT_RESOLUTION: int = 720  # Default video resolution (1:1 format)
    A2E_DEFAULT_SPEECH_RATE: float = 1.5
    
    # CORS
    ALLOWED_HOSTS: List[str] = ["*"]
    
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
