@echo off
echo.
echo ===============================================
echo    🍛 KKCG Analytics Dashboard - Quick Start
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

:: Navigate to KKCG App directory
echo 🎨 Starting KKCG Analytics Dashboard...
cd /d "%BASE_DIR%kkcg_app"

:: Install dependencies if needed
echo 📦 Checking dependencies...
pip install -r requirements.txt >nul 2>&1

echo.
echo 🌐 Launching KKCG Analytics Dashboard...
echo    - Forecasting Tool (sample data mode)
echo    - Heatmap Analytics Tool
echo    - Beautiful Dark Mode UI
echo.

:: Start Streamlit app
start "KKCG Analytics Dashboard" cmd /k "streamlit run Home.py --server.port 8501"

:: Wait for startup
timeout /t 3 /nobreak >nul

:: Open browser
echo 🌍 Opening browser to http://localhost:8501...
start http://localhost:8501

echo.
echo ✅ KKCG Dashboard Started Successfully!
echo.
echo 📊 Access: http://localhost:8501
echo 💡 Use sidebar to navigate between tools
echo ⏹️  Close the Streamlit window to stop
echo.
pause 