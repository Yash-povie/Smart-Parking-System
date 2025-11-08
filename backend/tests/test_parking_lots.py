"""
Tests for parking lots endpoints
"""

import pytest
from fastapi import status


def test_get_parking_lots(client):
    """Test getting all parking lots"""
    response = client.get("/api/v1/parking-lots/")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


def test_get_parking_lot_by_id(client, test_parking_lot):
    """Test getting parking lot by ID"""
    response = client.get(f"/api/v1/parking-lots/{test_parking_lot.id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == test_parking_lot.id
    assert data["name"] == test_parking_lot.name


def test_get_parking_lot_not_found(client):
    """Test getting non-existent parking lot"""
    response = client.get("/api/v1/parking-lots/99999")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_create_parking_lot(client, admin_headers):
    """Test creating parking lot as admin"""
    response = client.post(
        "/api/v1/parking-lots/",
        json={
            "name": "New Parking Lot",
            "address": "456 New Street",
            "city": "New City",
            "state": "NC",
            "zip_code": "54321",
            "latitude": 40.7580,
            "longitude": -73.9855,
            "price_per_hour": 6.0,
            "description": "New parking lot"
        },
        headers=admin_headers
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == "New Parking Lot"
    assert data["price_per_hour"] == 6.0


def test_create_parking_lot_unauthorized(client, auth_headers):
    """Test creating parking lot without admin access"""
    response = client.post(
        "/api/v1/parking-lots/",
        json={
            "name": "New Parking Lot",
            "address": "456 New Street",
            "city": "New City",
            "state": "NC",
            "zip_code": "54321",
            "latitude": 40.7580,
            "longitude": -73.9855,
            "price_per_hour": 6.0
        },
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_update_parking_lot(client, test_parking_lot, admin_headers):
    """Test updating parking lot"""
    response = client.put(
        f"/api/v1/parking-lots/{test_parking_lot.id}",
        json={
            "name": "Updated Parking Lot",
            "price_per_hour": 7.0
        },
        headers=admin_headers
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "Updated Parking Lot"
    assert data["price_per_hour"] == 7.0


def test_delete_parking_lot(client, test_parking_lot, admin_headers):
    """Test deleting parking lot"""
    response = client.delete(
        f"/api/v1/parking-lots/{test_parking_lot.id}",
        headers=admin_headers
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_get_nearby_parking_lots(client, test_parking_lot):
    """Test getting nearby parking lots"""
    response = client.get(
        "/api/v1/parking-lots/nearby",
        params={
            "latitude": 40.7128,
            "longitude": -74.0060,
            "radius_km": 5.0
        }
    )
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


