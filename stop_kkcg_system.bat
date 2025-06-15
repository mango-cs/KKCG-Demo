@echo off
echo.
echo ===============================================
echo    🛑 KKCG System Shutdown
echo ===============================================
echo.

echo 🔍 Stopping KKCG services...

:: Stop Streamlit processes
echo 📱 Stopping Streamlit dashboard...
taskkill /f /im "streamlit.exe" >nul 2>&1
taskkill /f /im "python.exe" /fi "WINDOWTITLE eq KKCG Analytics Dashboard*" >nul 2>&1

:: Stop FastAPI backend processes
echo 🔌 Stopping FastAPI backend...
taskkill /f /im "uvicorn.exe" >nul 2>&1
taskkill /f /im "python.exe" /fi "WINDOWTITLE eq KKCG FastAPI Backend*" >nul 2>&1

:: Stop any remaining Python processes related to KKCG
for /f "tokens=2 delims=," %%i in ('tasklist /fi "imagename eq python.exe" /fo csv ^| find "python.exe"') do (
    for /f "tokens=*" %%j in ('netstat -ano ^| find "8000" ^| find "LISTENING"') do (
        taskkill /f /pid %%i >nul 2>&1
    )
)

for /f "tokens=2 delims=," %%i in ('tasklist /fi "imagename eq python.exe" /fo csv ^| find "python.exe"') do (
    for /f "tokens=*" %%j in ('netstat -ano ^| find "8501" ^| find "LISTENING"') do (
        taskkill /f /pid %%i >nul 2>&1
    )
)

:: Close any browser windows with KKCG
echo 🌐 Closing KKCG browser windows...
timeout /t 1 /nobreak >nul

echo.
echo ✅ KKCG system stopped successfully!
echo.
echo 🔄 Services terminated:
echo    - Streamlit Dashboard (port 8501)
echo    - FastAPI Backend (port 8000)
echo    - Related browser windows
echo.
echo 💡 You can restart using:
echo    - start_kkcg_system.bat (Full system)
echo    - start_kkcg_app_only.bat (Dashboard only)
echo.
pause 