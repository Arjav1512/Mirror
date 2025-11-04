#!/bin/bash
# Startup script for Mirror application

echo "Starting Mirror Application..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install Python dependencies if needed
if [ ! -f "venv/.installed" ]; then
    echo "Installing Python dependencies..."
    pip install -r requirements.txt
    touch venv/.installed
fi

# Install Node.js dependencies for frontend if needed
if [ ! -d "frontend/node_modules" ]; then
    echo "Installing frontend dependencies..."
    cd frontend
    npm install
    cd ..
fi

# Download NLTK data
echo "Checking NLTK data..."
python3 -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('brown', quiet=True); nltk.download('vader_lexicon', quiet=True)" 2>/dev/null || echo "NLTK data check skipped"

# Start Flask API server in background (for form submissions)
echo "Starting API server on port 5001..."
cd backend
python api_server.py > ../api.log 2>&1 &
API_PID=$!
cd ..

# Check if React is built, if not build it
if [ ! -d "frontend/dist" ]; then
    echo "Building React frontend..."
    cd frontend
    if [ ! -d "node_modules" ]; then
        echo "Installing npm dependencies..."
        npm install
    fi
    npm run build
    cd ..
fi

# Start landing page server in background (serving React build)
echo "Starting landing page server on port 5000..."
cd backend
python serve_react.py 5000 > ../landing.log 2>&1 &
LANDING_PID=$!
cd ..

# Wait a moment for API to start
sleep 2

echo ""
echo "═══════════════════════════════════════════════════════"
echo "🚀 Mirror Application Starting..."
echo "═══════════════════════════════════════════════════════"
echo ""
echo "📍 Landing Page:  http://localhost:5000"
echo "📍 Journal App:   http://localhost:8501"
echo "📍 API Server:    http://localhost:5001"
echo ""
echo "Start with the landing page to sign up!"
echo "═══════════════════════════════════════════════════════"
echo ""

# Start Streamlit app
echo "Starting Streamlit app (Journal) on port 8501..."
cd backend
streamlit run app.py --server.port 8501

# Cleanup on exit
kill $API_PID $LANDING_PID 2>/dev/null
echo ""
echo "Mirror application stopped."

