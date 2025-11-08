"""
Simple system test - checks if server is running and tests basic endpoints
"""

import requests
import sys
import json

BASE_URL = "http://localhost:5000"

def test_endpoint(method, endpoint, description):
    """Test an endpoint"""
    try:
        url = f"{BASE_URL}{endpoint}"
        
        if method == "GET":
            response = requests.get(url, timeout=5)
        elif method == "POST":
            response = requests.post(url, timeout=5)
        else:
            print(f"[FAILED] {description} - Unknown method")
            return False
        
        if response.status_code < 400:
            print(f"[PASSED] {description} - Status: {response.status_code}")
            return True
        else:
            print(f"[FAILED] {description} - Status: {response.status_code}")
            return False
    
    except requests.exceptions.ConnectionError:
        print(f"[FAILED] {description} - Cannot connect to server")
        print("  ERROR: Server is not running!")
        print("  Please start the server with: python -m uvicorn main:app --reload --port 5000")
        return False
    except Exception as e:
        print(f"[FAILED] {description} - Error: {str(e)}")
        return False

print("=" * 60)
print("Smart Parking System - System Test")
print("=" * 60)
print()

# Check if server is running
print("Checking if server is running...")
try:
    response = requests.get(f"{BASE_URL}/health", timeout=2)
    print("[PASSED] Server is running!")
    print()
except:
    print("[FAILED] Server is not running!")
    print()
    print("Please start the server first:")
    print("  cd backend")
    print("  python -m uvicorn main:app --reload --port 5000")
    print()
    sys.exit(1)

# Test endpoints
print("Testing Endpoints:")
print("-" * 60)

passed = 0
failed = 0

# Health check
if test_endpoint("GET", "/health", "Health check"):
    passed += 1
else:
    failed += 1

# Root endpoint
if test_endpoint("GET", "/", "Root endpoint"):
    passed += 1
else:
    failed += 1

# API docs
if test_endpoint("GET", "/api/docs", "Swagger UI"):
    passed += 1
else:
    failed += 1

# Get parking lots
if test_endpoint("GET", "/api/v1/parking-lots/", "Get parking lots"):
    passed += 1
else:
    failed += 1

# Get nearby parking lots
if test_endpoint("GET", "/api/v1/parking-lots/nearby?latitude=40.7128&longitude=-74.0060&radius_km=5", "Get nearby parking lots"):
    passed += 1
else:
    failed += 1

# Test registration
print()
print("Testing Authentication:")
print("-" * 60)

try:
    register_data = {
        "email": f"test_{hash(str(__import__('time').time()))}@example.com",
        "password": "test123",
        "full_name": "Test User"
    }
    response = requests.post(f"{BASE_URL}/api/v1/auth/register", json=register_data, timeout=5)
    if response.status_code == 201:
        print("[PASSED] User registration - Status: 201")
        passed += 1
        user_email = register_data["email"]
        
        # Test login
        login_response = requests.post(
            f"{BASE_URL}/api/v1/auth/login",
            data={"username": user_email, "password": "test123"},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=5
        )
        if login_response.status_code == 200:
            print("[PASSED] User login - Status: 200")
            passed += 1
            token = login_response.json().get("access_token")
            
            if token:
                headers = {"Authorization": f"Bearer {token}"}
                
                # Test protected endpoint
                user_response = requests.get(f"{BASE_URL}/api/v1/users/me", headers=headers, timeout=5)
                if user_response.status_code == 200:
                    print("[PASSED] Get current user - Status: 200")
                    passed += 1
                else:
                    print(f"[FAILED] Get current user - Status: {user_response.status_code}")
                    failed += 1
        else:
            print(f"[FAILED] User login - Status: {login_response.status_code}")
            failed += 1
    else:
        print(f"[FAILED] User registration - Status: {response.status_code}")
        failed += 1
except Exception as e:
    print(f"[FAILED] Authentication test - Error: {str(e)}")
    failed += 1

print()
print("=" * 60)
print("Test Summary:")
print("=" * 60)
print(f"Passed: {passed}")
print(f"Failed: {failed}")
print(f"Total: {passed + failed}")
print("=" * 60)

if failed == 0:
    print()
    print("SUCCESS: All tests passed! System is working correctly.")
    sys.exit(0)
else:
    print()
    print("WARNING: Some tests failed. Check the errors above.")
    sys.exit(1)

