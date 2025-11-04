# Mirror MVP - Complete Setup ✅

## Architecture Overview

### Frontend (React + Tailwind CSS)
- **Technology**: React 18, Vite, Tailwind CSS
- **Port**: 5000 (production) or 3000 (development)
- **Location**: `frontend/`
- **Components**: 
  - Hero section with animated mirror icon
  - How It Works feature cards
  - Signup form with validation
  - Footer with links

### Backend Services

1. **API Server** (Flask)
   - **Port**: 5001
   - **File**: `backend/api_server.py`
   - **Endpoints**:
     - `POST /api/signup` - Create user account
     - `GET /api/user/<email>` - Get user by email
   - **CORS**: Enabled for React frontend

2. **Journal App** (Streamlit)
   - **Port**: 8501
   - **File**: `backend/app.py`
   - **Features**: Journaling, timeline, summaries, insights

3. **Database** (SQLite)
   - **File**: `mirror.db` (created automatically)
   - **Schema**: users, journal_entries, biases, weekly_summaries

## Quick Start

### Option 1: Automated (Recommended)
```bash
./start.sh
```

### Option 2: Manual
```bash
# Terminal 1: API Server
cd backend && python api_server.py

# Terminal 2: Landing Page
cd backend && python serve_react.py 5000

# Terminal 3: Streamlit Journal
cd backend && streamlit run app.py
```

## First Time Setup

1. **Install Python dependencies:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Install Node.js dependencies:**
   ```bash
   cd frontend
   npm install
   npm run build
   ```

3. **Run the application:**
   ```bash
   ./start.sh
   ```

## User Flow

1. User visits **http://localhost:5000** (Landing Page)
2. Fills out signup form (email, name, goals, experience)
3. Form submits to **http://localhost:5001/api/signup**
4. User is redirected to **http://localhost:8501** (Journal App)
5. User signs in with their email
6. Can start journaling immediately

## Key Features Implemented

✅ Modern React frontend with Tailwind CSS
✅ Responsive design (mobile-friendly)
✅ Smooth animations and transitions
✅ Form validation and error handling
✅ API integration with Flask backend
✅ CORS configured for cross-origin requests
✅ React Router support (SPA routing)
✅ Production-ready build process
✅ Streamlit journal interface
✅ Complete database schema
✅ Sentiment analysis
✅ Cognitive bias detection
✅ Emotional timeline visualization
✅ Weekly summary generation

## Troubleshooting

### React build fails
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run build
```

### Port conflicts
```bash
# Kill processes on ports
lsof -ti:5000 | xargs kill -9
lsof -ti:5001 | xargs kill -9
lsof -ti:8501 | xargs kill -9
```

### CORS errors
- Make sure API server is running on port 5001
- Check that CORS is configured in `backend/api_server.py`
- Verify API URL in `frontend/src/utils/api.js`

## Development

### Frontend Development
```bash
cd frontend
npm run dev
```
Runs on http://localhost:3000 with hot reload

### Rebuild Frontend
```bash
cd frontend
npm run build
```

## Production Deployment

1. Build React frontend: `cd frontend && npm run build`
2. Serve `frontend/dist/` via `backend/serve_react.py`
3. Run API server: `python backend/api_server.py`
4. Run Streamlit: `streamlit run backend/app.py`

## File Structure

```
Mirror/
├── frontend/              # React + Tailwind CSS
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── pages/         # Page components
│   │   └── utils/         # API utilities
│   ├── dist/             # Production build
│   └── package.json
├── backend/
│   ├── app.py            # Streamlit journal app
│   ├── api_server.py     # Flask API server
│   ├── serve_react.py    # React build server
│   └── [other modules]
└── start.sh              # Startup script
```

## Status: ✅ MVP COMPLETE

All features are implemented and integrated. The application is ready for use!

