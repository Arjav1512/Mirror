# Mirror MVP Setup Guide

## Quick Start

### Prerequisites
- Python 3.10+ 
- Node.js 18+ and npm
- pip (Python package manager)

### One-Command Setup

**Mac/Linux:**
```bash
./start.sh
```

**Windows:**
```bash
start.bat
```

This script will:
1. ✅ Create Python virtual environment
2. ✅ Install Python dependencies
3. ✅ Install Node.js dependencies
4. ✅ Build React frontend
5. ✅ Start all servers

## Manual Setup

### Step 1: Install Python Dependencies
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2: Install Node.js Dependencies
```bash
cd frontend
npm install
npm run build
cd ..
```

### Step 3: Start Servers

**Terminal 1 - API Server:**
```bash
cd backend
python api_server.py
```
Runs on: http://localhost:5001

**Terminal 2 - Landing Page:**
```bash
cd backend
python serve_react.py 5000
```
Runs on: http://localhost:5000

**Terminal 3 - Streamlit Journal:**
```bash
cd backend
streamlit run app.py
```
Runs on: http://localhost:8501

## Development Mode

For frontend development with hot reload:

```bash
cd frontend
npm run dev
```

This runs the React dev server on http://localhost:3000

## Troubleshooting

### Port Already in Use
```bash
# Mac/Linux
lsof -ti:5000 | xargs kill -9
lsof -ti:5001 | xargs kill -9
lsof -ti:8501 | xargs kill -9

# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### React Build Errors
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run build
```

### Python Import Errors
```bash
source venv/bin/activate  # Activate venv first
pip install -r requirements.txt
```

## Access Points

- **Landing Page**: http://localhost:5000
- **API Server**: http://localhost:5001
- **Journal App**: http://localhost:8501
- **React Dev Server**: http://localhost:3000 (dev mode only)

