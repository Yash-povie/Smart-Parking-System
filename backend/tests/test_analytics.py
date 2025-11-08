"""
Tests for analytics endpoints
"""

import pytest
from fastapi import status


def test_get_dashboard_analytics(client, test_user, auth_headers):
    """Test getting dashboard analytics"""
    response = client.get(
        "/api/v1/analytics/dashboard",
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "total_bookings" in data
    assert "revenue" in data


def test_get_parking_lot_stats(client, test_parking_lot, admin_headers):
    """Test getting parking lot statistics"""
    response = client.get(
        f"/api/v1/analytics/parking-lot/{test_parking_lot.id}/stats",
        headers=admin_headers
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "parking_lot_id" in data
    assert "total_slots" in data
    assert "revenue" in data


