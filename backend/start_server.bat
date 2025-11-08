@echo off
echo Starting Smart Parking System Backend...
cd /d "%~dp0"
python -m uvicorn main:app --reload --port 5000
pause


