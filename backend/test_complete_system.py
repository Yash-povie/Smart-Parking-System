"""
Complete System Test - Tests everything works
"""

import requests
import json
import sys

BASE_URL = "http://localhost:5000"

print("=" * 70)
print("COMPLETE SYSTEM TEST - Smart Parking System")
print("=" * 70)
print()

# Test Results
results = {"passed": [], "failed": []}

def test(name, func):
    """Run a test"""
    try:
        result = func()
        if result:
            results["passed"].append(name)
            print(f"[PASS] {name}")
        else:
            results["failed"].append(name)
            print(f"[FAIL] {name}")
    except Exception as e:
        results["failed"].append(name)
        print(f"[FAIL] {name} - Error: {str(e)}")

# 1. Server Health
print("1. SERVER HEALTH")
print("-" * 70)
test("Server is running", lambda: requests.get(f"{BASE_URL}/health", timeout=2).status_code == 200)
test("Root endpoint works", lambda: requests.get(f"{BASE_URL}/", timeout=2).status_code == 200)
test("API docs accessible", lambda: requests.get(f"{BASE_URL}/api/docs", timeout=2).status_code == 200)

# 2. Authentication
print("\n2. AUTHENTICATION")
print("-" * 70)
token = None
user_email = f"testuser_{hash(str(__import__('time').time()))}@example.com"

def test_register():
    global user_email
    response = requests.post(
        f"{BASE_URL}/api/v1/auth/register",
        json={
            "email": user_email,
            "password": "test123",
            "full_name": "Test User",
            "phone_number": "+1234567890"
        },
        timeout=5
    )
    return response.status_code in [200, 201]

def test_login():
    global token, user_email
    response = requests.post(
        f"{BASE_URL}/api/v1/auth/login",
        data={"username": user_email, "password": "test123"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=5
    )
    if response.status_code == 200:
        data = response.json()
        token = data.get("access_token")
        return token is not None
    return False

test("User registration", test_register)
test("User login", test_login)

auth_headers = {"Authorization": f"Bearer {token}"} if token else None

# 3. Parking Lots (Public)
print("\n3. PARKING LOTS (Public Endpoints)")
print("-" * 70)
test("Get all parking lots", lambda: requests.get(f"{BASE_URL}/api/v1/parking-lots/", timeout=5).status_code == 200)
test("Get nearby parking lots", lambda: requests.get(f"{BASE_URL}/api/v1/parking-lots/nearby?latitude=40.7128&longitude=-74.0060&radius_km=5", timeout=5).status_code == 200)
test("Get parking lot by ID (if exists)", lambda: requests.get(f"{BASE_URL}/api/v1/parking-lots/1", timeout=5).status_code in [200, 404])

# 4. Parking Slots
print("\n4. PARKING SLOTS")
print("-" * 70)
test("Get parking slots", lambda: requests.get(f"{BASE_URL}/api/v1/parking-slots/?parking_lot_id=1", timeout=5).status_code in [200, 404])

# 5. Safety Ratings
print("\n5. SAFETY RATINGS")
print("-" * 70)
test("Get safety rating", lambda: requests.get(f"{BASE_URL}/api/v1/safety/1", timeout=5).status_code in [200, 404])

# 6. Protected Endpoints (if authenticated)
if auth_headers:
    print("\n6. PROTECTED ENDPOINTS (Authenticated)")
    print("-" * 70)
    test("Get current user", lambda: requests.get(f"{BASE_URL}/api/v1/users/me", headers=auth_headers, timeout=5).status_code == 200)
    test("Get user bookings", lambda: requests.get(f"{BASE_URL}/api/v1/bookings/", headers=auth_headers, timeout=5).status_code == 200)
    test("Get dashboard analytics", lambda: requests.get(f"{BASE_URL}/api/v1/analytics/dashboard", headers=auth_headers, timeout=5).status_code == 200)
else:
    print("\n6. PROTECTED ENDPOINTS")
    print("-" * 70)
    print("[SKIP] Authentication required - login test failed")

# 7. Error Handling
print("\n7. ERROR HANDLING")
print("-" * 70)
test("404 for non-existent resource", lambda: requests.get(f"{BASE_URL}/api/v1/parking-lots/99999", timeout=5).status_code == 404)
test("401 for protected endpoint without auth", lambda: requests.get(f"{BASE_URL}/api/v1/users/me", timeout=5).status_code == 401)

# Summary
print("\n" + "=" * 70)
print("TEST SUMMARY")
print("=" * 70)
print(f"Passed: {len(results['passed'])}")
print(f"Failed: {len(results['failed'])}")
print(f"Total: {len(results['passed']) + len(results['failed'])}")
print()

if results['failed']:
    print("Failed Tests:")
    for test_name in results['failed']:
        print(f"  - {test_name}")
    print()

if len(results['failed']) == 0:
    print("SUCCESS: All tests passed! System is fully operational.")
    print()
    print("Next Steps:")
    print("  1. Visit http://localhost:5000/api/docs to explore the API")
    print("  2. Create sample data: python seed_data.py")
    print("  3. Start AI service: cd ai-service && python app.py")
    print("  4. Build frontend: cd frontend && npm run dev")
    sys.exit(0)
else:
    print("WARNING: Some tests failed. System may have issues.")
    print("Check the errors above and ensure the server is running correctly.")
    sys.exit(1)

