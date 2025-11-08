# Smart Parking System 🚗

An AI-powered smart parking solution for India with real-time detection, booking, and safety ratings.

## 🎯 Features

- **AI-Powered Detection**: Real-time parking slot detection using YOLOv8
- **Smart Booking**: Find, book, and manage parking spots
- **Suggestions**: AI-recommended parking lots based on availability and safety
- **Safety Ratings**: User feedback and AI analytics for parking lot safety
- **Indian Pricing**: All prices in ₹ (Rupees) - ₹60 to ₹200 per hour
- **Real-Time Updates**: Live availability tracking
- **User Dashboard**: Personal booking history and preferences

## 🛠️ Tech Stack

### Frontend
- **Next.js 16** - React framework with App Router
- **TypeScript** - Type-safe JavaScript
- **Tailwind CSS** - Utility-first CSS framework
- **React Hooks** - useState, useEffect for state management
- **Next.js Navigation** - useRouter, useParams, useSearchParams

### Backend
- **Python 3.9+** - Programming language
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - ORM for database operations
- **SQLite** - Database (default, can use PostgreSQL)
- **JWT** - Authentication tokens
- **bcrypt** - Password hashing
- **Pydantic** - Data validation

### AI/ML
- **YOLOv8** - Object detection model
- **OpenCV** - Computer vision
- **PyTorch** - Deep learning framework
- **Ultralytics** - YOLOv8 implementation

## 📁 Project Structure

```
parking-system/
├── frontend/              # Next.js frontend application
│   ├── app/              # Next.js app directory
│   │   ├── page.tsx      # Home page
│   │   ├── login/        # Login page
│   │   ├── register/     # Registration page
│   │   ├── dashboard/    # User dashboard
│   │   └── parking-lots/ # Parking lot pages
│   ├── components/       # React components
│   │   └── Suggestions.tsx # Suggestions component
│   ├── lib/              # Utility functions
│   │   └── api.ts        # API client
│   └── package.json      # Frontend dependencies
│
├── backend/              # Python FastAPI backend
│   ├── app/              # Application code
│   │   ├── api/          # API endpoints
│   │   ├── core/         # Core configuration
│   │   ├── models/       # Database models
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── ai/           # AI components
│   │   └── websocket/    # WebSocket manager
│   ├── main.py           # Application entry point
│   ├── requirements.txt  # Python dependencies
│   └── seed_data.py     # Sample data generator
│
└── package.json          # Root package.json
```

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ (for frontend)
- Python 3.9+ (for backend)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd parking-system
   ```

2. **Install all dependencies**
   ```bash
   npm run install:all
   ```

3. **Add sample data**
   ```bash
   cd backend
   python seed_data.py
   ```

4. **Start the application**
   ```bash
   npm run dev
   ```

5. **Open in browser**
   - Frontend: http://localhost:3000
   - Backend API Docs: http://localhost:5000/api/docs

## 👤 User Credentials

### Admin Account
- **Email**: `admin@parking.com`
- **Password**: `admin123`
- **Role**: Admin (full access)

### Owner Account
- **Email**: `owner@parking.com`
- **Password**: `owner123`
- **Role**: Parking Owner

### User Account
- **Email**: `user@example.com`
- **Password**: `user123`
- **Role**: Regular User

### Create New Account
You can also register a new account at: http://localhost:3000/register

## 📖 How to Use

### 1. Browse Parking Lots
- Visit http://localhost:3000
- See all available parking lots
- View suggestions (top 3 recommended)
- Check availability and prices

### 2. View Parking Lot Details
- Click "View Details" on any parking lot
- See parking slots status
- View safety ratings
- Check pricing

### 3. Book a Parking Spot
- Click "Book Now" on parking lot page
- Login if not already logged in
- Fill in booking details:
  - Vehicle number
  - Vehicle type (Car, Bike, SUV, Truck)
  - Start time
  - End time
- Confirm booking
- View total price (calculated automatically)

### 4. View Dashboard
- Login to your account
- Go to Dashboard
- See all your bookings
- View booking history

### 5. Register New Account
- Click "Register" in navigation
- Fill in details:
  - Full Name
  - Email
  - Phone Number
  - Password
- Create account
- Login to start booking

## 🔧 Components Used

### Frontend Components

#### 1. **Suggestions Component** (`components/Suggestions.tsx`)
- **Purpose**: Shows top 3 recommended parking lots
- **Features**:
  - Filters by availability
  - Sorts by availability rate × safety rating
  - Displays price, availability, and ratings
  - Clickable cards linking to parking lot details
- **Methods Used**:
  - `useState` - State management
  - `useEffect` - Load data on mount
  - `parkingLotApi.getAll()` - Fetch parking lots
  - Array filtering and sorting

#### 2. **Home Page** (`app/page.tsx`)
- **Purpose**: Main landing page with parking lot listings
- **Features**:
  - Hero section
  - Suggestions display
  - Grid of parking lots
  - Loading and error states
- **Methods Used**:
  - `useState` - Manage parking lots, loading, error
  - `useEffect` - Load data on component mount
  - `parkingLotApi.getAll()` - Fetch all parking lots
  - Conditional rendering

#### 3. **Booking Page** (`app/parking-lots/[id]/book/page.tsx`)
- **Purpose**: Book a parking spot
- **Features**:
  - Vehicle information form
  - Date/time pickers
  - Real-time price calculation
  - Booking confirmation
- **Methods Used**:
  - `useParams` - Get parking lot ID from URL
  - `useRouter` - Navigation
  - `useState` - Form state management
  - `bookingApi.create()` - Create booking
  - Date calculations for pricing

#### 4. **Parking Lot Detail Page** (`app/parking-lots/[id]/page.tsx`)
- **Purpose**: Show parking lot details and slots
- **Features**:
  - Parking lot information
  - Slot status grid
  - Book Now button
- **Methods Used**:
  - `useParams` - Get ID from URL
  - `Promise.all()` - Parallel API calls
  - `parkingLotApi.getById()` - Get lot details
  - `parkingSlotApi.getByLotId()` - Get slots

#### 5. **Login Page** (`app/login/page.tsx`)
- **Purpose**: User authentication
- **Features**:
  - Email/password login
  - Redirect after login
  - Error handling
- **Methods Used**:
  - `useSearchParams` - Get redirect URL
  - `useRouter` - Navigation
  - `authApi.login()` - Authenticate user
  - `localStorage` - Store JWT token

### Backend Components

#### 1. **AI Detector** (`backend/app/ai/detector.py`)
- **Purpose**: Detect vehicles in parking lots
- **Methods**:
  - `load_model()` - Load YOLOv8 model
  - `detect_slots()` - Detect parking slots
  - `analyze_safety()` - Calculate safety score
- **Technologies**: YOLOv8, OpenCV, PyTorch

#### 2. **API Endpoints** (`backend/app/api/v1/endpoints/`)
- **auth.py** - Authentication (register, login)
- **parking_lots.py** - Parking lot CRUD
- **parking_slots.py** - Slot management
- **bookings.py** - Booking operations
- **ai.py** - AI detection endpoints
- **analytics.py** - Dashboard statistics
- **safety.py** - Safety ratings

#### 3. **Database Models** (`backend/app/models/`)
- **User** - User accounts
- **ParkingLot** - Parking lot information
- **ParkingSlot** - Individual slots
- **Booking** - Booking records
- **SafetyReview** - User reviews

## 🔐 Authentication Methods

### JWT (JSON Web Tokens)
- **How it works**:
  1. User logs in with email/password
  2. Backend validates credentials
  3. Backend generates JWT token
  4. Token stored in localStorage (frontend)
  5. Token sent in Authorization header for protected routes
- **Token expiration**: 30 minutes (configurable)

### Password Hashing
- **Method**: bcrypt
- **Rounds**: 12
- **Security**: One-way hashing, cannot be reversed

## 📡 API Methods

### REST API
- **Base URL**: `http://localhost:5000/api/v1`
- **Authentication**: Bearer token in Authorization header
- **Format**: JSON

