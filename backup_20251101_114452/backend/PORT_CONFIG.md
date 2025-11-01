# Port Configuration Guide

## Default Port

The backend is configured to run on **port 5000** by default.

## Why Port 5000 Might Be In Use

On macOS, port 5000 is commonly used by:
1. **AirPlay Receiver** - Apple's service for receiving AirPlay connections
2. **Previous Flask instance** - If you started the server before and didn't stop it
3. **Other applications** - Some development tools use port 5000

## Solutions

### Solution 1: Use a Different Port (Recommended)

The easiest solution is to use port **5001** or **8000**.

#### Option A: Set Environment Variable
```bash
export PORT=5001
python app.py
```

#### Option B: Create .env file
Create a `.env` file in the `backend/` directory:
```env
PORT=5001
FLASK_ENV=development
CORS_ORIGIN=http://localhost:3000
```

Then run:
```bash
python app.py
```

#### Option C: Update Frontend API URL
If you change the port, update `frontend/.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:5001
```

### Solution 2: Kill Process Using Port 5000

Find what's using the port:
```bash
lsof -ti:5000
```

Kill the process:
```bash
kill -9 $(lsof -ti:5000)
```

Then start your backend:
```bash
python app.py
```

### Solution 3: Disable AirPlay Receiver (macOS)

If AirPlay Receiver is using port 5000:

1. Open **System Preferences** → **General** → **AirDrop & Handoff**
2. Turn off **AirPlay Receiver**
3. Restart your backend

## Recommended Ports

- **Port 5001** - Common alternative to 5000
- **Port 8000** - Also commonly used for web servers
- **Port 8080** - Alternative web server port

## Quick Fix (Right Now)

**Easiest**: Use port 5001

```bash
cd backend
export PORT=5001
python app.py
```

And update your frontend `.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:5001
```

Then restart your frontend.

