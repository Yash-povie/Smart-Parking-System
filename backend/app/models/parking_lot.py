"""
Parking Lot model
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class ParkingLot(Base):
    __tablename__ = "parking_lots"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    address = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    zip_code = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    total_slots = Column(Integer, default=0)
    available_slots = Column(Integer, default=0)
    price_per_hour = Column(Float, nullable=False, default=0.0)
    description = Column(Text, nullable=True)
    image_url = Column(String, nullable=True)
    camera_url = Column(String, nullable=True)  # URL for parking lot camera feed
    is_active = Column(Boolean, default=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    safety_rating = Column(Float, default=0.0)  # Average safety rating
    total_reviews = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    owner = relationship("User", back_populates="parking_lots")
    slots = relationship("ParkingSlot", back_populates="parking_lot", cascade="all, delete-orphan")
    bookings = relationship("Booking", back_populates="parking_lot")
    reviews = relationship("SafetyReview", back_populates="parking_lot")


