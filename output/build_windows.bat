@echo off
REM EasyKiConverter Windows Build Script

REM Change to project root directory
cd ..

REM Activate virtual environment
call even\Scripts\activate.bat

REM Change back to output directory
cd output

REM Clean previous build files
echo Cleaning previous build files...
rmdir /s /q build dist 2>nul

REM Build application with PyInstaller
echo Building application...
pyinstaller --clean build_windows.spec

REM Build complete
echo Build complete! Executable located in dist\ directory