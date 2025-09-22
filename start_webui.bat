@echo off
REM Enhanced version with better error handling and Windows compatibility
setlocal enabledelayedexpansion

REM Set console code page to UTF-8 for better compatibility
chcp 65001 >nul 2>&1

REM Set error handling
title EasyKiConverter Web UI Launcher
echo.
echo =====================================
echo   EasyKiConverter Web UI Launcher
echo =====================================
echo.

REM Set project root path with proper quoting
set "PROJECT_ROOT=%~dp0"
if "%PROJECT_ROOT:~-1%"=="\" set "PROJECT_ROOT=%PROJECT_ROOT:~0,-1%"
set "BASE_PATH=%PROJECT_ROOT%\EasyKiConverter"

echo [INFO] Project root: %PROJECT_ROOT%
echo [INFO] Base path: %BASE_PATH%

REM Check if base directory exists
if not exist "%BASE_PATH%" (
    echo [ERROR] EasyKiConverter directory not found!
    echo Expected path: %BASE_PATH%
    echo.
    echo Please ensure you are running this script from the correct location.
    echo.
    echo Press any key to exit...
    pause >nul
    exit /b 1
)

REM Initialize Python executable variable
set "PYTHON_EXEC="

REM Check for system Python first
echo [INFO] Checking for Python installation...
where python >nul 2>&1
if !errorlevel! equ 0 (
    for /f "tokens=*" %%i in ('where python') do set "PYTHON_EXEC=%%i"
    echo [INFO] System Python found: !PYTHON_EXEC!
) else (
    where python3 >nul 2>&1
    if !errorlevel! equ 0 (
        for /f "tokens=*" %%i in ('where python3') do set "PYTHON_EXEC=%%i"
        echo [INFO] System Python3 found: !PYTHON_EXEC!
    )
)

REM If no system Python, check for project-specific Python
if not defined PYTHON_EXEC (
    echo [INFO] No system Python found. Checking for project-specific Python...
    call :find_project_python
) else (
    REM Verify system Python works
    "!PYTHON_EXEC!" --version >nul 2>&1
    if !errorlevel! neq 0 (
        echo [WARNING] System Python verification failed. Trying project Python...
        set "PYTHON_EXEC="
        call :find_project_python
    )
)

REM If still no Python, offer to download
if not defined PYTHON_EXEC (
    echo.
    echo [ERROR] No Python installation found!
    echo.
    choice /C YN /M "Would you like to download and install Python 3.13.7 automatically"
    if !errorlevel! equ 1 (
        call :download_python
        if !errorlevel! neq 0 (
            echo [ERROR] Python download/installation failed!
            echo.
            echo Please install Python manually from https://www.python.org/downloads/
            echo.
            echo Press any key to exit...
            pause >nul
            exit /b 1
        )
    ) else (
        echo.
        echo Please install Python 3.7 or higher and try again.
        echo.
        echo Press any key to exit...
        pause >nul
        exit /b 1
    )
)

echo [SUCCESS] Using Python: !PYTHON_EXEC!

REM Check Python version
echo [INFO] Checking Python version...
for /f "tokens=2" %%i in ('"!PYTHON_EXEC!" --version 2^>^&1') do set "PYTHON_VERSION=%%i"
echo [INFO] Python !PYTHON_VERSION! detected

REM Basic version check
echo !PYTHON_VERSION! | findstr /r "^3\.[7-9]\|^3\.[1-9][0-9]" >nul
if !errorlevel! neq 0 (
    echo !PYTHON_VERSION! | findstr /r "^3\." >nul
    if !errorlevel! neq 0 (
        echo [ERROR] Python !PYTHON_VERSION! is not supported. This project requires Python 3.7 or higher.
        echo.
        echo Press any key to exit...
        pause >nul
        exit /b 1
    ) else (
        echo [WARNING] Python !PYTHON_VERSION! detected. Recommended version is 3.7+
        echo Continuing anyway...
    )
)

