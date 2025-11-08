"""
Pytest configuration and fixtures
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base, get_db
from app.core.config import settings
from main import app

# Create test database (in-memory SQLite)
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    """Create a fresh database for each test"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    """Create a test client"""
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(db):
    """Create a test user"""
    from app.models.user import User, UserRole
    from app.core.security import get_password_hash
    
    user = User(
        email="test@example.com",
        full_name="Test User",
        hashed_password=get_password_hash("test123"),
        phone_number="+1234567890",
        role=UserRole.USER,
        is_active=True,
        is_verified=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def test_admin(db):
    """Create a test admin user"""
    from app.models.user import User, UserRole
    from app.core.security import get_password_hash
    
    admin = User(
        email="admin@example.com",
        full_name="Admin User",
        hashed_password=get_password_hash("admin123"),
        phone_number="+1234567891",
        role=UserRole.ADMIN,
        is_active=True,
        is_verified=True
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin


@pytest.fixture
def auth_headers(client, test_user):
    """Get authentication headers for test user"""
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": test_user.email,
            "password": "test123"
        }
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def admin_headers(client, test_admin):
    """Get authentication headers for admin user"""
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": test_admin.email,
            "password": "admin123"
        }
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def test_parking_lot(db, test_admin):
    """Create a test parking lot"""
    from app.models.parking_lot import ParkingLot
    
    parking_lot = ParkingLot(
        name="Test Parking Lot",
        address="123 Test Street",
        city="Test City",
        state="TS",
        zip_code="12345",
        latitude=40.7128,
        longitude=-74.0060,
        price_per_hour=5.0,
        description="Test parking lot",
        total_slots=10,
        available_slots=5,
        owner_id=test_admin.id,
        is_active=True
    )
    db.add(parking_lot)
    db.commit()
    db.refresh(parking_lot)
    return parking_lot


