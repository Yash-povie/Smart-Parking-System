"""
Configuration settings for AI Service
"""

from pydantic_settings import BaseSettings
from typing import List
from pathlib import Path


class Settings(BaseSettings):
    """Application settings"""
    
    # App
    APP_NAME: str = "Smart Parking AI Service"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8001
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/1"
    
    # Backend API
    BACKEND_URL: str = "http://localhost:5000"
    
    # Model
    MODEL_PATH: Path = Path("models/parking_slot_detector.pt")
    CONFIDENCE_THRESHOLD: float = 0.5
    
    # Monitoring
    DETECTION_INTERVAL: int = 30  # seconds
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

