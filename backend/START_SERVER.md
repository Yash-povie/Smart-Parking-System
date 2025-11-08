# Starting the Backend Server

## Quick Start

### Option 1: Using the Script (Easiest)

**Windows:**
```bash
start_server.bat
```

**Mac/Linux:**
```bash
chmod +x start_server.sh
./start_server.sh
```

### Option 2: Manual Start

```bash
cd backend
python -m uvicorn main:app --reload --port 5000
```

### Option 3: Using Config (Recommended)

The server will automatically use port 5000 from config:

```bash
cd backend
python -m uvicorn main:app --reload
```

## Port Configuration

The default port is **5000**. You can change it by:

1. **Setting environment variable:**
   ```bash
   set PORT=8080  # Windows
   export PORT=8080  # Mac/Linux
   python -m uvicorn main:app --reload
   ```

2. **Editing .env file:**
   ```
   PORT=8080
   ```

3. **Command line:**
   ```bash
   python -m uvicorn main:app --reload --port 8080
   ```

## Verify Server is Running

Once started, you should see:
```
✓ Database connection successful
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:5000
```

Then visit:
- **API Docs**: http://localhost:5000/api/docs
- **Health Check**: http://localhost:5000/health


