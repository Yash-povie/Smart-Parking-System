#!/bin/bash

echo "========================================"
echo "Starting Smart Parking System"
echo "========================================"
echo ""

echo "[1/2] Starting Backend API (includes AI service)..."
cd backend
python -m uvicorn main:app --reload --port 5000 &
BACKEND_PID=$!
cd ..

sleep 3

echo "[2/2] Starting Frontend..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "========================================"
echo "All services starting..."
echo "========================================"
echo ""
echo "Backend API:    http://localhost:5000"
echo "Backend Docs:   http://localhost:5000/api/docs"
echo "AI Endpoints:   http://localhost:5000/api/v1/ai"
echo "Frontend:       http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Wait for user interrupt
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT TERM
wait

