"""
Booking model
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Enum, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class BookingStatus(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    EXPIRED = "expired"


class Booking(Base):
    __tablename__ = "bookings"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    parking_lot_id = Column(Integer, ForeignKey("parking_lots.id"), nullable=False)
    slot_id = Column(Integer, ForeignKey("parking_slots.id"), nullable=True)
    status = Column(Enum(BookingStatus), default=BookingStatus.PENDING)
    
    # Timing
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)
    actual_start_time = Column(DateTime(timezone=True), nullable=True)
    actual_end_time = Column(DateTime(timezone=True), nullable=True)
    
    # Pricing
    price_per_hour = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)
    payment_status = Column(String, default="pending")  # pending, paid, refunded
    payment_intent_id = Column(String, nullable=True)  # Stripe payment intent ID
    
    # Additional info
    vehicle_number = Column(String, nullable=True)
    notes = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="bookings")
    parking_lot = relationship("ParkingLot", back_populates="bookings")
    slot = relationship("ParkingSlot", back_populates="bookings")


