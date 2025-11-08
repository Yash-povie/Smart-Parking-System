# AI Service Merged into Backend

## ✅ What Changed

The AI service has been **merged into the backend** for simplicity. Everything now runs in a single service.

## 📍 AI Endpoints

All AI endpoints are now available under `/api/v1/ai`:

- `POST /api/v1/ai/detect-slots` - Detect slots from uploaded image
- `POST /api/v1/ai/detect-from-url` - Detect slots from camera URL
- `GET /api/v1/ai/parking-lot/{id}/slots` - Get slot status
- `POST /api/v1/ai/parking-lot/{id}/start-monitoring` - Start monitoring
- `POST /api/v1/ai/parking-lot/{id}/stop-monitoring` - Stop monitoring
- `GET /api/v1/ai/parking-lot/{id}/safety-score` - Get safety score

## 🚀 Benefits

- ✅ **Simpler setup** - Only one Python service to run
- ✅ **Single port** - Everything on port 5000
- ✅ **Easier deployment** - One service to deploy
- ✅ **Shared resources** - Database and Redis connections shared

## 📦 Dependencies

All AI dependencies are now in `backend/requirements.txt`:
- `ultralytics>=8.0.0` - YOLOv8 model
- `aiohttp>=3.9.0` - Async HTTP client
- `torch>=2.0.0` - PyTorch (for YOLOv8)

## 🔧 Configuration

AI components are initialized automatically when the backend starts. The model loads on startup (non-blocking).

## 📝 Old AI Service

The `ai-service/` directory is kept for reference but is no longer needed. You can delete it if you want.

