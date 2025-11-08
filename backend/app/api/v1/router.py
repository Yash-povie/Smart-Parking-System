"""
API v1 Router - Main API endpoints
"""

from fastapi import APIRouter
from app.api.v1.endpoints import (
    auth,
    users,
    parking_lots,
    parking_slots,
    bookings,
    payments,
    analytics,
    safety,
    ai
)

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(parking_lots.router, prefix="/parking-lots", tags=["Parking Lots"])
api_router.include_router(parking_slots.router, prefix="/parking-slots", tags=["Parking Slots"])
api_router.include_router(bookings.router, prefix="/bookings", tags=["Bookings"])
api_router.include_router(payments.router, prefix="/payments", tags=["Payments"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
api_router.include_router(safety.router, prefix="/safety", tags=["Safety Ratings"])
api_router.include_router(ai.router, prefix="/ai", tags=["AI Detection"])


