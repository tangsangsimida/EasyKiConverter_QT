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

REM Check for Python installation
echo Checking Python environment...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ERROR: Python is not installed or not found in PATH.
    echo.
    echo Please follow these steps:
    echo 1. Download Python 3.7+ from https://www.python.org/downloads/
    echo 2. During installation, make sure to check "Add Python to PATH"
    echo 3. Restart your command prompt and try again
    echo.
    pause
    exit /b 1
)

REM Get Python version and check if it meets requirements
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set python_version=%%i
echo Python %python_version% detected successfully

REM Check Python version (basic check for 3.x)
echo %python_version% | findstr /r "^3\.[7-9]\|^3\.[1-9][0-9]" >nul
if errorlevel 1 (
    echo %python_version% | findstr /r "^3\." >nul
    if errorlevel 1 (
        echo.
        echo ERROR: Python version %python_version% is not supported.
        echo This project requires Python 3.7 or higher.
        echo Please upgrade your Python installation.
        echo.
        pause
        exit /b 1
    ) else (
        echo WARNING: Python %python_version% detected. Recommended version is 3.7+
        echo Continuing anyway...
    )
)
echo.

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

REM Set up pip mirror for faster downloads in China
echo Setting up pip configuration for faster downloads...
set "PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple"
set "PIP_TRUSTED_HOST=pypi.tuna.tsinghua.edu.cn"

REM Upgrade pip in virtual environment
echo Upgrading pip using Tsinghua mirror...
python -m pip install --upgrade pip -i %PIP_INDEX_URL% --trusted-host %PIP_TRUSTED_HOST% >nul 2>&1
if errorlevel 1 (
    echo Failed to upgrade pip using mirror, trying default source...
    python -m pip install --upgrade pip >nul 2>&1
)

echo Installing dependencies using domestic mirror for faster speed...
echo.

REM Install main requirements if exists
if exist "%base_path%\requirements.txt" (
    echo Installing main project dependencies...
    pip install -r "%base_path%\requirements.txt" -i %PIP_INDEX_URL% --trusted-host %PIP_TRUSTED_HOST%
    if errorlevel 1 (
        echo Some main dependencies failed with mirror, trying default source...
        pip install -r "%base_path%\requirements.txt"
        if errorlevel 1 (
            echo WARNING: Some main dependencies failed to install.
        )
    )
    echo Main dependencies installed successfully!
) else (
    echo WARNING: Main requirements file not found, skipping.
)

REM Install Web UI requirements
echo.
echo Installing Web UI dependencies...
pip install -r "%base_path%\Web_Ui\requirements.txt" -i %PIP_INDEX_URL% --trusted-host %PIP_TRUSTED_HOST%
if errorlevel 1 (
    echo Failed with mirror, trying default source...
    pip install -r "%base_path%\Web_Ui\requirements.txt"
    if errorlevel 1 (
        echo ERROR: Failed to install Web UI dependencies.
        echo Please check your internet connection and try again.
        pause
        exit /b 1
    )
)
echo Web UI dependencies installed successfully!

echo.
echo All dependencies installed successfully!
echo.
echo =====================================
echo      Starting Web UI Server
echo =====================================
echo.
echo Virtual Environment: %venv_path%
echo Server URL: http://localhost:8000
echo.
echo Starting server...
echo Your browser will open automatically after startup.
echo If browser doesn't open, manually navigate to: http://localhost:8000
echo.
echo Press Ctrl+C to stop the server when you're done.
echo.

REM Change to the Web UI directory and start the server
cd /d "%base_path%\Web_Ui"

REM Start server and open browser
start "" http://localhost:8000
python app.py

echo.
echo Server stopped. Deactivating virtual environment...
deactivate
echo.
echo Virtual environment deactivated.
echo Thank you for using EasyKiConverter!
echo.
pause