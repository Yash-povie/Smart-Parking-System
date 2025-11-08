"""
Parking slots endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.parking_slot import ParkingSlot, SlotStatus
from app.models.parking_lot import ParkingLot
from app.schemas.parking import ParkingSlotResponse, ParkingSlotCreate

router = APIRouter()


@router.get("/", response_model=List[ParkingSlotResponse])
async def get_parking_slots(
    parking_lot_id: int = Query(..., description="Parking lot ID"),
    status_filter: Optional[str] = Query(None, description="Filter by status"),
    db: Session = Depends(get_db)
):
    """Get parking slots for a parking lot"""
    # Verify parking lot exists
    parking_lot = db.query(ParkingLot).filter(ParkingLot.id == parking_lot_id).first()
    if not parking_lot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Parking lot not found"
        )
    
    query = db.query(ParkingSlot).filter(ParkingSlot.parking_lot_id == parking_lot_id)
    
    if status_filter:
        try:
            slot_status = SlotStatus(status_filter)
            query = query.filter(ParkingSlot.status == slot_status)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid status: {status_filter}"
            )
    
    slots = query.all()
    return slots


@router.get("/{slot_id}", response_model=ParkingSlotResponse)
async def get_parking_slot(
    slot_id: int,
    db: Session = Depends(get_db)
):
    """Get parking slot by ID"""
    slot = db.query(ParkingSlot).filter(ParkingSlot.id == slot_id).first()
    
    if not slot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Parking slot not found"
        )
    
    return slot


@router.post("/", response_model=ParkingSlotResponse, status_code=status.HTTP_201_CREATED)
async def create_parking_slot(
    slot_data: ParkingSlotCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new parking slot (admin or parking owner only)"""
    
    # Verify parking lot exists
    parking_lot = db.query(ParkingLot).filter(ParkingLot.id == slot_data.parking_lot_id).first()
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
    
    # Check if slot number already exists
    existing = db.query(ParkingSlot).filter(
        ParkingSlot.parking_lot_id == slot_data.parking_lot_id,
        ParkingSlot.slot_number == slot_data.slot_number
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Slot number already exists for this parking lot"
        )
    
    slot = ParkingSlot(**slot_data.dict())
    db.add(slot)
    db.commit()
    db.refresh(slot)
    
    # Update parking lot total slots
    parking_lot.total_slots = db.query(ParkingSlot).filter(
        ParkingSlot.parking_lot_id == slot_data.parking_lot_id
    ).count()
    db.commit()
    
    return slot


@router.put("/{slot_id}/status")
async def update_slot_status(
    slot_id: int,
    new_status: str,
    db: Session = Depends(get_db)
):
    """Update slot status (called by AI service)"""
    slot = db.query(ParkingSlot).filter(ParkingSlot.id == slot_id).first()
    
    if not slot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Parking slot not found"
        )
    
    try:
        slot.status = SlotStatus(new_status)
        from datetime import datetime
        slot.last_detected_at = datetime.utcnow()
        db.commit()
        db.refresh(slot)
        
        return slot
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status: {new_status}"
        )

