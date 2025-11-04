# Quick Start Guide

## How to Run Mirror

### Option 1: Use the Startup Script (Recommended)

**Linux/Mac:**
```bash
./start.sh
```

**Windows:**
```bash
start.bat
```

This will:
1. Start the Flask API server on `http://localhost:5000` (serves the landing page)
2. Start the Streamlit app on `http://localhost:8501` (journal interface)

### Option 2: Manual Start

**Terminal 1 - Start API Server (Landing Page):**
```bash
cd backend
python api_server.py
```
This serves the landing page at: `http://localhost:5000`

**Terminal 2 - Start Streamlit App (Journal):**
```bash
cd backend
streamlit run app.py
```
This serves the journal at: `http://localhost:8501`

## User Flow

1. **Landing Page** → Visit `http://localhost:5000`
   - Fill out the signup form
   - Submit your information
   - You'll be redirected to the journal app

2. **Journal App** → `http://localhost:8501`
   - Sign in with your email
   - Start journaling!

## Troubleshooting

### Landing page not loading?
- Make sure the Flask API server is running on port 5000
- Check `api.log` for errors

### Form submission fails?
- Verify the API server is running: `http://localhost:5000/api/user/test@example.com`
- Check browser console for errors
- Ensure both servers are running

### Can't see styles/CSS?
- Make sure you're accessing via `http://localhost:5000` (not 8501)
- Flask server should serve the CSS/JS files automatically

## Ports
- **5000**: Landing page (Flask API server)
- **8501**: Journal app (Streamlit)

