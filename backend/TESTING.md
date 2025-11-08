# Backend Testing Guide

## Running Tests

### Option 1: Using Pytest (Recommended)

```bash
# Install test dependencies
pip install -r requirements-test.txt

# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_auth.py

# Run specific test
pytest tests/test_auth.py::test_login_success

# Run with verbose output
pytest -v
```

### Option 2: Using the Test Script

```bash
# Run all tests
python run_tests.py
```

### Option 3: Manual API Testing

**Windows:**
```bash
test_api.bat
```

**Mac/Linux:**
```bash
chmod +x test_api.sh
./test_api.sh
```

## Test Coverage

The test suite includes:

### ✅ Authentication Tests
- User registration
- Login/logout
- Token validation
- Protected endpoints

### ✅ Parking Lots Tests
- CRUD operations
- Location-based search
- Filtering
- Permissions

### ✅ Parking Slots Tests
- Slot management
- Status updates
- Availability tracking

### ✅ Booking Tests
- Booking creation
- Time validation
- Conflict detection
- Booking lifecycle

### ✅ Safety Ratings Tests
- Review submission
- Rating aggregation
- Duplicate prevention

### ✅ Analytics Tests
- Dashboard statistics
- Revenue tracking
- Occupancy rates

### ✅ Integration Tests
- Complete workflows
- End-to-end scenarios

## Test Structure

```
tests/
├── conftest.py          # Test fixtures
├── test_auth.py         # Authentication tests
├── test_parking_lots.py # Parking lots tests
├── test_parking_slots.py # Parking slots tests
├── test_bookings.py     # Booking tests
├── test_safety.py       # Safety ratings tests
├── test_analytics.py    # Analytics tests
└── test_integration.py # Integration tests
```

## Writing New Tests

1. Create test file: `tests/test_feature.py`
2. Import fixtures from `conftest.py`
3. Write test functions starting with `test_`
4. Use assertions to verify behavior

Example:
```python
def test_my_feature(client, auth_headers):
    response = client.get("/api/v1/my-endpoint", headers=auth_headers)
    assert response.status_code == 200
    assert "expected_data" in response.json()
```

## Continuous Testing

Tests run automatically on:
- Code changes (with pytest-watch)
- Before commits (pre-commit hooks)
- CI/CD pipeline

## Test Database

Tests use an in-memory SQLite database that's:
- Created fresh for each test
- Isolated from other tests
- Automatically cleaned up

## Coverage Reports

View coverage report:
```bash
pytest --cov=app --cov-report=html
open htmlcov/index.html  # Mac/Linux
start htmlcov/index.html  # Windows
```


