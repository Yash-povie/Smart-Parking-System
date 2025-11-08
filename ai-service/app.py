"""
AI Service for Smart Parking System
Computer vision service for parking slot detection
"""

from fastapi import FastAPI, HTTPException, File, UploadFile, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import cv2
import numpy as np
from typing import List, Dict, Optional
import asyncio
from datetime import datetime
import os
from pathlib import Path
import redis
import json
from dotenv import load_dotenv

from app.detector import ParkingSlotDetector
from app.camera_manager import CameraManager
from app.config import settings

load_dotenv()

app = FastAPI(
    title="Smart Parking AI Service",
    description="AI-powered parking slot detection service",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
detector = ParkingSlotDetector()
camera_manager = CameraManager()
redis_client = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True) if settings.REDIS_URL else None


@app.on_event("startup")
async def startup_event():
    """Initialize on startup"""
    print("🤖 AI Service starting up...")
    print("📹 Loading parking slot detection model...")
    await detector.load_model()
    print("✅ AI Service ready!")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "Smart Parking AI Service",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "ai-service",
        "model_loaded": detector.model_loaded
    }


@app.post("/detect-slots")
async def detect_slots(
    parking_lot_id: int,
    image: UploadFile = File(...),
    background_tasks: BackgroundTasks = None
):
    """
    Detect parking slots from an uploaded image
    """
    try:
        # Read image
        image_bytes = await image.read()
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            raise HTTPException(status_code=400, detail="Invalid image format")
        
        # Detect parking slots
        results = await detector.detect_slots(img, parking_lot_id)
        
        # Store results in Redis for real-time updates
        if redis_client:
            cache_key = f"parking_lot:{parking_lot_id}:slots"
            redis_client.setex(
                cache_key,
                300,  # 5 minutes TTL
                json.dumps(results)
            )
        
        # Background task to update backend
        if background_tasks:
            background_tasks.add_task(
                update_backend_slots,
                parking_lot_id,
                results
            )
        
        return JSONResponse(content=results)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Detection error: {str(e)}")


@app.post("/detect-from-url")
async def detect_from_url(
    parking_lot_id: int,
    camera_url: str,
    background_tasks: BackgroundTasks = None
):
    """
    Detect parking slots from a camera URL
    """
    try:
        # Fetch image from camera URL
        img = await camera_manager.fetch_image(camera_url)
        
        if img is None:
            raise HTTPException(status_code=400, detail="Failed to fetch image from camera")
        
        # Detect parking slots
        results = await detector.detect_slots(img, parking_lot_id)
        
        # Store results in Redis
        if redis_client:
            cache_key = f"parking_lot:{parking_lot_id}:slots"
            redis_client.setex(
                cache_key,
                300,
                json.dumps(results)
            )
        
        # Background task to update backend
        if background_tasks:
            background_tasks.add_task(
                update_backend_slots,
                parking_lot_id,
                results
            )
        
        return JSONResponse(content=results)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Detection error: {str(e)}")


@app.get("/parking-lot/{parking_lot_id}/slots")
async def get_slot_status(parking_lot_id: int):
    """
    Get current slot status for a parking lot
    """
    try:
        # Try to get from Redis cache first
        if redis_client:
            cache_key = f"parking_lot:{parking_lot_id}:slots"
            cached = redis_client.get(cache_key)
            if cached:
                return JSONResponse(content=json.loads(cached))
        
        # If not in cache, return empty status
        return JSONResponse(content={
            "parking_lot_id": parking_lot_id,
            "slots": [],
            "total_slots": 0,
            "available_slots": 0,
            "occupied_slots": 0,
            "timestamp": datetime.now().isoformat()
        })
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.post("/parking-lot/{parking_lot_id}/start-monitoring")
async def start_monitoring(parking_lot_id: int, camera_url: str):
    """
    Start continuous monitoring of a parking lot
    """
    try:
        await camera_manager.start_monitoring(parking_lot_id, camera_url, detector)
        return {
            "status": "monitoring_started",
            "parking_lot_id": parking_lot_id,
            "camera_url": camera_url
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.post("/parking-lot/{parking_lot_id}/stop-monitoring")
async def stop_monitoring(parking_lot_id: int):
    """
    Stop monitoring a parking lot
    """
    try:
        await camera_manager.stop_monitoring(parking_lot_id)
        return {
            "status": "monitoring_stopped",
            "parking_lot_id": parking_lot_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.get("/parking-lot/{parking_lot_id}/safety-score")
async def get_safety_score(parking_lot_id: int):
    """
    Get AI-analyzed safety score for a parking lot
    """
    try:
        score = await detector.analyze_safety(parking_lot_id)
        return {
            "parking_lot_id": parking_lot_id,
            "safety_score": score,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


async def update_backend_slots(parking_lot_id: int, results: Dict):
    """
    Background task to update backend with slot detection results
    """
    try:
        import httpx
        async with httpx.AsyncClient() as client:
            await client.post(
                f"{settings.BACKEND_URL}/api/v1/parking-lots/{parking_lot_id}/update-slots",
                json=results,
                timeout=5.0
            )
    except Exception as e:
        print(f"Failed to update backend: {e}")


if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )


