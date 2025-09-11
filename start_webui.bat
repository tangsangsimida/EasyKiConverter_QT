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
    echo Python not found in system PATH. Checking for project-specific Python...
    
    REM Check if project-specific Python exists
    if exist "%project_root%python\python.exe" (
        echo Project-specific Python found.
        set "PYTHON_EXEC=%project_root%python\python.exe"
    ) else (
        echo.
        echo Project-specific Python not found. Downloading Python...
        echo This Python will be used only for this project and will not affect your system Python.
        echo.
        
        REM Create python directory if it doesn't exist
        if not exist "%project_root%python" mkdir "%project_root%python"
        
        REM Try to download Python from the official source first
        echo Downloading Python 3.13.7 from official source...
        powershell -Command "try { Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.13.7/python-3.13.7-amd64.exe' -OutFile '%project_root%python\python-installer.exe' -ErrorAction Stop } catch { exit 1 }"
        
        if errorlevel 1 (
            echo.
            echo ERROR: Failed to download Python from official source.
            echo Trying alternative download method...
            echo.
            
            REM Alternative download method using bitsadmin
            bitsadmin /transfer pythonDownloadJob /download /priority normal "https://www.python.org/ftp/python/3.13.7/python-3.13.7-amd64.exe" "%project_root%python\python-installer.exe"
            
            if errorlevel 1 (
                echo.
                echo ERROR: Failed to download Python using alternative method.
                echo Please check your internet connection and try again.
                echo.
                pause
                exit /b 1
            )
        )
        
        echo Installing Python...
        "%project_root%python\python-installer.exe" /quiet InstallAllUsers=0 PrependPath=0 Include_test=0 TargetDir="%project_root%python"
        
        if errorlevel 1 (
            echo.
            echo ERROR: Failed to install Python.
            echo.
            pause
            exit /b 1
        )
        
        REM Clean up installer
        del "%project_root%python\python-installer.exe"
        
        echo Python installed successfully in project directory!
        set "PYTHON_EXEC=%project_root%python\python.exe"
        
        REM Verify Python installation
        if not exist "%project_root%python\python.exe" (
            echo.
            echo ERROR: Python installation failed. python.exe not found.
            echo.
            pause
            exit /b 1
        )
    )
) else (
    echo System Python found.
    set "PYTHON_EXEC=python"
)

REM Get Python version and check if it meets requirements
for /f "tokens=2" %%i in ('%PYTHON_EXEC% --version 2^>^&1') do set python_version=%%i
echo Python %python_version% detected successfully

REM Check Python version (basic check for 3.x)
echo %python_version% | findstr /r "^3\.[7-9]\|^3\.[1-9][0-9]" >nul
if errorlevel 1 (
    echo %python_version% | findstr /r "^3\." >nul
    if errorlevel 1 (
        echo.
        echo ERROR: Python version %python_version% is not supported.
        echo This project requires Python 3.7 or higher.
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
    %PYTHON_EXEC% -m venv "%project_root%venv"
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
%PYTHON_EXEC% -m pip install --upgrade pip -i %PIP_INDEX_URL% --trusted-host %PIP_TRUSTED_HOST% >nul 2>&1
if errorlevel 1 (
    echo Failed to upgrade pip using mirror, trying default source...
    %PYTHON_EXEC% -m pip install --upgrade pip >nul 2>&1
)

echo Installing dependencies using domestic mirror for faster speed...
echo.

REM Install main requirements if exists
if exist "%base_path%\requirements.txt" (
    echo Installing main project dependencies...
    %PYTHON_EXEC% -m pip install -r "%base_path%\requirements.txt" -i %PIP_INDEX_URL% --trusted-host %PIP_TRUSTED_HOST%
    if errorlevel 1 (
        echo Some main dependencies failed with mirror, trying default source...
        %PYTHON_EXEC% -m pip install -r "%base_path%\requirements.txt"
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
%PYTHON_EXEC% -m pip install -r "%base_path%\Web_Ui\requirements.txt" -i %PIP_INDEX_URL% --trusted-host %PIP_TRUSTED_HOST%
if errorlevel 1 (
    echo Failed with mirror, trying default source...
    %PYTHON_EXEC% -m pip install -r "%base_path%\Web_Ui\requirements.txt"
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