REM Setup virtual environment
echo [INFO] Setting up virtual environment...
call :setup_venv
if !errorlevel! neq 0 (
    echo [ERROR] Virtual environment setup failed!
    echo.
    echo Press any key to exit...
    pause >nul
    exit /b 1
)

REM Install dependencies
echo [INFO] Installing dependencies...
call :install_deps
if !errorlevel! neq 0 (
    echo [ERROR] Dependency installation failed!
    echo.
    echo Press any key to exit...
    pause >nul
    exit /b 1
)

REM Start Web UI
echo [INFO] Starting Web UI server...
call :start_server
if !errorlevel! neq 0 (
    echo [ERROR] Failed to start Web UI server!
    echo.
    echo Press any key to exit...
    pause >nul
    exit /b 1
)

REM Cleanup
echo.
echo [INFO] Cleaning up...
deactivate >nul 2>&1
echo [INFO] Virtual environment deactivated.
echo.
echo Thank you for using EasyKiConverter!
echo.
echo Press any key to exit...
pause >nul
exit /b 0

REM =============================================================================
REM Function Definitions
REM =============================================================================

:find_project_python
REM Find Python in project directory
set "PYTHON_FOUND=0"
for %%p in (python.exe python3.13.exe python3.12.exe python3.11.exe python3.10.exe python3.9.exe python3.exe) do (
    if exist "%PROJECT_ROOT%python\%%p" (
        set "PYTHON_EXEC=%PROJECT_ROOT%python\%%p"
        set "PATH=%PROJECT_ROOT%python;%PATH%"
        echo [INFO] Found project Python: !PYTHON_EXEC!
        set "PYTHON_FOUND=1"
        goto :verify_project_python
    )
)

:verify_project_python
if !PYTHON_FOUND! equ 1 (
    "!PYTHON_EXEC!" --version >nul 2>&1
    if !errorlevel! equ 0 (
        echo [INFO] Project Python verification successful
        exit /b 0
    ) else (
        echo [WARNING] Project Python verification failed
        set "PYTHON_EXEC="
        set "PYTHON_FOUND=0"
        exit /b 1
    )
) else (
    echo [INFO] No project Python found
    exit /b 1
)

:download_python
REM Download and install Python
set "PYTHON_INSTALL_DIR=%PROJECT_ROOT%python"

echo [INFO] Creating Python installation directory...
if not exist "%PYTHON_INSTALL_DIR%" (
    mkdir "%PYTHON_INSTALL_DIR%"
    if !errorlevel! neq 0 (
        echo [ERROR] Failed to create Python directory!
        exit /b 1
    )
)

echo [INFO] Downloading Python 3.13.7...
echo This may take a few minutes depending on your internet connection.

REM Try curl first
curl -L -o "%TEMP%\python-3.13.7-amd64.zip" "https://mirrors.ustc.edu.cn/python/3.13.7/python-3.13.7-amd64.zip" >nul 2>&1
if !errorlevel! equ 0 (
    echo [INFO] Download successful, extracting...
    powershell -Command "Expand-Archive -Path '%TEMP%\python-3.13.7-amd64.zip' -DestinationPath '%PYTHON_INSTALL_DIR%' -Force" >nul 2>&1
    if !errorlevel! equ 0 (
        del "%TEMP%\python-3.13.7-amd64.zip" >nul 2>&1
        set "PYTHON_EXEC=%PYTHON_INSTALL_DIR%\python.exe"
        set "PATH=%PYTHON_INSTALL_DIR%;%PATH%"
        
        REM Verify installation
        "!PYTHON_EXEC!" --version >nul 2>&1
        if !errorlevel! equ 0 (
            echo [SUCCESS] Python installed successfully!
            exit /b 0
        ) else (
            echo [ERROR] Python installation verification failed!
            exit /b 1
        )
    ) else (
        echo [ERROR] Failed to extract Python!
        exit /b 1
    )
) else (
    echo [ERROR] Download failed! Please check your internet connection.
    exit /b 1
)

:setup_venv
REM Setup virtual environment
set "VENV_CREATED=0"

