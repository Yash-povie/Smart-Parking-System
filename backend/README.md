# Smart Parking System - Backend API

Python FastAPI backend for the Smart Parking System.

## Features

- FastAPI with async/await support
- JWT authentication
- PostgreSQL database with SQLAlchemy ORM
- WebSocket support for real-time updates
- Redis integration for caching
- Payment processing with Stripe
- RESTful API design

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Set up database:
```bash
# Make sure PostgreSQL is running
# Create database: parking_db
```

5. Run database migrations:
```bash
alembic upgrade head
```

6. Run the server:
```bash
python -m uvicorn main:app --reload --port 5000
```

Or use the npm script:
```bash
npm run dev:backend
```

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:5000/api/docs
- ReDoc: http://localhost:5000/api/redoc

## Project Structure

```
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/     # API endpoint handlers
│   │       └── router.py      # API router
│   ├── core/
│   │   ├── config.py          # Configuration settings
│   │   ├── database.py        # Database setup
│   │   └── security.py        # Authentication & security
│   ├── models/                # SQLAlchemy models
│   ├── schemas/               # Pydantic schemas
│   └── websocket/             # WebSocket handlers
├── main.py                    # Application entry point
└── requirements.txt           # Python dependencies
```

## Environment Variables

See `.env.example` for all required environment variables.

## Development

The server runs in development mode with auto-reload enabled. Any changes to the code will automatically restart the server.

