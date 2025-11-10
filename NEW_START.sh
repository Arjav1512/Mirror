#!/bin/bash

# Mirror - Unified Start Script (Refactored)
# Starts all services for the Mirror journaling application

echo ""
echo "=========================================="
echo "🧠 Mirror - AI-Powered Journal"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 is not installed${NC}"
    echo "Please install Python 3.8+ first"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js is not installed${NC}"
    echo "Please install Node.js 16+ first"
    exit 1
fi

echo -e "${GREEN}✓${NC} Python3 detected: $(python3 --version)"
echo -e "${GREEN}✓${NC} Node.js detected: $(node --version)"
echo ""

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt --quiet
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓${NC} Python dependencies installed"
else
    echo -e "${RED}❌ Failed to install Python dependencies${NC}"
    exit 1
fi

# Download NLTK data
echo "📚 Downloading NLTK data..."
python3 -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('brown', quiet=True); nltk.download('vader_lexicon', quiet=True)" 2>/dev/null
echo -e "${GREEN}✓${NC} NLTK data downloaded"

# Install Node dependencies and build
echo "🏗️  Building frontend..."
cd frontend
npm install --silent 2>/dev/null
npm run build --silent 2>/dev/null
cd ..

if [ -d "frontend/dist" ]; then
    echo -e "${GREEN}✓${NC} Frontend built successfully"
else
    echo -e "${RED}❌ Frontend build failed${NC}"
    exit 1
fi

echo ""
echo "=========================================="
echo "🚀 Starting Services"
echo "=========================================="
echo ""

# Kill any existing processes on the ports
echo "🔍 Checking for processes on ports..."
lsof -ti:5001 | xargs kill -9 2>/dev/null
lsof -ti:8501 | xargs kill -9 2>/dev/null
sleep 1

# Start API Server in background
echo "🌐 Starting API Server (port 5001)..."
cd backend
python3 api_server.py > ../api.log 2>&1 &
API_PID=$!
cd ..
sleep 2

# Check if API server started
if ps -p $API_PID > /dev/null; then
    echo -e "${GREEN}✓${NC} API Server started (PID: $API_PID)"
else
    echo -e "${RED}❌ API Server failed to start${NC}"
    cat api.log
    exit 1
fi

# Start Streamlit in background
echo "📝 Starting Journal App (port 8501)..."
cd backend
streamlit run streamlit_app.py --server.port 8501 --server.headless true > ../streamlit.log 2>&1 &
STREAMLIT_PID=$!
cd ..
sleep 3

# Check if Streamlit started
if ps -p $STREAMLIT_PID > /dev/null; then
    echo -e "${GREEN}✓${NC} Journal App started (PID: $STREAMLIT_PID)"
else
    echo -e "${RED}❌ Journal App failed to start${NC}"
    cat streamlit.log
    kill $API_PID 2>/dev/null
    exit 1
fi

echo ""
echo "=========================================="
echo "✨ Mirror is Ready!"
echo "=========================================="
echo ""
echo "📍 Access Points:"
echo "   • Landing Page: http://localhost:5001"
echo "   • Journal App:  http://localhost:8501"
echo "   • API Server:   http://localhost:5001/api"
echo ""
echo "💡 Tips:"
echo "   • Sign up at the landing page"
echo "   • Your data is stored in Supabase"
echo "   • All AI analysis runs locally"
echo ""
echo "📋 Process IDs:"
echo "   • API Server:  $API_PID"
echo "   • Journal App: $STREAMLIT_PID"
echo ""
echo "🛑 To stop: Press Ctrl+C or run:"
echo "   kill $API_PID $STREAMLIT_PID"
echo ""
echo "=========================================="
echo ""

# Keep script running and handle Ctrl+C
trap "echo ''; echo '🛑 Shutting down...'; kill $API_PID $STREAMLIT_PID 2>/dev/null; exit 0" INT

# Wait for processes
wait
