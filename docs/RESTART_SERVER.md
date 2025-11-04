# Fixing 403 Error - Server Restart Guide

The 403 error was likely caused by an old server process. Here's how to fix it:

## Step 1: Kill any existing processes

**Mac/Linux:**
```bash
# Kill process on port 5000
lsof -ti:5000 | xargs kill -9
```

**Or manually:**
```bash
# Find the process
lsof -i:5000
# Kill it (replace PID with the actual process ID)
kill -9 <PID>
```

## Step 2: Restart the server

```bash
cd backend
python api_server.py
```

You should see:
```
============================================================
🚀 Starting Mirror Flask Server
============================================================
📍 Frontend directory: /path/to/frontend
🌐 Server will start on: http://localhost:5000
📝 Landing page: http://localhost:5000/
============================================================
```

## Step 3: Clear browser cache

1. Open browser developer tools (F12)
2. Right-click the refresh button
3. Select "Empty Cache and Hard Reload"

Or:
- **Chrome/Edge:** Ctrl+Shift+Delete (Cmd+Shift+Delete on Mac) → Clear cache
- **Firefox:** Ctrl+Shift+Delete → Clear cache

## Step 4: Visit the landing page

Go to: **http://localhost:5000**

If you still see 403:
1. Check the terminal output for any error messages
2. Make sure you're visiting `http://localhost:5000` (not 8501)
3. Try in an incognito/private window

## Alternative: Use the test server

If the main server still has issues, try the simple test server:

```bash
python test_server.py
```

Then visit: **http://localhost:5001**

