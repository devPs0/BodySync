@echo off
echo Starting AI Gym Planner...
echo ==============================

cd /d "%~dp0"

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://python.org
    pause
    exit /b 1
)

echo Checking Flask installation...
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo Installing Flask...
    pip install Flask
    if errorlevel 1 (
        echo ERROR: Failed to install Flask
        pause
        exit /b 1
    )
)

echo.
echo Starting the Gym Planner...
echo The app will be available at: http://127.0.0.1:5000
echo.
echo Press Ctrl+C to stop the server
echo.

python app.py

pause