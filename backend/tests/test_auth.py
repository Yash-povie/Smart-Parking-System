"""
Tests for authentication endpoints
"""

import pytest
from fastapi import status


def test_register_user(client):
    """Test user registration"""
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "newuser@example.com",
            "password": "password123",
            "full_name": "New User",
            "phone_number": "+1234567890"
        }
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert data["full_name"] == "New User"
    assert "id" in data
    assert "hashed_password" not in data


def test_register_duplicate_email(client, test_user):
    """Test registration with duplicate email"""
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": test_user.email,
            "password": "password123",
            "full_name": "Duplicate User"
        }
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_login_success(client, test_user):
    """Test successful login"""
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": test_user.email,
            "password": "test123"
        }
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials(client, test_user):
    """Test login with invalid credentials"""
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": test_user.email,
            "password": "wrongpassword"
        }
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_current_user(client, auth_headers):
    """Test getting current user"""
    response = client.get(
        "/api/v1/auth/me",
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "email" in data
    assert "full_name" in data


def test_get_current_user_unauthorized(client):
    """Test getting current user without token"""
    response = client.get("/api/v1/auth/me")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


