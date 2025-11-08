"""
Integration tests for complete workflows
"""

import pytest
from fastapi import status
from datetime import datetime, timedelta


def test_complete_booking_workflow(client, test_user, test_parking_lot, db, auth_headers):
    """Test complete booking workflow"""
    from app.models.parking_slot import ParkingSlot, SlotStatus
    from app.models.booking import Booking, BookingStatus
    
    # Create a parking slot
    slot = ParkingSlot(
        parking_lot_id=test_parking_lot.id,
        slot_number="A1",
        status=SlotStatus.AVAILABLE
    )
    db.add(slot)
    db.commit()
    db.refresh(slot)
    
    # Create booking
    start_time = datetime.utcnow() + timedelta(hours=1)
    end_time = start_time + timedelta(hours=2)
    
    booking_response = client.post(
        "/api/v1/bookings/",
        json={
            "parking_lot_id": test_parking_lot.id,
            "slot_id": slot.id,
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "vehicle_number": "TEST123"
        },
        headers=auth_headers
    )
    assert booking_response.status_code == status.HTTP_201_CREATED
    booking = booking_response.json()
    
    # Verify slot is reserved
    slot_response = client.get(f"/api/v1/parking-slots/{slot.id}")
    slot_data = slot_response.json()
    assert slot_data["status"] == "reserved"
    
    # Cancel booking
    cancel_response = client.post(
        f"/api/v1/bookings/{booking['id']}/cancel",
        headers=auth_headers
    )
    assert cancel_response.status_code == status.HTTP_200_OK
    
    # Verify slot is available again
    slot_response = client.get(f"/api/v1/parking-slots/{slot.id}")
    slot_data = slot_response.json()
    assert slot_data["status"] == "available"


def test_parking_lot_with_slots_workflow(client, admin_headers, db):
    """Test creating parking lot and adding slots"""
    from app.models.parking_lot import ParkingLot
    from app.models.parking_slot import ParkingSlot, SlotStatus
    
    # Create parking lot
    lot_response = client.post(
        "/api/v1/parking-lots/",
        json={
            "name": "Integration Test Lot",
            "address": "123 Test St",
            "city": "Test City",
            "state": "TS",
            "zip_code": "12345",
            "latitude": 40.7128,
            "longitude": -74.0060,
            "price_per_hour": 5.0
        },
        headers=admin_headers
    )
    assert lot_response.status_code == status.HTTP_201_CREATED
    lot = lot_response.json()
    
    # Create slots
    for i in range(1, 6):
        slot_response = client.post(
            "/api/v1/parking-slots/",
            json={
                "parking_lot_id": lot["id"],
                "slot_number": f"A{i}",
                "is_disabled": False,
                "is_ev_charging": (i % 2 == 0)
            },
            headers=admin_headers
        )
        assert slot_response.status_code == status.HTTP_201_CREATED
    
    # Verify slots were created
    slots_response = client.get(
        "/api/v1/parking-slots/",
        params={"parking_lot_id": lot["id"]}
    )
    assert slots_response.status_code == status.HTTP_200_OK
    slots = slots_response.json()
    assert len(slots) == 5


