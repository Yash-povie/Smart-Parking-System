"""
Safety Review model
"""

from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class SafetyReview(Base):
    __tablename__ = "safety_reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    parking_lot_id = Column(Integer, ForeignKey("parking_lots.id"), nullable=False)
    
    # Rating (1-5)
    safety_rating = Column(Float, nullable=False)  # 1.0 to 5.0
    lighting_rating = Column(Float, nullable=True)
    security_rating = Column(Float, nullable=True)
    cleanliness_rating = Column(Float, nullable=True)
    
    # Review text
    review_text = Column(Text, nullable=True)
    
    # AI-generated insights
    ai_safety_score = Column(Float, nullable=True)  # AI-analyzed safety score
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="safety_reviews")
    parking_lot = relationship("ParkingLot", back_populates="reviews")


