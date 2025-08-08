@echo off
title EasyKiConverter Web UI Launcher
echo.
echo =====================================
echo   EasyKiConverter Web UI Launcher
echo =====================================
echo.

REM Check for Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH.
    echo Please install Python 3.7+ and add it to the system PATH.
    pause
    exit /b 1
)

echo Installing dependencies...

REM Set base path
set "base_path=%~dp0EasyKiConverter"

REM Install main requirements
if exist "%base_path%\requirements.txt" (
    pip install -r "%base_path%\requirements.txt"
) else (
    echo WARNING: Main requirements file not found, skipping.
)

REM Install Web UI requirements
pip install -r "%base_path%\Web_Ui\requirements.txt"
if errorlevel 1 (
    echo ERROR: Failed to install Web UI dependencies.
    pause
    exit /b 1
)

echo.
echo Starting Web UI server...
echo.
echo After startup, your browser will open to http://localhost:8000
echo If it does not, please navigate to that address manually.
echo.
echo Press Ctrl+C to stop the server.
echo.

REM Change to the Web UI directory and start the server
cd /d "%base_path%\Web_Ui"

REM Start server and open browser
start "" http://localhost:8000
python app.py

pause