"""
Comprehensive system test script
Tests all endpoints and functionality
"""

import requests
import json
from datetime import datetime, timedelta
import sys

BASE_URL = "http://localhost:5000"

# Colors for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
NC = '\033[0m'  # No Color

class TestResults:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.tests = []
    
    def add_test(self, name, passed, message=""):
        self.tests.append({
            "name": name,
            "passed": passed,
            "message": message
        })
        if passed:
            self.passed += 1
            print(f"{GREEN}[PASSED]{NC}: {name}")
        else:
            self.failed += 1
            print(f"{RED}[FAILED]{NC}: {name}")
            if message:
                print(f"  {RED}Error: {message}{NC}")
    
    def print_summary(self):
        print("\n" + "=" * 60)
        print(f"{BLUE}Test Summary{NC}")
        print("=" * 60)
        print(f"{GREEN}Passed: {self.passed}{NC}")
        print(f"{RED}Failed: {self.failed}{NC}")
        print(f"Total: {self.passed + self.failed}")
        print("=" * 60)
        
        if self.failed > 0:
            print(f"\n{RED}Failed Tests:{NC}")
            for test in self.tests:
                if not test["passed"]:
                    print(f"  - {test['name']}: {test['message']}")
        
        return self.failed == 0

results = TestResults()

def test_endpoint(method, endpoint, description, data=None, headers=None, expected_status=200):
    """Test an API endpoint"""
    try:
        url = f"{BASE_URL}{endpoint}"
        
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=5)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers, timeout=5)
        elif method == "PUT":
            response = requests.put(url, json=data, headers=headers, timeout=5)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers, timeout=5)
        else:
            results.add_test(description, False, f"Unknown method: {method}")
            return None
        
        if response.status_code == expected_status:
            results.add_test(description, True)
            try:
                return response.json()
            except:
                return response.text
        else:
            results.add_test(description, False, 
                f"Expected {expected_status}, got {response.status_code}: {response.text[:100]}")
            return None
    
    except requests.exceptions.ConnectionError:
        results.add_test(description, False, "Cannot connect to server. Is it running?")
        return None
    except Exception as e:
        results.add_test(description, False, str(e))
        return None

print(f"{BLUE}{'='*60}{NC}")
print(f"{BLUE}Smart Parking System - Comprehensive Test Suite{NC}")
print(f"{BLUE}{'='*60}{NC}\n")

# Test 1: Health Check
print(f"{YELLOW}1. Health & Status Checks{NC}")
print("-" * 60)
test_endpoint("GET", "/health", "Health check endpoint")
test_endpoint("GET", "/", "Root endpoint")
test_endpoint("GET", "/api/docs", "Swagger UI documentation")

# Test 2: Authentication
print(f"\n{YELLOW}2. Authentication Tests{NC}")
print("-" * 60)

# Register user
register_data = {
    "email": f"testuser_{datetime.now().timestamp()}@example.com",
    "password": "test123",
    "full_name": "Test User",
    "phone_number": "+1234567890"
}
register_response = test_endpoint("POST", "/api/v1/auth/register", "User registration", register_data)
user_email = register_data["email"]

if register_response:
    # Login
    login_response = test_endpoint("POST", "/api/v1/auth/login", "User login",
        data={"username": user_email, "password": "test123"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        expected_status=200)
    
    token = None
    if login_response and "access_token" in login_response:
        token = login_response["access_token"]
        auth_headers = {"Authorization": f"Bearer {token}"}
        
        # Get current user
        test_endpoint("GET", "/api/v1/users/me", "Get current user", headers=auth_headers)
        
        # Test 3: Parking Lots
        print(f"\n{YELLOW}3. Parking Lots Tests{NC}")
        print("-" * 60)
        
        # Get all parking lots
        lots_response = test_endpoint("GET", "/api/v1/parking-lots/", "Get all parking lots")
        
        # Get nearby parking lots
        test_endpoint("GET", "/api/v1/parking-lots/nearby?latitude=40.7128&longitude=-74.0060&radius_km=5", 
                     "Get nearby parking lots")
        
        # Create parking lot (admin required, will fail for regular user)
        lot_data = {
            "name": "Test Parking Lot",
            "address": "123 Test Street",
            "city": "Test City",
            "state": "TS",
            "zip_code": "12345",
            "latitude": 40.7128,
            "longitude": -74.0060,
            "price_per_hour": 5.0,
            "description": "Test parking lot"
        }
        create_lot_response = test_endpoint("POST", "/api/v1/parking-lots/", 
                                           "Create parking lot (should fail - not admin)", 
                                           lot_data, auth_headers, expected_status=403)
        
        # Test 4: Bookings
        print(f"\n{YELLOW}4. Booking Tests{NC}")
        print("-" * 60)
        
        # Get user's bookings
        test_endpoint("GET", "/api/v1/bookings/", "Get user bookings", headers=auth_headers)
        
        # Test 5: Safety Ratings
        print(f"\n{YELLOW}5. Safety Ratings Tests{NC}")
        print("-" * 60)
        
        # Get safety rating (will fail if no parking lot exists)
        test_endpoint("GET", "/api/v1/safety/1", "Get safety rating")
        
        # Test 6: Analytics
        print(f"\n{YELLOW}6. Analytics Tests{NC}")
        print("-" * 60)
        
        # Get dashboard analytics
        test_endpoint("GET", "/api/v1/analytics/dashboard", "Get dashboard analytics", headers=auth_headers)
        
        # Test 7: Parking Slots
        print(f"\n{YELLOW}7. Parking Slots Tests{NC}")
        print("-" * 60)
        
        # Get parking slots
        test_endpoint("GET", "/api/v1/parking-slots/?parking_lot_id=1", "Get parking slots")
        
    else:
        print(f"{RED}⚠ Cannot continue tests - login failed{NC}")
else:
    print(f"{RED}⚠ Cannot continue tests - registration failed{NC}")

# Test 8: API Documentation
print(f"\n{YELLOW}8. API Documentation Tests{NC}")
print("-" * 60)
test_endpoint("GET", "/api/docs", "Swagger UI")
test_endpoint("GET", "/api/redoc", "ReDoc documentation")

# Test 9: Error Handling
print(f"\n{YELLOW}9. Error Handling Tests{NC}")
print("-" * 60)
test_endpoint("GET", "/api/v1/parking-lots/99999", "Get non-existent parking lot", expected_status=404)
test_endpoint("GET", "/api/v1/bookings/99999", "Get non-existent booking", 
             headers=auth_headers if 'auth_headers' in locals() else None, expected_status=404)

# Test 10: Invalid Requests
print(f"\n{YELLOW}10. Invalid Request Tests{NC}")
print("-" * 60)
test_endpoint("POST", "/api/v1/auth/login", "Login with invalid credentials",
             data={"username": "invalid@example.com", "password": "wrong"},
             headers={"Content-Type": "application/x-www-form-urlencoded"},
             expected_status=401)

# Print summary
print("\n")
success = results.print_summary()

# Exit with appropriate code
if success:
    print(f"\n{GREEN}✅ All tests passed! System is working correctly.{NC}\n")
    sys.exit(0)
else:
    print(f"\n{RED}❌ Some tests failed. Please check the errors above.{NC}\n")
    sys.exit(1)

