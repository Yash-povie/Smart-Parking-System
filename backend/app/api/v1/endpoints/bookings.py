"""
Booking management endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional
from datetime import datetime, timedelta

from app.core.database import get_db
from app.core.security import get_current_user
from app.core.config import settings
from app.models.user import User
from app.models.booking import Booking, BookingStatus
from app.models.parking_lot import ParkingLot
from app.models.parking_slot import ParkingSlot, SlotStatus
from app.schemas.parking import BookingCreate, BookingResponse

router = APIRouter()


@router.post("/", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
async def create_booking(
    booking_data: BookingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new booking"""
    # Validate parking lot exists
    parking_lot = db.query(ParkingLot).filter(ParkingLot.id == booking_data.parking_lot_id).first()
    if not parking_lot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Parking lot not found"
        )
    
    if not parking_lot.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Parking lot is not active"
        )
    
    # Validate time range
    if booking_data.end_time <= booking_data.start_time:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="End time must be after start time"
        )
    
    duration_minutes = (booking_data.end_time - booking_data.start_time).total_seconds() / 60
    if duration_minutes < settings.MIN_BOOKING_DURATION_MINUTES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Minimum booking duration is {settings.MIN_BOOKING_DURATION_MINUTES} minutes"
        )
    
    # Check if slot is available (if specified)
    slot = None
    if booking_data.slot_id:
        slot = db.query(ParkingSlot).filter(ParkingSlot.id == booking_data.slot_id).first()
        if not slot:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Parking slot not found"
            )
        
        if slot.parking_lot_id != booking_data.parking_lot_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Slot does not belong to this parking lot"
            )
        
        if slot.status != SlotStatus.AVAILABLE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Slot is not available"
            )
        
        # Check for conflicting bookings
        conflicting = db.query(Booking).filter(
            and_(
                Booking.slot_id == booking_data.slot_id,
                Booking.status.in_([BookingStatus.CONFIRMED, BookingStatus.ACTIVE]),
                Booking.start_time < booking_data.end_time,
                Booking.end_time > booking_data.start_time
            )
        ).first()
        
        if conflicting:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Slot is already booked for this time"
            )
    
    # Calculate price
    hours = duration_minutes / 60
    total_price = parking_lot.price_per_hour * hours
    
    # Create booking
    booking = Booking(
        user_id=current_user.id,
        parking_lot_id=booking_data.parking_lot_id,
        slot_id=booking_data.slot_id,
        start_time=booking_data.start_time,
        end_time=booking_data.end_time,
        price_per_hour=parking_lot.price_per_hour,
        total_price=total_price,
        vehicle_number=booking_data.vehicle_number,
        notes=booking_data.notes,
        status=BookingStatus.PENDING
    )
    
    db.add(booking)
    db.commit()
    db.refresh(booking)
    
    # Reserve slot if specified
    if slot:
        slot.status = SlotStatus.RESERVED
        db.commit()
    
    return booking


@router.get("/", response_model=List[BookingResponse])
async def get_bookings(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    status_filter: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get user's bookings"""
    query = db.query(Booking).filter(Booking.user_id == current_user.id)
    
    if status_filter:
        try:
            booking_status = BookingStatus(status_filter)
            query = query.filter(Booking.status == booking_status)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid status: {status_filter}"
            )
    
    bookings = query.order_by(Booking.created_at.desc()).offset(skip).limit(limit).all()
    return bookings


@router.get("/{booking_id}", response_model=BookingResponse)
async def get_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get booking by ID"""
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )
    
    # Check if user owns this booking or is admin
    if booking.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    return booking


@router.post("/{booking_id}/confirm")
async def confirm_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Confirm a booking (after payment)"""
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )
    
    if booking.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    if booking.status != BookingStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Booking is not in pending status"
        )
    
    if booking.payment_status != "paid":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Payment required to confirm booking"
        )
    
    booking.status = BookingStatus.CONFIRMED
    db.commit()
    db.refresh(booking)
    
    return booking


@router.post("/{booking_id}/cancel")
async def cancel_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Cancel a booking"""
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )
    
    if booking.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    if booking.status in [BookingStatus.COMPLETED, BookingStatus.CANCELLED]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Booking cannot be cancelled"
        )
    
    booking.status = BookingStatus.CANCELLED
    
    # Free up the slot
    if booking.slot_id:
        slot = db.query(ParkingSlot).filter(ParkingSlot.id == booking.slot_id).first()
        if slot:
            slot.status = SlotStatus.AVAILABLE
    
    db.commit()
    db.refresh(booking)
    
    return booking


@router.post("/{booking_id}/start")
async def start_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Start a booking (when user arrives)"""
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )
    
    if booking.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    if booking.status != BookingStatus.CONFIRMED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Booking must be confirmed before starting"
        )
    
    booking.status = BookingStatus.ACTIVE
    booking.actual_start_time = datetime.utcnow()
    
    # Mark slot as occupied
    if booking.slot_id:
        slot = db.query(ParkingSlot).filter(ParkingSlot.id == booking.slot_id).first()
        if slot:
            slot.status = SlotStatus.OCCUPIED
    
    db.commit()
    db.refresh(booking)
    
    return booking


@router.post("/{booking_id}/end")
async def end_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """End a booking (when user leaves)"""
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )
    
    if booking.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    if booking.status != BookingStatus.ACTIVE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Booking is not active"
        )
    
    booking.status = BookingStatus.COMPLETED
    booking.actual_end_time = datetime.utcnow()
    
    # Free up the slot
    if booking.slot_id:
        slot = db.query(ParkingSlot).filter(ParkingSlot.id == booking.slot_id).first()
        if slot:
            slot.status = SlotStatus.AVAILABLE
    
    db.commit()
    db.refresh(booking)
    
    return booking

