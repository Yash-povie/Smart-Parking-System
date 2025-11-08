# Welcome! 👋 Smart Parking System Guide

## 🎯 What This Project Is

A complete **AI-powered smart parking system** for India with:
- Real-time parking slot detection using AI (YOLOv8)
- Smart booking system
- Suggestions based on availability and safety
- Beautiful UI with Indian pricing (₹60-₹200/hr)
- User dashboard and admin panel

## 🚀 Quick Start (3 Steps!)

### Step 1: Install Everything
```bash
npm run install:all
```
This installs all dependencies (frontend + backend)

### Step 2: Add Sample Data
```bash
cd backend
python seed_data.py
```
This creates:
- 3 user accounts (admin, owner, user)
- 6 parking lots across India
- Parking slots for each lot

### Step 3: Start the App
```bash
npm run dev
```
Then open: **http://localhost:3000**

## 🔑 Login Credentials

**User Account** (for booking):
- Email: `user@example.com`
- Password: `user123`

**Admin Account** (full access):
- Email: `admin@parking.com`
- Password: `admin123`

## 📖 How to Use

### 1. Browse Parking Lots
- Go to http://localhost:3000
- See all available parking lots
- Check the **Suggestions** section (top 3 recommended)

### 2. View Details
- Click **"View Details"** on any parking lot
- See parking slots (green = available, red = occupied)
- Check pricing in ₹ (Rupees)

### 3. Book a Spot
- Click **"Book Now"** button
- Login if not already logged in
- Fill in:
  - Vehicle number (e.g., MH12AB1234)
  - Vehicle type (Car, Bike, SUV, Truck)
  - Start time
  - End time
- See total price calculated automatically
- Click **"Confirm Booking"**

### 4. View Dashboard
- Login to your account
- Go to **Dashboard**
- See all your bookings

## 🛠️ Technologies Used

### Frontend
- **Next.js 16** - React framework
- **TypeScript** - Type-safe code
- **Tailwind CSS** - Styling
- **React Hooks** - useState, useEffect, useRouter, useParams

### Backend
- **Python 3.9+** - Programming language
- **FastAPI** - Web framework
- **SQLAlchemy** - Database ORM
- **SQLite** - Database (default)
- **JWT** - Authentication
- **bcrypt** - Password hashing

### AI/ML
- **YOLOv8** - Object detection
- **OpenCV** - Computer vision
- **PyTorch** - Deep learning

## 📁 Project Structure

```
parking-system/
├── frontend/          # Next.js frontend
│   ├── app/           # Pages (home, login, booking, etc.)
│   ├── components/    # React components (Suggestions)
│   └── lib/           # API client
│
├── backend/           # Python FastAPI backend
│   ├── app/           # Application code
│   │   ├── api/       # API endpoints
│   │   ├── ai/        # AI components
│   │   ├── models/    # Database models
│   │   └── schemas/   # Data validation
│   └── main.py        # Entry point
│
└── package.json       # Root config
```

## 🎨 Components Explained

### 1. **Suggestions Component** (`frontend/components/Suggestions.tsx`)
**What it does**: Shows top 3 recommended parking lots

**How it works**:
- Fetches all parking lots
- Filters by availability
- Sorts by: (availability rate × safety rating)
- Shows top 3 with price and ratings

**Methods used**:
- `useState` - Store suggestions
- `useEffect` - Load on page load
- `parkingLotApi.getAll()` - Fetch data
- Array filtering and sorting

### 2. **Home Page** (`frontend/app/page.tsx`)
**What it does**: Main landing page

**Features**:
- Hero section with title
- Suggestions section
- Grid of all parking lots
- Loading and error states

**Methods used**:
- `useState` - Manage parking lots, loading, error
- `useEffect` - Load data when page loads
- `parkingLotApi.getAll()` - Fetch parking lots
- Conditional rendering (if loading, if error, etc.)

### 3. **Booking Page** (`frontend/app/parking-lots/[id]/book/page.tsx`)
**What it does**: Book a parking spot

**Features**:
- Form for vehicle details
- Date/time pickers
- Real-time price calculation
- Booking confirmation

**Methods used**:
- `useParams` - Get parking lot ID from URL
- `useRouter` - Navigate after booking
- `useState` - Form state
- `bookingApi.create()` - Create booking
- Date calculations for pricing

### 4. **Parking Lot Detail** (`frontend/app/parking-lots/[id]/page.tsx`)
**What it does**: Show parking lot details

**Features**:
- Parking lot information
- Slot status grid (green/red/yellow)
- Book Now button

**Methods used**:
- `useParams` - Get ID from URL
- `Promise.all()` - Load lot and slots together
- `parkingLotApi.getById()` - Get lot details
- `parkingSlotApi.getByLotId()` - Get slots

### 5. **Login Page** (`frontend/app/login/page.tsx`)
**What it does**: User authentication

**Features**:
- Email/password login
- Redirect after login
- Error handling

**Methods used**:
- `useSearchParams` - Get redirect URL
- `useRouter` - Navigate after login
- `authApi.login()` - Authenticate
- `localStorage` - Store JWT token

## 🔧 Backend Methods

### Authentication
- **JWT Tokens**: Secure authentication
- **bcrypt**: Password hashing (one-way, cannot be reversed)
- **Token expiration**: 30 minutes

### API Endpoints
- `POST /api/v1/auth/register` - Register user
- `POST /api/v1/auth/login` - Login user
- `GET /api/v1/parking-lots/` - Get all lots
- `GET /api/v1/parking-lots/{id}` - Get lot details
- `POST /api/v1/bookings/` - Create booking
- `GET /api/v1/bookings/` - Get user bookings

### Database
- **SQLite** (default) - No setup needed
- **PostgreSQL** (optional) - For production

## 🎨 UI/UX Features

### Styling
- **Gradients**: Blue → Indigo → Purple backgrounds
- **Rounded corners**: Modern card design
- **Hover effects**: Transform and shadow
- **Color coding**: Green (available), Red (occupied), Yellow (reserved)
- **Responsive**: Works on mobile, tablet, desktop

### State Management
- **React Hooks**: useState, useEffect
- **Local Storage**: JWT token storage
- **URL Parameters**: Dynamic routing

## 📊 Sample Data

### Parking Lots Created:
1. **Connaught Place Parking** - Delhi (₹80/hr)
2. **Phoenix Mall Parking** - Mumbai (₹60/hr)
3. **Airport Express Parking** - Bangalore (₹150/hr)
4. **Marina Beach Parking** - Chennai (₹70/hr)
5. **IT Park Premium Parking** - Hyderabad (₹120/hr)
6. **Heritage City Parking** - Jaipur (₹65/hr)

## 🐛 Troubleshooting

### Backend won't start?
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload --port 5000
```

### Frontend won't start?
```bash
cd frontend
npm install
npm run dev
```

### Database errors?
```bash
cd backend
rm parking.db
python seed_data.py
```

## 📚 More Documentation

- **README.md** - Complete documentation
- **SETUP_GUIDE.md** - Detailed setup instructions
- **USER_CREDENTIALS.md** - All login credentials
- **API Docs**: http://localhost:5000/api/docs

## 🎯 Next Steps

1. **Explore the code** - Check out the components
2. **Try booking** - Book a parking spot
3. **Check API docs** - See all available endpoints
4. **Customize** - Add your own features!

## 💡 Tips

- **Check browser console** for errors
- **Check backend terminal** for API logs
- **Use API docs** to test endpoints
- **Check README.md** for detailed info

---

**Happy Coding! 🚀**

