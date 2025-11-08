# Quick System Test Guide

## Test the Backend System

### Step 1: Start the Server

Make sure the backend server is running:

```bash
cd backend
python -m uvicorn main:app --reload --port 5000
```

You should see:
```
✓ Database connection successful
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:5000
```

### Step 2: Run Tests

**Option 1: Simple Test (Recommended)**
```bash
cd backend
python test_system_simple.py
```

**Option 2: Comprehensive Test**
```bash
cd backend
python test_system.py
```

**Option 3: Manual Browser Test**

1. Open: http://localhost:5000/api/docs
2. Test endpoints interactively in Swagger UI

**Option 4: Using curl**

```bash
# Health check
curl http://localhost:5000/health

# Get parking lots
curl http://localhost:5000/api/v1/parking-lots/

# Register user
curl -X POST http://localhost:5000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123","full_name":"Test User"}'
```

## What to Test

### ✅ Basic Endpoints
- [ ] Health check: `/health`
- [ ] Root endpoint: `/`
- [ ] API docs: `/api/docs`

### ✅ Authentication
- [ ] Register user: `POST /api/v1/auth/register`
- [ ] Login: `POST /api/v1/auth/login`
- [ ] Get current user: `GET /api/v1/users/me` (requires auth)

### ✅ Parking Lots
- [ ] Get all parking lots: `GET /api/v1/parking-lots/`
- [ ] Get nearby: `GET /api/v1/parking-lots/nearby`
- [ ] Get by ID: `GET /api/v1/parking-lots/{id}`

### ✅ Bookings
- [ ] Get bookings: `GET /api/v1/bookings/` (requires auth)
- [ ] Create booking: `POST /api/v1/bookings/` (requires auth)

### ✅ Safety Ratings
- [ ] Get safety rating: `GET /api/v1/safety/{parking_lot_id}`
- [ ] Submit review: `POST /api/v1/safety/{parking_lot_id}/review` (requires auth)

### ✅ Analytics
- [ ] Dashboard: `GET /api/v1/analytics/dashboard` (requires auth)

## Expected Results

All endpoints should return:
- **200 OK** for successful GET requests
- **201 Created** for successful POST requests
- **401 Unauthorized** for protected endpoints without auth
- **404 Not Found** for non-existent resources

## Troubleshooting

### Server not running
```
Error: Cannot connect to server
```
**Solution:** Start the server first

### Port already in use
```
Error: Address already in use
```
**Solution:** Change port or stop the existing server

### Database error
```
Error: Database connection failed
```
**Solution:** Check database configuration in `.env` file

