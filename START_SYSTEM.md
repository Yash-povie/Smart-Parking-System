# 🚀 How to Start the Whole System

## Quick Start (All Services at Once)

### Option 1: One Command (Recommended)

```bash
npm run dev
```

This starts:
- ✅ Backend API with AI Service (port 5000)
- ✅ Frontend (port 3000)

**Note:** Make sure you've installed dependencies first (see below).

---

## Step-by-Step Setup

### Step 1: Install Dependencies

**First time setup only:**

```bash
# Install all dependencies (backend, frontend, AI service)
npm run install:all
```

Or install manually:

```bash
# Root dependencies
npm install

# Backend dependencies
cd backend
pip install -r requirements.txt
cd ..

# AI Service dependencies
cd ai-service
pip install -r requirements.txt
cd ..

# Frontend dependencies
cd frontend
npm install
cd ..
```

### Step 2: Start Services

#### Option A: Start All at Once (Easiest)

```bash
npm run dev
```

#### Option B: Start Each Service Separately

**Terminal 1 - Backend (includes AI):**
```bash
cd backend
python -m uvicorn main:app --reload --port 5000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

---

## What Gets Started

### 1. Backend API (includes AI Service)
- **URL**: http://localhost:5000
- **API Docs**: http://localhost:5000/api/docs
- **AI Endpoints**: http://localhost:5000/api/v1/ai
- **Health Check**: http://localhost:5000/health
- **Database**: SQLite (auto-created at `backend/parking.db`)
- **Model**: Pre-trained YOLOv8 (works immediately)

### 2. Frontend
- **URL**: http://localhost:3000
- **Web App**: Opens in browser automatically

---

## Verify Everything is Running

### Check Backend
```bash
curl http://localhost:5000/health
```
Should return: `{"status":"healthy","service":"smart-parking-api"}`

### Check AI Endpoints
```bash
curl http://localhost:5000/api/v1/ai/parking-lot/1/slots
```
Should return slot status or empty status

### Check Frontend
Open browser: http://localhost:3000

---

## Windows Quick Start

### Using Batch Files

**Start Backend:**
```bash
cd backend
start_server.bat
```

**Start AI Service:**
```bash
cd ai-service
python app.py
```

**Start Frontend:**
```bash
cd frontend
npm run dev
```

---

## Troubleshooting

### Port Already in Use

If you get "port already in use" error:

**Backend (port 5000):**
```bash
# Find and kill process
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

**Frontend (port 3000):**
```bash
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

### Dependencies Not Installed

```bash
# Reinstall all dependencies
npm run install:all
```

### Database Issues

The system uses SQLite by default (no setup needed). Database file is created automatically at:
- `backend/parking.db`

---

## First Time Setup Checklist

- [ ] Install Node.js 18+ (for frontend)
- [ ] Install Python 3.9+ (for backend and AI service)
- [ ] Run `npm run install:all` to install all dependencies
- [ ] Start system with `npm run dev`
- [ ] Verify backend: http://localhost:5000/health
- [ ] Verify AI endpoints: http://localhost:5000/api/v1/ai/parking-lot/1/slots
- [ ] Open frontend: http://localhost:3000

---

## Optional: Add Sample Data

After starting the backend, you can add sample parking lots:

```bash
cd backend
python seed_data.py
```

This creates:
- Sample parking lots
- Sample parking slots
- Test bookings
- Safety reviews

---

## System URLs Summary

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend** | http://localhost:3000 | Web application |
| **Backend API** | http://localhost:5000 | REST API (includes AI) |
| **Backend Docs** | http://localhost:5000/api/docs | Swagger UI |
| **AI Endpoints** | http://localhost:5000/api/v1/ai | AI detection endpoints |

---

## Stop the System

Press `Ctrl+C` in each terminal window, or:

**Windows:**
```bash
# Kill all Node.js processes
taskkill /F /IM node.exe

# Kill all Python processes (be careful!)
taskkill /F /IM python.exe
```

---

**That's it! Your system is ready to use! 🎉**

