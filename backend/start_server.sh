#!/bin/bash
echo "Starting Smart Parking System Backend..."
cd "$(dirname "$0")"
python -m uvicorn main:app --reload --port 5000


