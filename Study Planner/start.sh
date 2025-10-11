#!/bin/bash
echo "Starting AI Gym Planner..."
echo "=============================="

cd "$(dirname "$0")"

echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.7+ from https://python.org"
    exit 1
fi

echo "Checking Flask installation..."
if ! python3 -c "import flask" &> /dev/null; then
    echo "Installing Flask..."
    pip3 install Flask
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to install Flask"
        exit 1
    fi
fi

echo ""
echo "Starting the Gym Planner..."
echo "The app will be available at: http://127.0.0.1:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python3 app.py