@echo off
title EasyKiConverter Web UI Launcher
echo.
echo =====================================
echo   EasyKiConverter Web UI Launcher
echo =====================================
echo.

REM Set project root path
set "project_root=%~dp0"
set "base_path=%project_root%EasyKiConverter"

REM Check for Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH.
    echo Please install Python 3.7+ and add it to the system PATH.
    pause
    exit /b 1
)

echo Checking for virtual environment...

REM Check for existing virtual environments
set "venv_path="
if exist "%project_root%venv\Scripts\activate.bat" (
    set "venv_path=%project_root%venv"
    echo Found virtual environment: venv
) else if exist "%project_root%.venv\Scripts\activate.bat" (
    set "venv_path=%project_root%.venv"
    echo Found virtual environment: .venv
) else if exist "%project_root%env\Scripts\activate.bat" (
    set "venv_path=%project_root%env"
    echo Found virtual environment: env
) else (
    echo No virtual environment found. Creating new virtual environment...
    python -m venv "%project_root%venv"
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment.
        echo Please ensure you have the venv module installed.
        pause
        exit /b 1
    )
    set "venv_path=%project_root%venv"
    echo Virtual environment created successfully: venv
)

REM Activate virtual environment
echo Activating virtual environment...
call "%venv_path%\Scripts\activate.bat"
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment.
    pause
    exit /b 1
)

echo Virtual environment activated: %venv_path%
echo.

REM Upgrade pip in virtual environment
echo Upgrading pip...
python -m pip install --upgrade pip >nul 2>&1

echo Installing dependencies...

REM Install main requirements if exists
if exist "%base_path%\requirements.txt" (
    echo Installing main project dependencies...
    pip install -r "%base_path%\requirements.txt"
    if errorlevel 1 (
        echo WARNING: Some main dependencies failed to install.
    )
) else (
    echo WARNING: Main requirements file not found, skipping.
)

REM Install Web UI requirements
echo Installing Web UI dependencies...
pip install -r "%base_path%\Web_Ui\requirements.txt"
if errorlevel 1 (
    echo ERROR: Failed to install Web UI dependencies.
    echo Please check your internet connection and try again.
    pause
    exit /b 1
)

echo.
echo Dependencies installed successfully!
echo.
echo Starting Web UI server...
echo.
echo Virtual Environment: %venv_path%
echo Server URL: http://localhost:8000
echo.
echo After startup, your browser will open automatically.
echo If it does not, please navigate to http://localhost:8000 manually.
echo.
echo Press Ctrl+C to stop the server.
echo.

REM Change to the Web UI directory and start the server
cd /d "%base_path%\Web_Ui"

REM Start server and open browser
start "" http://localhost:8000
python app.py

echo.
echo Server stopped. Deactivating virtual environment...
deactivate
pause