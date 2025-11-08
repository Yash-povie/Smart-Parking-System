"""
Parking Slot model
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class SlotStatus(str, enum.Enum):
    AVAILABLE = "available"
    OCCUPIED = "occupied"
    RESERVED = "reserved"
    MAINTENANCE = "maintenance"


class ParkingSlot(Base):
    __tablename__ = "parking_slots"
    
    id = Column(Integer, primary_key=True, index=True)
    parking_lot_id = Column(Integer, ForeignKey("parking_lots.id"), nullable=False)
    slot_number = Column(String, nullable=False)  # e.g., "A1", "B3"
    status = Column(Enum(SlotStatus), default=SlotStatus.AVAILABLE)
    is_disabled = Column(Boolean, default=False)  # For disabled parking
    is_ev_charging = Column(Boolean, default=False)  # For EV charging spots
    camera_detection_id = Column(String, nullable=True)  # ID for AI detection
    last_detected_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    parking_lot = relationship("ParkingLot", back_populates="slots")
    bookings = relationship("Booking", back_populates="slot")


