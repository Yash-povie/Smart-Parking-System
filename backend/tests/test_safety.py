"""
Tests for safety ratings endpoints
"""

import pytest
from fastapi import status


def test_get_safety_rating(client, test_parking_lot):
    """Test getting safety rating"""
    response = client.get(f"/api/v1/safety/{test_parking_lot.id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "parking_lot_id" in data
    assert "safety_score" in data


def test_submit_safety_review(client, test_user, test_parking_lot, auth_headers):
    """Test submitting safety review"""
    response = client.post(
        f"/api/v1/safety/{test_parking_lot.id}/review",
        json={
            "safety_rating": 4.5,
            "lighting_rating": 4.0,
            "security_rating": 5.0,
            "cleanliness_rating": 4.5,
            "review_text": "Great parking lot!"
        },
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["safety_rating"] == 4.5
    assert data["parking_lot_id"] == test_parking_lot.id


def test_submit_duplicate_review(client, test_user, test_parking_lot, auth_headers, db):
    """Test submitting duplicate review"""
    from app.models.safety_review import SafetyReview
    
    # Create first review
    review = SafetyReview(
        user_id=test_user.id,
        parking_lot_id=test_parking_lot.id,
        safety_rating=4.0
    )
    db.add(review)
    db.commit()
    
    # Try to submit another review
    response = client.post(
        f"/api/v1/safety/{test_parking_lot.id}/review",
        json={
            "safety_rating": 5.0
        },
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


