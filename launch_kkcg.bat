@echo off
title KKCG Analytics System Launcher
color 0F

:menu
cls
echo.
echo ===============================================
echo          KKCG Analytics System
echo ===============================================
echo.
echo Please select an option:
echo.
echo 1) Start Full System (Backend + Dashboard)
echo 2) Start Dashboard Only (Quick)
echo 3) Stop All Services  
echo 4) View Documentation
echo 5) Exit
echo.
echo ===============================================
echo.
set /p choice=Enter your choice (1-5): 

if "%choice%"=="1" goto full_system
if "%choice%"=="2" goto dashboard_only
if "%choice%"=="3" goto stop_system
if "%choice%"=="4" goto documentation
if "%choice%"=="5" goto exit
echo Invalid choice. Please try again.
timeout /t 2 >nul
goto menu

:full_system
cls
echo.
echo [STARTING] Full KKCG System...
echo    - FastAPI Backend (port 8000)
echo    - Streamlit Dashboard (port 8501)
echo    - Browser auto-launch
echo.
call start_kkcg_system.bat
goto menu

:dashboard_only  
cls
echo.
echo [STARTING] KKCG Dashboard Only...
echo    - Streamlit Dashboard (port 8501)
echo    - Sample data mode
echo    - Browser auto-launch
echo.
call start_kkcg_app_only.bat
goto menu

:stop_system
cls
echo.
echo [STOPPING] KKCG System...
echo.
call stop_kkcg_system.bat
goto menu

:documentation
cls
echo.
echo [DOCS] Opening Documentation...
echo.
if exist "BATCH_FILES_README.md" (
    start notepad "BATCH_FILES_README.md"
) else (
    echo [ERROR] Documentation file not found
    echo Please ensure BATCH_FILES_README.md exists
)
echo.
pause
goto menu

:exit
cls
echo.
echo Thank you for using KKCG Analytics System!
echo.
echo Built for data-driven restaurant success
echo.
timeout /t 3 >nul
exit 