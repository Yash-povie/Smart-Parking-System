# Smart Parking AI Service

AI-powered computer vision service for parking slot detection using YOLOv8.

## Features

- **Real-time Detection**: Detect parking slots from camera feeds
- **YOLOv8 Integration**: Uses YOLOv8 for vehicle detection
- **Camera Management**: Fetch and process images from camera URLs
- **Continuous Monitoring**: Monitor parking lots continuously
- **Safety Analysis**: AI-powered safety score analysis
- **Redis Caching**: Cache detection results for fast access

## Setup

1. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables:**
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. **Create models directory:**
```bash
mkdir models
```

5. **Run the service:**
```bash
python app.py
```

Or use uvicorn:
```bash
uvicorn app:app --reload --port 8001
```

## Model Training

To train a custom model for parking slot detection:

1. **Collect dataset**: Images of parking lots with labeled slots
2. **Label data**: Use tools like LabelImg or Roboflow
3. **Train model**: Use YOLOv8 training scripts
4. **Save model**: Place trained model in `models/parking_slot_detector.pt`

For now, the service uses pre-trained YOLOv8 model as a fallback.

## API Endpoints

- `GET /` - Service info
- `GET /health` - Health check
- `POST /detect-slots` - Detect slots from uploaded image
- `POST /detect-from-url` - Detect slots from camera URL
- `GET /parking-lot/{id}/slots` - Get current slot status
- `POST /parking-lot/{id}/start-monitoring` - Start continuous monitoring
- `POST /parking-lot/{id}/stop-monitoring` - Stop monitoring
- `GET /parking-lot/{id}/safety-score` - Get safety score

## Usage Example

### Detect slots from image:
```bash
curl -X POST "http://localhost:8001/detect-slots?parking_lot_id=1" \
  -F "image=@parking_lot.jpg"
```

### Detect from camera URL:
```bash
curl -X POST "http://localhost:8001/detect-from-url" \
  -H "Content-Type: application/json" \
  -d '{
    "parking_lot_id": 1,
    "camera_url": "http://camera.example.com/feed"
  }'
```

### Start monitoring:
```bash
curl -X POST "http://localhost:8001/parking-lot/1/start-monitoring" \
  -H "Content-Type: application/json" \
  -d '{
    "camera_url": "http://camera.example.com/feed"
  }'
```

## Integration with Backend

The AI service automatically updates the backend when slots are detected. Make sure:

1. Backend is running on `BACKEND_URL`
2. Redis is running (optional but recommended)
3. Camera URLs are accessible

## Development

The service uses:
- **FastAPI** for the API
- **YOLOv8** for object detection
- **OpenCV** for image processing
- **Redis** for caching
- **aiohttp** for async HTTP requests

## Notes

- The service uses pre-trained YOLOv8 model by default
- For production, train a custom model for better accuracy
- Camera URLs should be publicly accessible or use authentication
- Detection interval can be adjusted based on requirements


