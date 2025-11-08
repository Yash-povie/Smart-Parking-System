# Quick Start Guide

## ✅ Backend is Running!

Your backend is now live at: **http://localhost:5000**

## 🚀 Quick Test

### 1. Open API Documentation
Visit: **http://localhost:5000/api/docs**

This is the Swagger UI where you can test all endpoints interactively!

### 2. Test Health Check
Visit: **http://localhost:5000/health**

Should return: `{"status": "healthy", "service": "smart-parking-api"}`

### 3. Register a User

In Swagger UI:
1. Go to `/api/v1/auth/register`
2. Click "Try it out"
3. Use this example:
```json
{
  "email": "test@example.com",
  "password": "test123",
  "full_name": "Test User",
  "phone_number": "+1234567890"
}
```
4. Click "Execute"

### 4. Login

1. Go to `/api/v1/auth/login`
2. Click "Try it out"
3. Use:
   - username: `test@example.com`
   - password: `test123`
4. Click "Execute"
5. Copy the `access_token` from the response

### 5. Access Protected Endpoints

1. Click the "Authorize" button at the top of Swagger UI
2. Enter: `Bearer YOUR_ACCESS_TOKEN_HERE`
3. Now you can test protected endpoints!

## 📋 Available Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login and get token
- `GET /api/v1/auth/me` - Get current user (requires auth)

### Parking Lots
- `GET /api/v1/parking-lots/` - List all parking lots
- `GET /api/v1/parking-lots/nearby` - Find nearby parking
- `GET /api/v1/parking-lots/{id}` - Get parking lot details
- `POST /api/v1/parking-lots/` - Create parking lot (admin/owner)

### Bookings
- `POST /api/v1/bookings/` - Create booking
- `GET /api/v1/bookings/` - Get your bookings
- `POST /api/v1/bookings/{id}/confirm` - Confirm booking
- `POST /api/v1/bookings/{id}/cancel` - Cancel booking

### Payments
- `POST /api/v1/payments/create-payment-intent` - Create payment

### Safety Ratings
- `GET /api/v1/safety/{parking_lot_id}` - Get safety rating
- `POST /api/v1/safety/{parking_lot_id}/review` - Submit review

### Analytics
- `GET /api/v1/analytics/dashboard` - Get dashboard stats

## 🎯 Next Steps

1. **Test the API** - Use Swagger UI to test all endpoints
2. **Create Sample Data** - Add parking lots and slots
3. **Start AI Service** - Run the computer vision service
4. **Build Frontend** - Create the Next.js frontend
5. **Train Model** - Train YOLOv8 with your parking data

## 💡 Tips

- All endpoints are documented in Swagger UI
- Use the "Authorize" button to test protected endpoints
- Check the response schemas in Swagger for data formats
- Database is SQLite (parking.db) - no setup needed!

Happy coding! 🚀

