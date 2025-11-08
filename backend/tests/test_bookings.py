"""
Tests for booking endpoints
"""

import pytest
from fastapi import status
from datetime import datetime, timedelta


def test_create_booking(client, test_user, test_parking_lot, auth_headers):
    """Test creating a booking"""
    start_time = datetime.utcnow() + timedelta(hours=1)
    end_time = start_time + timedelta(hours=2)
    
    response = client.post(
        "/api/v1/bookings/",
        json={
            "parking_lot_id": test_parking_lot.id,
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "vehicle_number": "ABC123"
        },
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["parking_lot_id"] == test_parking_lot.id
    assert data["user_id"] == test_user.id
    assert data["status"] == "pending"


def test_create_booking_invalid_time(client, test_parking_lot, auth_headers):
    """Test creating booking with invalid time range"""
    start_time = datetime.utcnow() + timedelta(hours=1)
    end_time = start_time - timedelta(hours=1)  # End before start
    
    response = client.post(
        "/api/v1/bookings/",
        json={
            "parking_lot_id": test_parking_lot.id,
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat()
        },
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_get_bookings(client, test_user, auth_headers):
    """Test getting user's bookings"""
    response = client.get(
        "/api/v1/bookings/",
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


def test_get_booking_by_id(client, test_user, test_parking_lot, auth_headers, db):
    """Test getting booking by ID"""
    from app.models.booking import Booking, BookingStatus
    from datetime import datetime, timedelta
    
    booking = Booking(
        user_id=test_user.id,
        parking_lot_id=test_parking_lot.id,
        start_time=datetime.utcnow() + timedelta(hours=1),
        end_time=datetime.utcnow() + timedelta(hours=3),
        price_per_hour=test_parking_lot.price_per_hour,
        total_price=test_parking_lot.price_per_hour * 2,
        status=BookingStatus.PENDING
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    
    response = client.get(
        f"/api/v1/bookings/{booking.id}",
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == booking.id


def test_cancel_booking(client, test_user, test_parking_lot, auth_headers, db):
    """Test canceling a booking"""
    from app.models.booking import Booking, BookingStatus
    from datetime import datetime, timedelta
    
    booking = Booking(
        user_id=test_user.id,
        parking_lot_id=test_parking_lot.id,
        start_time=datetime.utcnow() + timedelta(hours=1),
        end_time=datetime.utcnow() + timedelta(hours=3),
        price_per_hour=test_parking_lot.price_per_hour,
        total_price=test_parking_lot.price_per_hour * 2,
        status=BookingStatus.PENDING
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    
    response = client.post(
        f"/api/v1/bookings/{booking.id}/cancel",
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "cancelled"


