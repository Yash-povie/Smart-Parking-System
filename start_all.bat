@echo off
echo ========================================
echo Starting Smart Parking System
echo ========================================
echo.

echo [1/2] Starting Backend API (includes AI service)...
start "Backend API" cmd /k "cd backend && python -m uvicorn main:app --reload --port 5000"

timeout /t 3 /nobreak >nul

echo [2/2] Starting Frontend...
start "Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ========================================
echo All services starting...
echo ========================================
echo.
echo Backend API:    http://localhost:5000
echo Backend Docs:   http://localhost:5000/api/docs
echo AI Endpoints:   http://localhost:5000/api/v1/ai
echo Frontend:       http://localhost:3000
echo.
echo Press any key to exit this window (services will keep running)
pause >nul

