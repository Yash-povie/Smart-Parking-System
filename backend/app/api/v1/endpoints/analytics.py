"""
Analytics endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from typing import Optional
from datetime import datetime, timedelta

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.booking import Booking, BookingStatus
from app.models.parking_lot import ParkingLot
from app.models.parking_slot import ParkingSlot, SlotStatus

router = APIRouter()


@router.get("/dashboard")
async def get_dashboard_analytics(
    parking_lot_id: Optional[int] = None,
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get dashboard analytics"""
    # Check permissions
    if current_user.role not in ["admin", "parking_owner"]:
        # Regular users can only see their own analytics
        parking_lot_id = None
    
    # Base query
    query = db.query(Booking)
    
    # Filter by parking lot if specified
    if parking_lot_id:
        # Verify ownership
        parking_lot = db.query(ParkingLot).filter(ParkingLot.id == parking_lot_id).first()
        if not parking_lot:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Parking lot not found"
            )
        
        if current_user.role != "admin" and parking_lot.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        
        query = query.filter(Booking.parking_lot_id == parking_lot_id)
    elif current_user.role == "user":
        # Regular users see only their bookings
        query = query.filter(Booking.user_id == current_user.id)
    
    # Date range
    start_date = datetime.utcnow() - timedelta(days=days)
    query = query.filter(Booking.created_at >= start_date)
    
    # Total bookings
    total_bookings = query.count()
    
    # Completed bookings
    completed_bookings = query.filter(Booking.status == BookingStatus.COMPLETED).count()
    
    # Revenue
    revenue = db.query(func.sum(Booking.total_price)).filter(
        and_(
            Booking.status == BookingStatus.COMPLETED,
            Booking.payment_status == "paid",
            Booking.created_at >= start_date
        )
    ).scalar() or 0.0
    
    # Occupancy rate
    if parking_lot_id:
        parking_lot = db.query(ParkingLot).filter(ParkingLot.id == parking_lot_id).first()
        total_slots = parking_lot.total_slots if parking_lot else 0
        occupied_slots = db.query(ParkingSlot).filter(
            and_(
                ParkingSlot.parking_lot_id == parking_lot_id,
                ParkingSlot.status == SlotStatus.OCCUPIED
            )
        ).count()
        occupancy_rate = (occupied_slots / total_slots * 100) if total_slots > 0 else 0
    else:
        occupancy_rate = None
    
    # Active bookings
    active_bookings = query.filter(Booking.status == BookingStatus.ACTIVE).count()
    
    # Pending bookings
    pending_bookings = query.filter(Booking.status == BookingStatus.PENDING).count()
    
    return {
        "total_bookings": total_bookings,
        "completed_bookings": completed_bookings,
        "active_bookings": active_bookings,
        "pending_bookings": pending_bookings,
        "revenue": float(revenue),
        "occupancy_rate": occupancy_rate,
        "period_days": days,
        "start_date": start_date.isoformat()
    }


@router.get("/parking-lot/{parking_lot_id}/stats")
async def get_parking_lot_stats(
    parking_lot_id: int,
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get detailed statistics for a parking lot"""
    parking_lot = db.query(ParkingLot).filter(ParkingLot.id == parking_lot_id).first()
    
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
    
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # Booking statistics
    bookings = db.query(Booking).filter(
        and_(
            Booking.parking_lot_id == parking_lot_id,
            Booking.created_at >= start_date
        )
    )
    
    total_bookings = bookings.count()
    completed = bookings.filter(Booking.status == BookingStatus.COMPLETED).count()
    revenue = db.query(func.sum(Booking.total_price)).filter(
        and_(
            Booking.parking_lot_id == parking_lot_id,
            Booking.status == BookingStatus.COMPLETED,
            Booking.payment_status == "paid",
            Booking.created_at >= start_date
        )
    ).scalar() or 0.0
    
    # Slot statistics
    total_slots = parking_lot.total_slots
    available_slots = db.query(ParkingSlot).filter(
        and_(
            ParkingSlot.parking_lot_id == parking_lot_id,
            ParkingSlot.status == SlotStatus.AVAILABLE
        )
    ).count()
    occupied_slots = db.query(ParkingSlot).filter(
        and_(
            ParkingSlot.parking_lot_id == parking_lot_id,
            ParkingSlot.status == SlotStatus.OCCUPIED
        )
    ).count()
    
    occupancy_rate = (occupied_slots / total_slots * 100) if total_slots > 0 else 0
    
    return {
        "parking_lot_id": parking_lot_id,
        "parking_lot_name": parking_lot.name,
        "total_slots": total_slots,
        "available_slots": available_slots,
        "occupied_slots": occupied_slots,
        "occupancy_rate": occupancy_rate,
        "total_bookings": total_bookings,
        "completed_bookings": completed,
        "revenue": float(revenue),
        "average_booking_value": float(revenue / completed) if completed > 0 else 0,
        "safety_rating": parking_lot.safety_rating,
        "total_reviews": parking_lot.total_reviews,
        "period_days": days
    }

