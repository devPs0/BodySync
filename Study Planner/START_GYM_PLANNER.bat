@echo off
cls
echo.
echo 🏋️ AI GYM PLANNER STARTER 🏋️
echo ================================
echo.
echo Starting your Gym Planner application...
echo.

cd /d "%~dp0"

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Python is not installed!
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

echo ✅ Python found
echo ✅ Gemini API configured
echo ✅ Starting Flask server...
echo.
echo 🌐 Your Gym Planner will be available at:
echo    👉 http://127.0.0.1:5000
echo.
echo 📋 Quick Setup:
echo    1. Go to http://127.0.0.1:5000
echo    2. Click "Register" to create an account
echo    3. Or login with existing account:
echo       Username: dev
echo       Password: devps0123
echo.
echo ⚠️  Keep this window open while using the app
echo 🛑 Press Ctrl+C to stop the server
echo.
echo ================================
echo.

python app.py

echo.
echo 👋 Gym Planner stopped. Press any key to exit.
pause >nul