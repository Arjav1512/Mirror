#!/bin/bash

# Mirror - Start All Services
# This script starts all three services in separate terminal tabs/windows

echo "🚀 Starting Mirror - All Services"
echo "=================================="
echo ""

# Check if .env files exist
if [ ! -f "backend/.env" ]; then
    echo "⚠️  Creating backend/.env from example..."
    cp backend/.env.example backend/.env 2>/dev/null || cat > backend/.env << 'EOF'
JWT_SECRET=mirror-secret-key-change-in-production
LANDING_PAGE_URL=http://localhost:3000
STREAMLIT_URL=http://localhost:8501
EOF
fi

if [ ! -f "frontend/.env" ]; then
    echo "⚠️  Creating frontend/.env from example..."
    cp frontend/.env.example frontend/.env 2>/dev/null || cat > frontend/.env << 'EOF'
VITE_API_URL=http://localhost:5001
VITE_STREAMLIT_URL=http://localhost:8501
EOF
fi

echo "✅ Environment files ready"
echo ""

# Test JWT authentication
echo "🔐 Testing JWT authentication..."
python test_auth.py
if [ $? -ne 0 ]; then
    echo "❌ JWT authentication test failed!"
    exit 1
fi
echo ""

echo "📋 Starting services..."
echo ""
echo "Please start these in separate terminals:"
echo ""
echo "Terminal 1 - API Server:"
echo "  cd $(pwd) && python backend/api_server.py"
echo ""
echo "Terminal 2 - Streamlit Dashboard:"
echo "  cd $(pwd) && streamlit run backend/app.py"
echo ""
echo "Terminal 3 - Frontend:"
echo "  cd $(pwd)/frontend && npm run dev"
echo ""
echo "=================================="
echo ""
echo "📍 URLs:"
echo "  Landing Page: http://localhost:3000"
echo "  API Server:   http://localhost:5001"
echo "  Dashboard:    http://localhost:8501"
echo ""
echo "🧪 Test Flow:"
echo "  1. Visit http://localhost:3000"
echo "  2. Fill signup form"
echo "  3. Submit"
echo "  4. Should redirect to http://localhost:8501 (auto-logged in)"
echo ""
echo "=================================="
