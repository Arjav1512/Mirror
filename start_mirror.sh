#!/bin/bash

# Mirror - Enhanced Auto-Start Script with Browser Launch
# Opens the application in your browser automatically

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Clear screen for clean output
clear

echo ""
echo "╔════════════════════════════════════════╗"
echo "║     🧠 Mirror - AI Journal Startup     ║"
echo "╔════════════════════════════════════════╗"
echo ""

# Function to print colored status
print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to open browser
open_browser() {
    local url=$1
    sleep 3  # Wait for server to be fully ready

    if command_exists xdg-open; then
        xdg-open "$url" 2>/dev/null &
    elif command_exists open; then
        open "$url" 2>/dev/null &
    elif command_exists start; then
        start "$url" 2>/dev/null &
    else
        print_warning "Could not auto-open browser. Please open: $url"
    fi
}

# Check prerequisites
echo "📋 Checking prerequisites..."
echo ""

if ! command_exists python3; then
    print_error "Python3 is not installed"
    echo "   Please install Python 3.8+ from https://python.org"
    exit 1
fi
print_status "Python3 detected: $(python3 --version | cut -d' ' -f2)"

if ! command_exists node; then
    print_error "Node.js is not installed"
    echo "   Please install Node.js 16+ from https://nodejs.org"
    exit 1
fi
print_status "Node.js detected: $(node --version | cut -d'v' -f2)"

if ! command_exists npm; then
    print_error "npm is not installed"
    exit 1
fi
print_status "npm detected: $(npm --version)"

echo ""

# Check if .env exists
if [ ! -f ".env" ]; then
    print_warning ".env file not found"
    print_info "Using default configuration"
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
if pip3 install -r requirements.txt --quiet 2>/dev/null; then
    print_status "Python dependencies installed"
else
    print_error "Failed to install Python dependencies"
    exit 1
fi

# Download NLTK data
echo "📚 Downloading NLTK data..."
if python3 -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('brown', quiet=True); nltk.download('vader_lexicon', quiet=True)" >/dev/null 2>&1; then
    print_status "NLTK data ready"
else
    print_warning "NLTK data download had issues (may already exist)"
fi

# Build frontend
echo "🏗️  Building frontend..."
cd frontend
if [ ! -d "node_modules" ]; then
    print_info "Installing Node dependencies (first time)..."
    npm install --silent 2>/dev/null
fi

if npm run build --silent 2>/dev/null; then
    print_status "Frontend built successfully"
else
    print_error "Frontend build failed"
    cd ..
    exit 1
fi
cd ..

# Check if dist folder exists
if [ ! -d "frontend/dist" ]; then
    print_error "Frontend dist folder not found"
    exit 1
fi

echo ""
echo "🔍 Checking ports..."

# Function to kill process on port
kill_port() {
    local port=$1
    local pids=$(lsof -ti:$port 2>/dev/null)
    if [ ! -z "$pids" ]; then
        print_info "Clearing port $port..."
        echo "$pids" | xargs kill -9 2>/dev/null
        sleep 1
    fi
}

# Clear ports
kill_port 5001
kill_port 8501

print_status "Ports 5001 and 8501 are available"

echo ""
echo "╔════════════════════════════════════════╗"
echo "║        🚀 Starting Services            ║"
echo "╔════════════════════════════════════════╗"
echo ""

# Start API Server
print_info "Starting API Server (port 5001)..."
cd backend
python3 api_server.py > ../api.log 2>&1 &
API_PID=$!
cd ..
sleep 2

# Check if API server started
if ps -p $API_PID > /dev/null 2>&1; then
    print_status "API Server started (PID: $API_PID)"
else
    print_error "API Server failed to start"
    echo "   Check api.log for details"
    cat api.log | tail -10
    exit 1
fi

# Start Streamlit
print_info "Starting Journal App (port 8501)..."
cd backend
streamlit run streamlit_app.py --server.port 8501 --server.headless true > ../streamlit.log 2>&1 &
STREAMLIT_PID=$!
cd ..
sleep 3

# Check if Streamlit started
if ps -p $STREAMLIT_PID > /dev/null 2>&1; then
    print_status "Journal App started (PID: $STREAMLIT_PID)"
else
    print_error "Journal App failed to start"
    echo "   Check streamlit.log for details"
    kill $API_PID 2>/dev/null
    cat streamlit.log | tail -10
    exit 1
fi

echo ""
echo "╔════════════════════════════════════════╗"
echo "║         ✨ Mirror is Ready!            ║"
echo "╔════════════════════════════════════════╗"
echo ""
echo "📍 Access Points:"
echo "   • Landing Page: ${BLUE}http://localhost:5001${NC}"
echo "   • Journal App:  ${BLUE}http://localhost:8501${NC}"
echo ""
echo "💡 What to do:"
echo "   1. Sign up at the landing page"
echo "   2. Start journaling your thoughts"
echo "   3. Get AI insights on emotions & patterns"
echo ""
echo "📋 Process IDs:"
echo "   • API Server:  $API_PID"
echo "   • Journal App: $STREAMLIT_PID"
echo ""
echo "🛑 To stop: Press ${RED}Ctrl+C${NC} or run:"
echo "   ${YELLOW}kill $API_PID $STREAMLIT_PID${NC}"
echo ""
echo "📊 View Logs:"
echo "   ${YELLOW}tail -f api.log streamlit.log${NC}"
echo ""

# Open browser automatically
print_info "Opening browser in 3 seconds..."
open_browser "http://localhost:5001" &

echo ""
echo "════════════════════════════════════════"
echo ""
print_status "All systems operational! Happy journaling! 🎉"
echo ""
echo "Keeping services running... (Press Ctrl+C to stop)"
echo ""

# Create a shutdown handler
cleanup() {
    echo ""
    echo ""
    print_info "Shutting down Mirror..."
    kill $API_PID 2>/dev/null
    kill $STREAMLIT_PID 2>/dev/null
    sleep 1
    print_status "Services stopped. Goodbye!"
    exit 0
}

# Trap Ctrl+C and cleanup
trap cleanup INT TERM

# Keep script running and monitor processes
while true; do
    # Check if processes are still running
    if ! ps -p $API_PID > /dev/null 2>&1; then
        print_error "API Server stopped unexpectedly"
        kill $STREAMLIT_PID 2>/dev/null
        exit 1
    fi

    if ! ps -p $STREAMLIT_PID > /dev/null 2>&1; then
        print_error "Journal App stopped unexpectedly"
        kill $API_PID 2>/dev/null
        exit 1
    fi

    sleep 5
done
