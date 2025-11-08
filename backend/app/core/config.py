"""
Application configuration settings
"""

from pydantic_settings import BaseSettings
from typing import List
import os
from pathlib import Path


class Settings(BaseSettings):
    """Application settings"""
    
    # App
    APP_NAME: str = "Smart Parking System"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 5000
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
    ]
    
    # Database
    # Default to SQLite for development if PostgreSQL is not available
    DATABASE_URL: str = "sqlite:///./parking.db"
    # For PostgreSQL: "postgresql://postgres:postgres@localhost:5432/parking_db"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # JWT
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # AI Service
    AI_SERVICE_URL: str = "http://localhost:8001"
    
    # File Upload
    UPLOAD_DIR: Path = Path("uploads")
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    # Stripe (Payment)
    STRIPE_SECRET_KEY: str = ""
    STRIPE_PUBLISHABLE_KEY: str = ""
    
    # Parking
    BOOKING_EXPIRY_MINUTES: int = 15
    MIN_BOOKING_DURATION_MINUTES: int = 30
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

# Create upload directory if it doesn't exist
settings.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

