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
