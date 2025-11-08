"""
Tests for parking slots endpoints
"""

import pytest
from fastapi import status


def test_get_parking_slots(client, test_parking_lot):
    """Test getting parking slots for a parking lot"""
    response = client.get(
        "/api/v1/parking-slots/",
        params={"parking_lot_id": test_parking_lot.id}
    )
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


def test_get_parking_slot_by_id(client, test_parking_lot, db):
    """Test getting parking slot by ID"""
    from app.models.parking_slot import ParkingSlot, SlotStatus
    
    slot = ParkingSlot(
        parking_lot_id=test_parking_lot.id,
        slot_number="A1",
        status=SlotStatus.AVAILABLE
    )
    db.add(slot)
    db.commit()
    db.refresh(slot)
    
    response = client.get(f"/api/v1/parking-slots/{slot.id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == slot.id
    assert data["slot_number"] == "A1"


def test_create_parking_slot(client, test_parking_lot, admin_headers):
    """Test creating parking slot"""
    response = client.post(
        "/api/v1/parking-slots/",
        json={
            "parking_lot_id": test_parking_lot.id,
            "slot_number": "B1",
            "is_disabled": False,
            "is_ev_charging": True
        },
        headers=admin_headers
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["slot_number"] == "B1"
    assert data["is_ev_charging"] == True