### Key Endpoints
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login user
- `GET /parking-lots/` - Get all parking lots
- `GET /parking-lots/{id}` - Get parking lot details
- `POST /bookings/` - Create booking
- `GET /bookings/` - Get user bookings
- `POST /ai/detect-slots` - AI detection

## 🎨 UI/UX Methods

### Styling
- **Tailwind CSS** - Utility-first CSS
- **Gradients** - Blue → Indigo → Purple
- **Responsive Design** - Mobile-first approach
- **Hover Effects** - Transform and shadow
- **Loading States** - Spinners and skeletons
- **Error Handling** - User-friendly messages

### State Management
- **React Hooks** - useState, useEffect
- **Local Storage** - JWT token storage
- **URL Parameters** - Dynamic routing

## 🗄️ Database

### Default: SQLite
- **File**: `backend/parking.db`
- **No setup required** - Auto-created

### Optional: PostgreSQL
- Update `DATABASE_URL` in `.env`
- Format: `postgresql://user:password@localhost:5432/dbname`

## 🧪 Testing

### Run Backend Tests
```bash
cd backend
python test_complete_system.py
```

### Expected Output
```
Passed: 15
Failed: 0
SUCCESS: All tests passed!
```

## 📝 Sample Data

### Parking Lots Created
1. **Connaught Place Parking** - Delhi (₹80/hr)
2. **Phoenix Mall Parking** - Mumbai (₹60/hr)
3. **Airport Express Parking** - Bangalore (₹150/hr)
4. **Marina Beach Parking** - Chennai (₹70/hr)
5. **IT Park Premium Parking** - Hyderabad (₹120/hr)
6. **Heritage City Parking** - Jaipur (₹65/hr)

## 🚨 Troubleshooting

### Backend won't start
- Check Python version: `python --version` (should be 3.9+)
- Install dependencies: `pip install -r requirements.txt`
- Check port 5000 is available

### Frontend won't start
- Check Node.js version: `node --version` (should be 18+)
- Install dependencies: `npm install`
- Check port 3000 is available

### AI model not loading
- Install AI dependencies: `pip install ultralytics torch`
- Model downloads automatically on first use

### Database errors
- Delete `backend/parking.db` and run `seed_data.py` again
- Check `.env` file for database URL

## 📚 Additional Documentation

- **Backend Setup**: `backend/README.md`
- **API Documentation**: http://localhost:5000/api/docs
- **Frontend Setup**: `frontend/README.md`
- **Testing Guide**: `backend/TESTING.md`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

Proprietary - All rights reserved

## 👥 Support

For issues or questions:
1. Check the troubleshooting section
2. Review API documentation
3. Check backend logs for errors

---

**Built with ❤️ for India 🇮🇳**
