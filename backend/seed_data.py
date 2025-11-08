"""
Seed script to create sample data for testing
Run this to populate the database with sample data
"""

from app.core.database import SessionLocal, Base, engine
from app.models.user import User, UserRole
from app.models.parking_lot import ParkingLot
from app.models.parking_slot import ParkingSlot, SlotStatus
from app.core.security import get_password_hash
from datetime import datetime, timedelta

# Create tables
Base.metadata.create_all(bind=engine)

db = SessionLocal()

try:
    # Create admin user
    admin = User(
        email="admin@parking.com",
        full_name="Admin User",
        hashed_password=get_password_hash("admin123"),
        phone_number="+1234567890",
        role=UserRole.ADMIN,
        is_active=True,
        is_verified=True
    )
    db.add(admin)
    
    # Create parking owner
    owner = User(
        email="owner@parking.com",
        full_name="Parking Owner",
        hashed_password=get_password_hash("owner123"),
        phone_number="+1234567891",
        role=UserRole.PARKING_OWNER,
        is_active=True,
        is_verified=True
    )
    db.add(owner)
    
    # Create regular user
    user = User(
        email="user@example.com",
        full_name="Test User",
        hashed_password=get_password_hash("user123"),
        phone_number="+1234567892",
        role=UserRole.USER,
        is_active=True,
        is_verified=True
    )
    db.add(user)
    
    db.commit()
    db.refresh(admin)
    db.refresh(owner)
    db.refresh(user)
    
    print("✅ Created users:")
    print(f"   Admin: {admin.email} / admin123")
    print(f"   Owner: {owner.email} / owner123")
    print(f"   User: {user.email} / user123")
    
    # Create sample parking lots with Indian prices (₹60-₹200)
    parking_lot1 = ParkingLot(
        name="Connaught Place Parking",
        address="123 Connaught Place",
        city="New Delhi",
        state="Delhi",
        zip_code="110001",
        latitude=28.6139,
        longitude=77.2090,
        price_per_hour=80.0,
        description="Premium parking in the heart of Delhi with 24/7 security",
        image_url="https://example.com/parking1.jpg",
        camera_url="https://example.com/camera1/feed",
        total_slots=50,
        available_slots=35,
        safety_rating=4.5,
        total_reviews=120,
        owner_id=owner.id,
        is_active=True
    )
    db.add(parking_lot1)
    
    parking_lot2 = ParkingLot(
        name="Phoenix Mall Parking",
        address="456 MG Road",
        city="Mumbai",
        state="Maharashtra",
        zip_code="400001",
        latitude=19.0760,
        longitude=72.8777,
        price_per_hour=60.0,
        description="Affordable parking near shopping mall with easy access",
        image_url="https://example.com/parking2.jpg",
        camera_url="https://example.com/camera2/feed",
        total_slots=200,
        available_slots=150,
        safety_rating=4.2,
        total_reviews=85,
        owner_id=owner.id,
        is_active=True
    )
    db.add(parking_lot2)
    
    parking_lot3 = ParkingLot(
        name="Airport Express Parking",
        address="789 Airport Road",
        city="Bangalore",
        state="Karnataka",
        zip_code="560001",
        latitude=12.9716,
        longitude=77.5946,
        price_per_hour=150.0,
        description="Secure parking near airport with shuttle service and CCTV",
        image_url="https://example.com/parking3.jpg",
        camera_url="https://example.com/camera3/feed",
        total_slots=100,
        available_slots=60,
        safety_rating=4.8,
        total_reviews=200,
        owner_id=owner.id,
        is_active=True
    )
    db.add(parking_lot3)
    
    parking_lot4 = ParkingLot(
        name="Marina Beach Parking",
        address="321 Beach Road",
        city="Chennai",
        state="Tamil Nadu",
        zip_code="600001",
        latitude=13.0475,
        longitude=80.2837,
        price_per_hour=70.0,
        description="Seaside parking with beautiful views and good security",
        image_url="https://example.com/parking4.jpg",
        camera_url="https://example.com/camera4/feed",
        total_slots=75,
        available_slots=50,
        safety_rating=4.3,
        total_reviews=95,
        owner_id=owner.id,
        is_active=True
    )
    db.add(parking_lot4)
    
    parking_lot5 = ParkingLot(
        name="IT Park Premium Parking",
        address="555 Tech Park",
        city="Hyderabad",
        state="Telangana",
        zip_code="500001",
        latitude=17.3850,
        longitude=78.4867,
        price_per_hour=120.0,
        description="Premium parking in IT hub with EV charging stations",
        image_url="https://example.com/parking5.jpg",
        camera_url="https://example.com/camera5/feed",
        total_slots=120,
        available_slots=80,
        safety_rating=4.7,
        total_reviews=150,
        owner_id=owner.id,
        is_active=True
    )
    db.add(parking_lot5)
    
    parking_lot6 = ParkingLot(
        name="Heritage City Parking",
        address="789 Old City",
        city="Jaipur",
        state="Rajasthan",
        zip_code="302001",
        latitude=26.9124,
        longitude=75.7873,
        price_per_hour=65.0,
        description="Budget-friendly parking near heritage sites",
        image_url="https://example.com/parking6.jpg",
        camera_url="https://example.com/camera6/feed",
        total_slots=90,
        available_slots=65,
        safety_rating=4.1,
        total_reviews=70,
        owner_id=owner.id,
        is_active=True
    )
    db.add(parking_lot6)
    
    db.commit()
    db.refresh(parking_lot1)
    db.refresh(parking_lot2)
    db.refresh(parking_lot3)
    db.refresh(parking_lot4)
    db.refresh(parking_lot5)
    db.refresh(parking_lot6)
    
    print("\n✅ Created parking lots:")
    print(f"   1. {parking_lot1.name} - {parking_lot1.city} (₹{parking_lot1.price_per_hour}/hr)")
    print(f"   2. {parking_lot2.name} - {parking_lot2.city} (₹{parking_lot2.price_per_hour}/hr)")
    print(f"   3. {parking_lot3.name} - {parking_lot3.city} (₹{parking_lot3.price_per_hour}/hr)")
    print(f"   4. {parking_lot4.name} - {parking_lot4.city} (₹{parking_lot4.price_per_hour}/hr)")
    print(f"   5. {parking_lot5.name} - {parking_lot5.city} (₹{parking_lot5.price_per_hour}/hr)")
    print(f"   6. {parking_lot6.name} - {parking_lot6.city} (₹{parking_lot6.price_per_hour}/hr)")
    
    # Create sample parking slots for lot 1
    for i in range(1, 51):
        status = SlotStatus.AVAILABLE if i > 15 else SlotStatus.OCCUPIED
        slot = ParkingSlot(
            parking_lot_id=parking_lot1.id,
            slot_number=f"A{i}",
            status=status,
            is_disabled=(i % 10 == 0),
            is_ev_charging=(i % 5 == 0)
        )
        db.add(slot)
    
    # Create sample parking slots for lot 2
    for i in range(1, 201):
        status = SlotStatus.AVAILABLE if i > 50 else SlotStatus.OCCUPIED
        slot = ParkingSlot(
            parking_lot_id=parking_lot2.id,
            slot_number=f"B{i}",
            status=status,
            is_disabled=(i % 20 == 0),
            is_ev_charging=(i % 10 == 0)
        )
        db.add(slot)
    
    # Create sample parking slots for lot 3
    for i in range(1, 101):
        status = SlotStatus.AVAILABLE if i > 40 else SlotStatus.OCCUPIED
        slot = ParkingSlot(
            parking_lot_id=parking_lot3.id,
            slot_number=f"C{i}",
            status=status,
            is_disabled=(i % 15 == 0),
            is_ev_charging=(i % 8 == 0)
        )
        db.add(slot)
    
    # Create sample parking slots for lot 4
    for i in range(1, 76):
        status = SlotStatus.AVAILABLE if i > 25 else SlotStatus.OCCUPIED
        slot = ParkingSlot(
            parking_lot_id=parking_lot4.id,
            slot_number=f"D{i}",
            status=status,
            is_disabled=(i % 12 == 0),
            is_ev_charging=(i % 6 == 0)
        )
        db.add(slot)
    
    # Create sample parking slots for lot 5
    for i in range(1, 121):
        status = SlotStatus.AVAILABLE if i > 40 else SlotStatus.OCCUPIED
        slot = ParkingSlot(
            parking_lot_id=parking_lot5.id,
            slot_number=f"E{i}",
            status=status,
            is_disabled=(i % 15 == 0),
            is_ev_charging=(i % 7 == 0)
        )
        db.add(slot)
    
    # Create sample parking slots for lot 6
    for i in range(1, 91):
        status = SlotStatus.AVAILABLE if i > 25 else SlotStatus.OCCUPIED
        slot = ParkingSlot(
            parking_lot_id=parking_lot6.id,
            slot_number=f"F{i}",
            status=status,
            is_disabled=(i % 12 == 0),
            is_ev_charging=(i % 6 == 0)
        )
        db.add(slot)
    
    db.commit()
    
    print("\n✅ Created parking slots:")
    print(f"   Parking Lot 1: 50 slots")
    print(f"   Parking Lot 2: 200 slots")
    print(f"   Parking Lot 3: 100 slots")
    print(f"   Parking Lot 4: 75 slots")
    print(f"   Parking Lot 5: 120 slots")
    print(f"   Parking Lot 6: 90 slots")
    
    print("\n🎉 Sample data created successfully!")
    print("\n📝 Login credentials:")
    print("   Admin: admin@parking.com / admin123")
    print("   Owner: owner@parking.com / owner123")
    print("   User: user@example.com / user123")
    
except Exception as e:
    print(f"❌ Error creating sample data: {e}")
    db.rollback()
finally:
    db.close()


