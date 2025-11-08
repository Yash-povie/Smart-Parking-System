"""
Safety ratings endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.parking_lot import ParkingLot
from app.models.safety_review import SafetyReview
from app.schemas.parking import SafetyReviewCreate, SafetyReviewResponse

router = APIRouter()


@router.get("/{parking_lot_id}")
async def get_safety_rating(
    parking_lot_id: int,
    db: Session = Depends(get_db)
):
    """Get safety rating for a parking lot"""
    parking_lot = db.query(ParkingLot).filter(ParkingLot.id == parking_lot_id).first()
    
    if not parking_lot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Parking lot not found"
        )
    
    # Calculate average ratings
    avg_ratings = db.query(
        func.avg(SafetyReview.safety_rating).label("avg_safety"),
        func.avg(SafetyReview.lighting_rating).label("avg_lighting"),
        func.avg(SafetyReview.security_rating).label("avg_security"),
        func.avg(SafetyReview.cleanliness_rating).label("avg_cleanliness"),
        func.count(SafetyReview.id).label("total_reviews")
    ).filter(SafetyReview.parking_lot_id == parking_lot_id).first()
    
    return {
        "parking_lot_id": parking_lot_id,
        "safety_score": float(avg_ratings.avg_safety) if avg_ratings.avg_safety else parking_lot.safety_rating,
        "lighting_score": float(avg_ratings.avg_lighting) if avg_ratings.avg_lighting else None,
        "security_score": float(avg_ratings.avg_security) if avg_ratings.avg_security else None,
        "cleanliness_score": float(avg_ratings.avg_cleanliness) if avg_ratings.avg_cleanliness else None,
        "total_reviews": avg_ratings.total_reviews or parking_lot.total_reviews,
        "parking_lot_rating": parking_lot.safety_rating
    }


@router.get("/{parking_lot_id}/reviews", response_model=List[SafetyReviewResponse])
async def get_safety_reviews(
    parking_lot_id: int,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Get safety reviews for a parking lot"""
    parking_lot = db.query(ParkingLot).filter(ParkingLot.id == parking_lot_id).first()
    
    if not parking_lot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Parking lot not found"
        )
    
    reviews = db.query(SafetyReview).filter(
        SafetyReview.parking_lot_id == parking_lot_id
    ).order_by(SafetyReview.created_at.desc()).offset(skip).limit(limit).all()
    
    return reviews


@router.post("/{parking_lot_id}/review", response_model=SafetyReviewResponse, status_code=status.HTTP_201_CREATED)
async def submit_safety_review(
    parking_lot_id: int,
    review_data: SafetyReviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Submit a safety review"""
    # Verify parking lot exists
    parking_lot = db.query(ParkingLot).filter(ParkingLot.id == parking_lot_id).first()
    if not parking_lot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Parking lot not found"
        )
    
    # Check if user already reviewed this parking lot
    existing_review = db.query(SafetyReview).filter(
        SafetyReview.parking_lot_id == parking_lot_id,
        SafetyReview.user_id == current_user.id
    ).first()
    
    if existing_review:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already reviewed this parking lot"
        )
    
    # Create review
    review = SafetyReview(
        user_id=current_user.id,
        parking_lot_id=parking_lot_id,
        **review_data.dict()
    )
    
    db.add(review)
    db.commit()
    db.refresh(review)
    
    # Update parking lot average rating
    avg_rating = db.query(func.avg(SafetyReview.safety_rating)).filter(
        SafetyReview.parking_lot_id == parking_lot_id
    ).scalar()
    
    parking_lot.safety_rating = float(avg_rating) if avg_rating else 0.0
    parking_lot.total_reviews = db.query(SafetyReview).filter(
        SafetyReview.parking_lot_id == parking_lot_id
    ).count()
    
    db.commit()
    
    return review

