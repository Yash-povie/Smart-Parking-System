"""
Parking-related schemas
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal


class ParkingLotBase(BaseModel):
    name: str
    address: str
    city: str
    state: str
    zip_code: str
    latitude: float
    longitude: float
    price_per_hour: float
    description: Optional[str] = None
    image_url: Optional[str] = None
    camera_url: Optional[str] = None


class ParkingLotCreate(ParkingLotBase):
    pass


class ParkingLotUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    price_per_hour: Optional[float] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    camera_url: Optional[str] = None
    is_active: Optional[bool] = None


class ParkingLotResponse(ParkingLotBase):
    id: int
    total_slots: int
    available_slots: int
    safety_rating: float
    total_reviews: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class ParkingSlotBase(BaseModel):
    slot_number: str
    is_disabled: bool = False
    is_ev_charging: bool = False


class ParkingSlotCreate(ParkingSlotBase):
    parking_lot_id: int


class ParkingSlotResponse(ParkingSlotBase):
    id: int
    parking_lot_id: int
    status: str
    last_detected_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class BookingBase(BaseModel):
    parking_lot_id: int
    slot_id: Optional[int] = None
    start_time: datetime
    end_time: datetime
    vehicle_number: Optional[str] = None
    notes: Optional[str] = None


class BookingCreate(BookingBase):
    pass


class BookingResponse(BookingBase):
    id: int
    user_id: int
    status: str
    actual_start_time: Optional[datetime] = None
    actual_end_time: Optional[datetime] = None
    price_per_hour: float
    total_price: float
    payment_status: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class SafetyReviewCreate(BaseModel):
    parking_lot_id: int
    safety_rating: float = Field(..., ge=1.0, le=5.0)
    lighting_rating: Optional[float] = Field(None, ge=1.0, le=5.0)
    security_rating: Optional[float] = Field(None, ge=1.0, le=5.0)
    cleanliness_rating: Optional[float] = Field(None, ge=1.0, le=5.0)
    review_text: Optional[str] = None


class SafetyReviewResponse(BaseModel):
    id: int
    user_id: int
    parking_lot_id: int
    safety_rating: float
    lighting_rating: Optional[float] = None
    security_rating: Optional[float] = None
    cleanliness_rating: Optional[float] = None
    review_text: Optional[str] = None
    ai_safety_score: Optional[float] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class NearbyParkingRequest(BaseModel):
    latitude: float
    longitude: float
    radius_km: float = 5.0
    max_results: int = 20


