@echo off
echo.
echo ===============================================
echo    KKCG Analytics System Startup
echo ===============================================
echo.

:: Set the base directory
set BASE_DIR=%~dp0

:: Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python and try again
    pause
    exit /b 1
)

echo ✅ Python found
echo.

:: Stop any existing services
echo 🛑 Stopping any existing services...
taskkill /f /im uvicorn.exe >nul 2>&1
taskkill /f /im python.exe >nul 2>&1
taskkill /f /im streamlit.exe >nul 2>&1
echo ✅ Previous services stopped
echo.

:: Start FastAPI Backend for Forecasting Tool
echo 🚀 Starting FastAPI Backend for Forecasting Tool...
cd /d "%BASE_DIR%FORECASTER\backend"
if not exist "app" (
    echo ❌ Backend directory not found at %BASE_DIR%FORECASTER\backend
    echo The forecasting tool will use sample data instead
    goto start_frontend
)

:: Install backend dependencies if needed
echo 📦 Checking backend dependencies...
pip install fastapi uvicorn pandas scikit-learn plotly >nul 2>&1

:: Start backend in background
echo 📡 Launching FastAPI server on http://localhost:8000...
start "KKCG FastAPI Backend" /min cmd /c "cd /d "%BASE_DIR%FORECASTER\backend" && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

:: Wait for backend to start and test connectivity
echo ⏳ Waiting for backend to initialize...
set /a counter=0
:check_backend
timeout /t 2 /nobreak >nul
curl http://localhost:8000/health >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Backend is online and responding
    goto start_frontend
)
set /a counter+=1
if %counter% lss 15 (
    echo    ... still waiting (%counter%/15)
    goto check_backend
)
echo ⚠️ Backend may still be starting (continuing with frontend)

:start_frontend
:: Navigate to KKCG App directory
echo.
echo 🎨 Starting KKCG Analytics Dashboard...
cd /d "%BASE_DIR%kkcg_app"

:: Check if frontend dependencies are installed
echo 📦 Installing/updating Streamlit dependencies...
pip install streamlit plotly pandas numpy requests >nul 2>&1

:: Start Streamlit app
echo 🌐 Launching KKCG Analytics Dashboard...
echo    - Forecasting Tool (with API integration)
echo    - Heatmap Analytics Tool
echo    - Beautiful Dark Mode UI
echo.

:: Start Streamlit and open browser
start "KKCG Analytics Dashboard" /min cmd /c "cd /d "%BASE_DIR%kkcg_app" && streamlit run Home.py --server.port 8501 --server.headless false"

:: Wait for Streamlit to start
echo ⏳ Waiting for Streamlit to start...
timeout /t 5 /nobreak >nul

:: Test backend connectivity again
curl http://localhost:8000/health >nul 2>&1
if %errorlevel% equ 0 (
    set BACKEND_STATUS=🟢 ONLINE
) else (
    set BACKEND_STATUS=🔴 OFFLINE (Demo Mode Available)
)

:: Open browser to the dashboard
echo 🌍 Opening browser to http://localhost:8501...
timeout /t 2 /nobreak >nul
start http://localhost:8501

echo.
echo ===============================================
echo    KKCG System Successfully Started!
echo ===============================================
echo.
echo.
echo [ACCESS POINTS]
echo    * Main Dashboard: http://localhost:8501
echo    * API Backend:    http://localhost:8000 - %BACKEND_STATUS%
echo    * API Docs:       http://localhost:8000/docs
echo.
echo [AVAILABLE TOOLS]
echo    * AI Forecasting Tool (with live API integration)
echo    * Heatmap Analytics Tool  
echo    * Business Intelligence Dashboard
echo.
echo [INSTRUCTIONS]
echo    - Use the sidebar to navigate between tools
echo    - Forecasting tool has full API integration
echo    - Backend runs in demo mode (no external dependencies)
echo    - Close service windows or press Ctrl+C to stop services
echo.
echo [TROUBLESHOOTING]
echo    - If backend shows offline, refresh the forecasting page
echo    - Sample data will be used if backend is unavailable
echo    - Both services run independently for maximum reliability
echo.
echo Happy analyzing!
echo.
pause 