REM Check for existing virtual environments
for %%v in (venv .venv env) do (
    if exist "%PROJECT_ROOT%\%%v\Scripts\activate.bat" (
        set "VENV_PATH=%PROJECT_ROOT%\%%v"
        echo [INFO] Found existing virtual environment: %%v
        set "VENV_CREATED=1"
        goto :activate_venv
    )
)

REM Create new virtual environment
if !VENV_CREATED! equ 0 (
    echo [INFO] Creating new virtual environment...
    "!PYTHON_EXEC!" -m venv "%PROJECT_ROOT%\venv"
    if !errorlevel! equ 0 (
        set "VENV_PATH=%PROJECT_ROOT%\venv"
        echo [SUCCESS] Virtual environment created successfully!
    ) else (
        echo [ERROR] Failed to create virtual environment!
        exit /b 1
    )
)

:activate_venv
echo [INFO] Activating virtual environment...
call "%VENV_PATH%\Scripts\activate.bat"
if !errorlevel! equ 0 (
    echo [SUCCESS] Virtual environment activated: !VENV_PATH!
    exit /b 0
) else (
    echo [ERROR] Failed to activate virtual environment!
    exit /b 1
)

:install_deps
REM Install dependencies
set "PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple"
set "PIP_TRUSTED_HOST=pypi.tuna.tsinghua.edu.cn"

echo [INFO] Upgrading pip...
python -m pip install --upgrade pip -i %PIP_INDEX_URL% --trusted-host %PIP_TRUSTED_HOST% >nul 2>&1
if !errorlevel! neq 0 (
    echo [WARNING] Failed to upgrade pip with mirror, trying default...
    python -m pip install --upgrade pip >nul 2>&1
)

REM Install main requirements
if exist "%BASE_PATH%\requirements.txt" (
    echo [INFO] Installing main project dependencies...
    python -m pip install -r "%BASE_PATH%\requirements.txt" -i %PIP_INDEX_URL% --trusted-host %PIP_TRUSTED_HOST%
    if !errorlevel! neq 0 (
        echo [WARNING] Failed with mirror, trying default source...
        python -m pip install -r "%BASE_PATH%\requirements.txt"
    )
) else (
    echo [WARNING] Main requirements file not found!
)

REM Install Web UI requirements
if exist "%BASE_PATH%\Web_Ui\requirements.txt" (
    echo [INFO] Installing Web UI dependencies...
    python -m pip install -r "%BASE_PATH%\Web_Ui\requirements.txt" -i %PIP_INDEX_URL% --trusted-host %PIP_TRUSTED_HOST%
    if !errorlevel! neq 0 (
        echo [WARNING] Failed with mirror, trying default source...
        python -m pip install -r "%BASE_PATH%\Web_Ui\requirements.txt"
        if !errorlevel! neq 0 (
            echo [ERROR] Failed to install Web UI dependencies!
            exit /b 1
        )
    )
) else (
    echo [ERROR] Web UI requirements file not found!
    exit /b 1
)

echo [SUCCESS] Dependencies installed successfully!
exit /b 0

:start_server
REM Start Web UI server
cd /d "%BASE_PATH%\Web_Ui"
if !errorlevel! neq 0 (
    echo [ERROR] Failed to change to Web UI directory!
    exit /b 1
)

if not exist "app.py" (
    echo [ERROR] app.py not found in Web UI directory!
    echo Directory: !cd!
    exit /b 1
)

echo [INFO] Starting Web UI server...
echo [INFO] Server will be available at: http://localhost:8000
echo [INFO] Your browser should open automatically.
echo.
echo Press Ctrl+C to stop the server when you're done.
echo.
echo =====================================
echo      Starting Web UI Server
echo =====================================
echo.

REM Open browser
start "" http://localhost:8000

REM Start the server
echo [INFO] Starting python app.py...
python app.py
if !errorlevel! neq 0 (
    echo [ERROR] Web UI server crashed or was stopped with errors!
    exit /b 1
)

exit /b 0