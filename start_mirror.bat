@echo off
REM Mirror - Windows Auto-Start Script with Browser Launch
REM Opens the application in your browser automatically

color 0A
cls

echo.
echo ==========================================
echo      Mirror - AI Journal Startup
echo ==========================================
echo.

REM Check Python
echo [*] Checking prerequisites...
python --version >nul 2>&1
if errorlevel 1 (
    echo [X] Python is not installed
    echo     Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)
echo [+] Python detected

REM Check Node
node --version >nul 2>&1
if errorlevel 1 (
    echo [X] Node.js is not installed
    echo     Please install Node.js 16+ from https://nodejs.org
    pause
    exit /b 1
)
echo [+] Node.js detected

echo.
echo [*] Installing Python dependencies...
pip install -r requirements.txt --quiet >nul 2>&1
if errorlevel 1 (
    echo [!] Warning: Some dependencies may have failed
) else (
    echo [+] Python dependencies installed
)

REM Download NLTK data
echo [*] Downloading NLTK data...
python -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('brown', quiet=True); nltk.download('vader_lexicon', quiet=True)" >nul 2>&1
echo [+] NLTK data ready

REM Build frontend
echo [*] Building frontend...
cd frontend
if not exist "node_modules" (
    echo [*] Installing Node dependencies (first time)...
    call npm install --silent >nul 2>&1
)
call npm run build --silent >nul 2>&1
if errorlevel 1 (
    echo [X] Frontend build failed
    cd ..
    pause
    exit /b 1
)
echo [+] Frontend built successfully
cd ..

REM Check ports
echo.
echo [*] Checking ports...

REM Kill processes on ports (Windows)
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :5001') do taskkill /F /PID %%a >nul 2>&1
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8501') do taskkill /F /PID %%a >nul 2>&1

timeout /t 1 /nobreak >nul
echo [+] Ports 5001 and 8501 are available

echo.
echo ==========================================
echo         Starting Services
echo ==========================================
echo.

REM Start API Server
echo [*] Starting API Server (port 5001)...
cd backend
start /B python api_server.py > ..\api.log 2>&1
cd ..
timeout /t 2 /nobreak >nul
echo [+] API Server started

REM Start Streamlit
echo [*] Starting Journal App (port 8501)...
cd backend
start /B streamlit run streamlit_app.py --server.port 8501 --server.headless true > ..\streamlit.log 2>&1
cd ..
timeout /t 3 /nobreak >nul
echo [+] Journal App started

echo.
echo ==========================================
echo         Mirror is Ready!
echo ==========================================
echo.
echo [*] Access Points:
echo     - Landing Page: http://localhost:5001
echo     - Journal App:  http://localhost:8501
echo.
echo [*] Opening browser in 3 seconds...
echo.

REM Wait and open browser
timeout /t 3 /nobreak >nul
start http://localhost:5001

echo.
echo [+] All systems operational! Happy journaling!
echo.
echo [*] To stop: Close this window or press Ctrl+C
echo [*] View logs: api.log and streamlit.log
echo.
echo Press any key to view logs, or close window to keep running...
pause >nul

REM Optional: tail logs (requires manual close)
type api.log
echo.
echo ==========================================
echo.
type streamlit.log
