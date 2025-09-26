@echo off
REM EasyKiConverter Windows Build Script

echo EasyKiConverter Windows Build Script
echo ====================================

echo.
echo Current directory: %CD%

REM Detect project root directory
set PROJECT_ROOT=
if exist "..\venv\Scripts\activate.bat" (
    echo Found project root at ..
    set PROJECT_ROOT=..
) else if exist "..\..\venv\Scripts\activate.bat" (
    echo Found project root at ..\..
    set PROJECT_ROOT=..\..
) else if exist "..\..\..\venv\Scripts\activate.bat" (
    echo Found project root at ..\..\..
    set PROJECT_ROOT=..\..\..
) else (
    echo Warning: Cannot find project root directory with venv
    echo Assuming current directory is the project root
    set PROJECT_ROOT=.
)

REM Check for virtual environment
set VENV_FOUND=0
set VENV_PATH=
if not "%PROJECT_ROOT%"=="" (
    if exist "%PROJECT_ROOT%\venv\Scripts\activate.bat" (
        echo Found virtual environment at %PROJECT_ROOT%\venv
        set VENV_FOUND=1
        set VENV_PATH=%PROJECT_ROOT%\venv
    ) else (
        echo Warning: Cannot find virtual environment at %PROJECT_ROOT%\venv
        echo Assuming you have already activated the correct virtual environment
        echo or that PyInstaller is available in your PATH
    )
)

REM Activate virtual environment if found
if %VENV_FOUND%==1 (
    echo Activating virtual environment from %VENV_PATH%...
    call %VENV_PATH%\Scripts\activate.bat
    if errorlevel 1 (
        echo Error: Failed to activate virtual environment
        exit /b 1
    )
    echo Virtual environment activated
)

REM Check if pyinstaller is available
echo.
echo Checking for PyInstaller...
pyinstaller --version >nul 2>&1
if errorlevel 1 (
    echo Error: PyInstaller not found
    echo Please make sure PyInstaller is installed in your virtual environment
    echo or that you have activated the correct virtual environment
    exit /b 1
)
echo PyInstaller version: 
pyinstaller --version

REM Clean previous build files
echo.
echo Cleaning previous build files...
rmdir /s /q build dist 2>nul

REM Build application with PyInstaller
echo.
echo Building application...
pyinstaller --clean build_windows.spec
if errorlevel 1 (
    echo Error: PyInstaller build failed
    exit /b 1
)

REM Build complete
echo.
echo Build complete! Executable located in dist\ directory
echo.
echo To run the application:
echo   cd dist
echo   EasyKiConverter.exe