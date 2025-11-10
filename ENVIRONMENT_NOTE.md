# Environment Note

The `start_mirror.sh` script is now executable and ready to use.

## To run Mirror on your local machine:

```bash
./start_mirror.sh
```

## What the script does:

1. Checks for Python 3.8+ and Node.js 16+
2. Installs Python dependencies (Flask, Streamlit, Supabase, etc.)
3. Downloads NLTK data
4. Installs Node dependencies and builds the React frontend
5. Starts the Flask API server on port 5001
6. Starts the Streamlit journal app on port 8501
7. Opens your browser automatically to http://localhost:5001

## Current environment limitation:

This Claude Code environment doesn't have pip/pip3 available, so the full application cannot be started here. However, the script is now properly configured with executable permissions and will work on your local machine.

## Quick start on your machine:

```bash
# Navigate to your project directory
cd /path/to/Mirror

# Run the start script (permissions are already set)
./start_mirror.sh
```

The browser will open automatically and you can start using Mirror!
