# Setup Guide - Smart Parking System

## 🚀 Quick Setup (5 Minutes)

### Step 1: Install Dependencies

```bash
# Install all dependencies at once
npm run install:all
```

This installs:
- Frontend dependencies (Node.js packages)
- Backend dependencies (Python packages)

### Step 2: Create Sample Data

```bash
cd backend
python seed_data.py
```

This creates:
- 3 user accounts (admin, owner, user)
- 6 parking lots across India
- Parking slots for each lot

### Step 3: Start the Application

```bash
# From root directory
npm run dev
```

This starts:
- Backend API on http://localhost:5000
- Frontend on http://localhost:3000

### Step 4: Login

Visit http://localhost:3000 and login with:
- **Email**: `user@example.com`
- **Password**: `user123`

## 📋 Detailed Setup

### Prerequisites Check

```bash
# Check Node.js version (should be 18+)
node --version

# Check Python version (should be 3.9+)
python --version

# Check npm
npm --version
```

### Manual Installation

If `npm run install:all` doesn't work:

#### Frontend
```bash
cd frontend
npm install
```

#### Backend
```bash
cd backend
pip install -r requirements.txt
```

### Environment Variables

Create `backend/.env` (optional):
```env
DATABASE_URL=sqlite:///./parking.db
SECRET_KEY=your-secret-key-change-in-production
PORT=5000
```

Create `frontend/.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:5000
```

## ✅ Verification

### Check Backend
```bash
curl http://localhost:5000/health
```
Should return: `{"status":"healthy","service":"smart-parking-api"}`

### Check Frontend
Open: http://localhost:3000

### Check API Docs
Open: http://localhost:5000/api/docs

## 🎯 First Steps After Setup

1. **Browse Parking Lots**
   - Go to http://localhost:3000
   - See all available parking lots
   - Check suggestions section

2. **View Details**
   - Click "View Details" on any parking lot
   - See parking slots
   - Check pricing

3. **Book a Spot**
   - Click "Book Now"
   - Login if needed
   - Fill booking form
   - Confirm booking

4. **View Dashboard**
   - Login to account
   - Go to Dashboard
   - See your bookings

## 🔑 All User Credentials

### Admin
- Email: `admin@parking.com`
- Password: `admin123`
- Access: Full system access

### Owner
- Email: `owner@parking.com`
- Password: `owner123`
- Access: Parking lot management

### User
- Email: `user@example.com`
- Password: `user123`
- Access: Book parking spots

## 🐛 Common Issues

### Port Already in Use
```bash
# Windows - Find process using port 5000
netstat -ano | findstr :5000

# Kill process (replace PID)
taskkill /PID <PID> /F
```

### Dependencies Not Installing
```bash
# Clear npm cache
npm cache clean --force

# Clear pip cache
pip cache purge

# Try again
npm run install:all
```

### Database Errors
```bash
# Delete database and recreate
cd backend
rm parking.db
python seed_data.py
```

## 📞 Need Help?

1. Check `README.md` for detailed documentation
2. Review API docs at http://localhost:5000/api/docs
3. Check backend logs for errors
4. Verify all prerequisites are installed

---

**Ready to go! 🎉**

