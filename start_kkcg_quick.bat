@echo off
echo ===============================================
echo    KKCG Analytics System - Quick Start
echo ===============================================
echo.

:: Stop any existing processes
echo [CLEANUP] Stopping existing services...
taskkill /f /im python.exe >nul 2>&1
echo Done.
echo.

:: Start Backend
echo [BACKEND] Starting FastAPI server...
cd FORECASTER\backend
start "KKCG Backend" /min powershell -Command "python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
cd ..\..
echo Backend starting on http://localhost:8000
echo.

:: Wait for backend
echo [WAIT] Waiting for backend to initialize...
timeout /t 8 /nobreak >nul

:: Start Frontend  
echo [FRONTEND] Starting Streamlit dashboard...
cd kkcg_app
start "KKCG Dashboard" /min powershell -Command "streamlit run Home.py --server.port 8501"
cd ..
echo Dashboard starting on http://localhost:8501
echo.

:: Wait and open browser
echo [BROWSER] Opening dashboard in browser...
timeout /t 5 /nobreak >nul
start http://localhost:8501

echo.
echo ===============================================
echo    System Started Successfully!
echo ===============================================
echo.
echo [ACCESS POINTS]
echo    * Dashboard: http://localhost:8501
echo    * Backend:   http://localhost:8000
echo    * API Docs:  http://localhost:8000/docs
echo.
echo [STATUS]
echo    - Backend: FastAPI server with demo data
echo    - Frontend: Streamlit dashboard
echo    - Forecasting Tool: Should show "Backend Online"
echo.
echo Press any key to close this window...
pause >nul 