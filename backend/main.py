"""
Smart Parking System - FastAPI Backend
Main application entry point
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import engine, Base
from app.api.v1.router import api_router
from app.websocket.manager import websocket_manager
from app.ai.detector import ParkingSlotDetector
from app.ai.camera_manager import CameraManager
from app.api.v1.endpoints.ai import init_ai_components
from fastapi import WebSocket
import redis


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    try:
        # Try to create tables, but don't fail if DB is not available
        Base.metadata.create_all(bind=engine)
        print("✓ Database connection successful")
    except Exception as e:
        print(f"⚠ Database connection failed: {e}")
        print("⚠ Application will continue, but database features may not work")
        print("⚠ Please check your DATABASE_URL in .env file")
    
    # Initialize AI components
    try:
        print("🤖 Initializing AI components...")
        detector = ParkingSlotDetector()
        camera_manager = CameraManager()
        
        # Try to load model (non-blocking)
        try:
            await detector.load_model()
        except Exception as e:
            print(f"⚠ AI model loading failed: {e}")
            print("⚠ AI features may be limited")
        
        # Try to connect to Redis (optional)
        redis_client = None
        try:
            redis_client = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)
            redis_client.ping()
            print("✓ Redis connection successful")
        except Exception as e:
            print(f"⚠ Redis connection failed: {e}")
            print("⚠ Caching features may not work")
            redis_client = None
        
        # Initialize AI endpoints
        init_ai_components(detector, camera_manager, redis_client)
        print("✓ AI components initialized")
    except Exception as e:
        print(f"⚠ AI initialization failed: {e}")
        print("⚠ AI features may not work")
    
    yield
    # Shutdown
    pass


app = FastAPI(
    title="Smart Parking System API",
    description="AI-powered smart parking solution with real-time detection",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix="/api/v1")

# WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket_manager.handle_websocket(websocket)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Smart Parking System API",
        "version": "1.0.0",
        "docs": "/api/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "smart-parking-api"}


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": str(exc),
            "path": str(request.url)
        }
    )


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )

