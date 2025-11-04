"""Flask API server for handling landing page form submissions."""
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from database import Database
from auth import generate_auth_token

# Get frontend directory path - resolve to absolute path
BASE_DIR = Path(__file__).parent.parent.resolve()
FRONTEND_DIR = BASE_DIR / 'frontend' / 'dist'  # Serve built React app from dist

# Ensure frontend directory exists
if not FRONTEND_DIR.exists():
    print(f"⚠️  Frontend dist directory not found: {FRONTEND_DIR}")
    print("Please run 'npm run build' in the frontend directory first.")
    raise FileNotFoundError(f"Frontend dist directory not found: {FRONTEND_DIR}")

# Create Flask app - don't use static_folder to avoid conflicts with manual routing
app = Flask(__name__)
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "http://localhost:3000",  # Vite dev server
            "http://localhost:5000",  # Production build server
            "http://127.0.0.1:3000", 
            "http://127.0.0.1:5000",
            "http://127.0.0.1:5001"  # Self
        ],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})  # Enable CORS for frontend (dev & production)

# Configure Flask to allow serving files from frontend directory
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # Disable caching in dev
app.config['PREFERRED_URL_SCHEME'] = 'http'

db = Database()

# Debug: Print paths
print(f"Frontend dist directory: {FRONTEND_DIR}")
print(f"Index.html exists: {(FRONTEND_DIR / 'index.html').exists()}")
print(f"Assets directory exists: {(FRONTEND_DIR / 'assets').exists()}")


@app.route('/api/signup', methods=['POST'])
def signup():
    """Handle user signup from landing page with comprehensive profiling."""
    try:
        data = request.get_json()
        
        # Extract all form fields
        email = data.get('email')
        name = data.get('name')
        age_group = data.get('ageGroup')
        occupation = data.get('occupation')
        journaling_experience = data.get('journalingExperience')
        primary_goal = data.get('primaryGoal')
        emotional_challenges = data.get('emotionalChallenges', '')
        preferred_reflection_time = data.get('preferredReflectionTime')
        
        # Validate required fields
        if not email or not name:
            return jsonify({'error': 'Email and name are required'}), 400
        
        if not age_group or not occupation:
            return jsonify({'error': 'Age group and occupation are required'}), 400
            
        if not journaling_experience or not primary_goal or not preferred_reflection_time:
            return jsonify({'error': 'Please complete all required fields'}), 400
        
        # Create comprehensive onboarding data
        onboarding_data = {
            'age_group': age_group,
            'occupation': occupation,
            'journaling_experience': journaling_experience,
            'primary_goal': primary_goal,
            'emotional_challenges': emotional_challenges,
            'preferred_reflection_time': preferred_reflection_time,
            'profile_completed_at': 'timestamp'  # Will be set by database
        }
        
        # Create user with comprehensive profile
        user_id = db.create_user(email, name, onboarding_data)
        
        # Generate JWT token for authentication
        auth_token = generate_auth_token(user_id, email, name)
        
        # Get Streamlit URL from environment or use default
        streamlit_url = os.getenv('STREAMLIT_URL', 'http://localhost:8501')
        redirect_url = f"{streamlit_url}?auth_token={auth_token}"
        
        return jsonify({
            'success': True,
            'user_id': user_id,
            'auth_token': auth_token,
            'redirect_url': redirect_url,
            'message': 'Profile created successfully! Redirecting to your dashboard...'
        }), 201
    
    except Exception as e:
        print(f"Error in signup: {str(e)}")  # Debug logging
        return jsonify({'error': str(e)}), 500


@app.route('/api/user/<email>', methods=['GET'])
def get_user(email):
    """Get user by email."""
    try:
        user = db.get_user_by_email(email)
        if user:
            return jsonify(user), 200
        else:
            return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Serve React/Vite built files
@app.route('/')
def index():
    """Serve React landing page."""
    try:
        return send_from_directory(str(FRONTEND_DIR), 'index.html', mimetype='text/html')
    except Exception as e:
        return f"Error serving index.html: {str(e)}", 500


@app.route('/assets/<path:path>')
def serve_assets(path):
    """Serve Vite built assets (JS, CSS, images)."""
    try:
        assets_dir = FRONTEND_DIR / 'assets'
        if not assets_dir.exists():
            return "Assets directory not found", 404
        return send_from_directory(str(assets_dir), path)
    except Exception as e:
        return f"Error serving asset: {str(e)}", 500


@app.route('/<path:path>')
def serve_static_files(path):
    """Serve other static files (vite.svg, etc.)."""
    try:
        file_path = FRONTEND_DIR / path
        if file_path.exists() and file_path.is_file():
            return send_from_directory(str(FRONTEND_DIR), path)
        # If file doesn't exist, fall through to 404 handler which serves index.html
        return not_found(None)
    except Exception as e:
        return not_found(None)


# Catch-all route for React Router - serve index.html for client-side routing
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors - serve index.html for React Router."""
    # Serve index.html for all non-API routes (React Router will handle routing)
    if not request.path.startswith('/api'):
        try:
            return send_from_directory(str(FRONTEND_DIR), 'index.html', mimetype='text/html')
        except:
            return "Page not found", 404
    return "API endpoint not found", 404


if __name__ == '__main__':
    # Run on port 5001 for API (landing page is on 5000)
    # Use host='0.0.0.0' to allow connections from all interfaces
    # Use threaded=True for better performance
    print("\n" + "="*60)
    print("🚀 Starting Mirror Flask API Server")
    print("="*60)
    print(f"🌐 API Server: http://localhost:5001")
    print(f"📡 Endpoint: http://localhost:5001/api/signup")
    print("="*60 + "\n")
    
    try:
        app.run(host='127.0.0.1', port=5001, debug=False, threaded=True)
    except OSError as e:
        if "Address already in use" in str(e):
            print("\n⚠️  Port 5001 is already in use!")
            print("Please stop the other process or use a different port.\n")
        raise

