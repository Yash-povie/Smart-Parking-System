"""
Parking lots management endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from typing import List, Optional
import math

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.parking_lot import ParkingLot
from app.models.parking_slot import ParkingSlot, SlotStatus
from app.schemas.parking import (
    ParkingLotCreate, ParkingLotUpdate, ParkingLotResponse,
    NearbyParkingRequest
)

router = APIRouter()


@router.get("/", response_model=List[ParkingLotResponse])
async def get_parking_lots(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    city: Optional[str] = None,
    is_active: Optional[bool] = True,
    min_rating: Optional[float] = Query(None, ge=0.0, le=5.0),
    db: Session = Depends(get_db)
):
    """Get all parking lots with filters"""
    query = db.query(ParkingLot)
    
    if is_active is not None:
        query = query.filter(ParkingLot.is_active == is_active)
    
    if city:
        query = query.filter(ParkingLot.city.ilike(f"%{city}%"))
    
    if min_rating is not None:
        query = query.filter(ParkingLot.safety_rating >= min_rating)
    
    total = query.count()
    parking_lots = query.offset(skip).limit(limit).all()
    
    # Update available slots count
    for lot in parking_lots:
        available_count = db.query(ParkingSlot).filter(
            and_(
                ParkingSlot.parking_lot_id == lot.id,
                ParkingSlot.status == SlotStatus.AVAILABLE
            )
        ).count()
        lot.available_slots = available_count
    
    return parking_lots


@router.get("/nearby", response_model=List[ParkingLotResponse])
async def get_nearby_parking_lots(
    latitude: float = Query(..., ge=-90, le=90),
    longitude: float = Query(..., ge=-180, le=180),
    radius_km: float = Query(5.0, ge=0.1, le=50.0),
    max_results: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get nearby parking lots based on location"""
    # Haversine formula for distance calculation
    # Using approximate calculation (for production, use PostGIS or similar)
    parking_lots = db.query(ParkingLot).filter(
        ParkingLot.is_active == True
    ).all()
    
    nearby_lots = []
    for lot in parking_lots:
        # Calculate distance (simplified - use proper geospatial for production)
        lat_diff = abs(lot.latitude - latitude)
        lon_diff = abs(lot.longitude - longitude)
        distance_km = math.sqrt(lat_diff**2 + lon_diff**2) * 111  # Rough conversion
        
        if distance_km <= radius_km:
            # Update available slots
            available_count = db.query(ParkingSlot).filter(
                and_(
                    ParkingSlot.parking_lot_id == lot.id,
                    ParkingSlot.status == SlotStatus.AVAILABLE
                )
            ).count()
            lot.available_slots = available_count
            nearby_lots.append((lot, distance_km))
    
    # Sort by distance
    nearby_lots.sort(key=lambda x: x[1])
    
    return [lot for lot, _ in nearby_lots[:max_results]]


@router.get("/{lot_id}", response_model=ParkingLotResponse)
async def get_parking_lot(
    lot_id: int,
    db: Session = Depends(get_db)
):
    """Get parking lot by ID"""
    parking_lot = db.query(ParkingLot).filter(ParkingLot.id == lot_id).first()
    
    if not parking_lot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Parking lot not found"
        )
    
    # Update available slots count
    available_count = db.query(ParkingSlot).filter(
        and_(
            ParkingSlot.parking_lot_id == lot_id,
            ParkingSlot.status == SlotStatus.AVAILABLE
        )
    ).count()
    parking_lot.available_slots = available_count
    
    return parking_lot


@router.post("/", response_model=ParkingLotResponse, status_code=status.HTTP_201_CREATED)
async def create_parking_lot(
    parking_lot_data: ParkingLotCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new parking lot (admin or parking owner only)"""
    if current_user.role not in ["admin", "parking_owner"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    parking_lot = ParkingLot(
        **parking_lot_data.dict(),
        owner_id=current_user.id if current_user.role == "parking_owner" else None
    )
    
    db.add(parking_lot)
    db.commit()
    db.refresh(parking_lot)
    
    return parking_lot


@router.put("/{lot_id}", response_model=ParkingLotResponse)
async def update_parking_lot(
    lot_id: int,
    parking_lot_data: ParkingLotUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update parking lot (admin or owner only)"""
    parking_lot = db.query(ParkingLot).filter(ParkingLot.id == lot_id).first()
    
    if not parking_lot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Parking lot not found"
        )
    
    # Check permissions
    if current_user.role != "admin" and parking_lot.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Update fields
    update_data = parking_lot_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(parking_lot, field, value)
    
    db.commit()
    db.refresh(parking_lot)
    
    return parking_lot


@router.delete("/{lot_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_parking_lot(
    lot_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete parking lot (admin only)"""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    parking_lot = db.query(ParkingLot).filter(ParkingLot.id == lot_id).first()
    
    if not parking_lot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Parking lot not found"
        )
    
    db.delete(parking_lot)
    db.commit()
    
    return None


@router.post("/{lot_id}/update-slots")
async def update_slot_status(
    lot_id: int,
    slot_updates: dict,
    db: Session = Depends(get_db)
):
    """Update slot status from AI service"""
    parking_lot = db.query(ParkingLot).filter(ParkingLot.id == lot_id).first()
    
    if not parking_lot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Parking lot not found"
        )
    
    # Update slot availability from AI detection results
    # This endpoint is called by the AI service
    total_slots = slot_updates.get("total_slots", 0)
    available_slots = slot_updates.get("available_slots", 0)
    occupied_slots = slot_updates.get("occupied_slots", 0)
    
    parking_lot.total_slots = total_slots
    parking_lot.available_slots = available_slots
    
    db.commit()
    
    return {"status": "updated", "parking_lot_id": lot_id}

