"""
AI endpoints for parking slot detection
"""

from fastapi import APIRouter, HTTPException, File, UploadFile, BackgroundTasks
from fastapi.responses import JSONResponse
import cv2
import numpy as np
from typing import Dict
from datetime import datetime
import json
import redis

from app.ai.detector import ParkingSlotDetector
from app.ai.camera_manager import CameraManager
from app.core.config import settings

router = APIRouter()

# Initialize components (will be set in main.py)
detector: ParkingSlotDetector = None
camera_manager: CameraManager = None
redis_client = None


def init_ai_components(det: ParkingSlotDetector, cam_mgr: CameraManager, redis_cli=None):
    """Initialize AI components"""
    global detector, camera_manager, redis_client
    detector = det
    camera_manager = cam_mgr
    redis_client = redis_cli


@router.post("/detect-slots")
async def detect_slots(
    parking_lot_id: int,
    image: UploadFile = File(...),
    background_tasks: BackgroundTasks = None
):
    """
    Detect parking slots from an uploaded image
    """
    if not detector:
        raise HTTPException(status_code=503, detail="AI detector not initialized. Install AI dependencies: pip install ultralytics torch")
    
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
        
        return JSONResponse(content=results)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Detection error: {str(e)}")


@router.post("/detect-from-url")
async def detect_from_url(
    parking_lot_id: int,
    camera_url: str,
    background_tasks: BackgroundTasks = None
):
    """
    Detect parking slots from a camera URL
    """
    if not detector or not camera_manager:
        raise HTTPException(status_code=503, detail="AI components not initialized")
    
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
        
        return JSONResponse(content=results)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Detection error: {str(e)}")


@router.get("/parking-lot/{parking_lot_id}/slots")
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


@router.post("/parking-lot/{parking_lot_id}/start-monitoring")
async def start_monitoring(parking_lot_id: int, camera_url: str):
    """
    Start continuous monitoring of a parking lot
    """
    if not detector or not camera_manager:
        raise HTTPException(status_code=503, detail="AI components not initialized")
    
    try:
        await camera_manager.start_monitoring(parking_lot_id, camera_url, detector)
        return {
            "status": "monitoring_started",
            "parking_lot_id": parking_lot_id,
            "camera_url": camera_url
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.post("/parking-lot/{parking_lot_id}/stop-monitoring")
async def stop_monitoring(parking_lot_id: int):
    """
    Stop monitoring a parking lot
    """
    if not camera_manager:
        raise HTTPException(status_code=503, detail="AI components not initialized")
    
    try:
        await camera_manager.stop_monitoring(parking_lot_id)
        return {
            "status": "monitoring_stopped",
            "parking_lot_id": parking_lot_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.get("/parking-lot/{parking_lot_id}/safety-score")
async def get_safety_score(parking_lot_id: int):
    """
    Get AI-analyzed safety score for a parking lot
    """
    if not detector:
        raise HTTPException(status_code=503, detail="AI detector not initialized")
    
    try:
        score = await detector.analyze_safety(parking_lot_id)
        return {
            "parking_lot_id": parking_lot_id,
            "safety_score": score,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

