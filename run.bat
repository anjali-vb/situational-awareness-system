@echo off
REM Situational Awareness System - WebSocket Server Launcher
REM This script sets up the environment and starts the server

setlocal enabledelayedexpansion

echo.
echo ============================================
echo Situational Awareness System - Server Setup
echo ============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.9 or higher from https://www.python.org/
    pause
    exit /b 1
)

echo [1/4] Python found: 
python --version
echo.

REM Check if virtual environment exists, if not create it
if not exist ".venv" (
    echo [2/4] Creating virtual environment...
    python -m venv .venv
    if %errorlevel% neq 0 (
        echo Error: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo Virtual environment created successfully
) else (
    echo [2/4] Virtual environment already exists
)
echo.

REM Activate virtual environment
echo [3/4] Activating virtual environment and installing dependencies...
call .venv\Scripts\activate.bat

REM Install package with dependencies
pip install -e . >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Failed to install package dependencies
    pause
    exit /b 1
)
echo Package and dependencies installed successfully
echo.

REM Start the server
echo [4/4] Starting WebSocket server...
echo.
echo ============================================
echo Server is running!
echo ============================================
echo.
echo WebSocket Server: ws://localhost:8765
echo.
echo To access the application:
echo 1. Open src\index.html in your web browser
echo 2. Or navigate to: file:///%cd:\=/%/src/index.html
echo.
echo Press Ctrl+C to stop the server
echo.
echo ============================================
echo.

python src\server.py

REM If server exits abnormally, pause to show error
if %errorlevel% neq 0 (
    echo.
    echo Server stopped with errors. Press any key to continue...
    pause
)
