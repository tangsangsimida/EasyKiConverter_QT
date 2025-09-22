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

REM 设置函数：查找Python可执行文件
REM Set up function: Find Python executable
call :find_python_executable

REM 检查Python环境
REM Check Python environment
echo Checking Python environment...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo Python not found in system PATH. Checking for project-specific Python...
    call :check_and_setup_project_python
) else (
    echo System Python found.
    set "PYTHON_EXEC=python"
)

REM 设置虚拟环境Python
REM Set up virtual environment Python
if "%PYTHON_EXEC%"=="python" (
    set "PYTHON_FOR_VENV=python"
) else (
    set "PYTHON_FOR_VENV=%PYTHON_EXEC%"
)

REM 检查Python版本
REM Check Python version
call :check_python_version

REM 检查虚拟环境
REM Check virtual environment
call :setup_virtual_environment

REM 设置pip镜像并安装依赖
REM Set up pip mirror and install dependencies
call :install_dependencies

REM 启动Web UI服务器
REM Start Web UI server
call :start_web_ui

REM 清理并退出
REM Cleanup and exit
echo.
echo Server stopped. Deactivating virtual environment...
deactivate
echo.
echo Virtual environment deactivated.
echo Thank you for using EasyKiConverter!
echo.
pause
exit /b

REM =============================================================================
REM 函数定义区域
REM Function definitions
REM =============================================================================

:find_python_executable
REM 查找项目特定的Python可执行文件
REM Find project-specific Python executable
set "PYTHON_EXEC="
for %%p in (python.exe python3.13.exe python3.12.exe python3.11.exe python3.10.exe python3.9.exe python3.exe) do (
    if exist "%project_root%python\%%p" (
        set "PYTHON_EXEC=%project_root%python\%%p"
        set "PATH=%project_root%python;%PATH%"
        goto :eof
    )
)
goto :eof

:check_and_setup_project_python
REM 检查项目特定Python并设置
REM Check project-specific Python and setup
call :find_python_executable

if defined PYTHON_EXEC (
    REM 验证项目特定Python是否工作
    REM Verify project-specific Python is working
    "%PYTHON_EXEC%" --version >nul 2>&1
    if errorlevel 1 (
        echo Project-specific Python is corrupted or not working.
        echo.
        echo Downloading Python...
        echo This Python will be used only for this project and will not affect your system Python.
        echo.
        call :download_and_install_python
    )
) else (
    echo.
    echo No project-specific Python found.
    echo This script will attempt to download and install Python automatically.
    echo.
    call :download_and_install_python
)
goto :eof

:download_and_install_python
REM 下载并安装Python
REM Download and install Python

REM 创建python目录（如果不存在）
REM Create python directory if it doesn't exist
if not exist "%project_root%python" mkdir "%project_root%python"

REM 尝试使用curl下载Python
REM Try to download Python using curl first
echo Downloading Python 3.13.7 using curl...
curl -L -O https://mirrors.ustc.edu.cn/python/3.13.7/python-3.13.7-amd64.zip

if errorlevel 1 (
    echo.
    echo ERROR: Failed to download Python using curl.
    echo Trying alternative download method...
    echo.
    call :download_python_alternative
) else (
    echo Extracting Python...
    REM 解压zip文件到python目录
    REM Extract the zip file to python directory
    powershell -Command "Expand-Archive -Path 'python-3.13.7-amd64.zip' -DestinationPath '%project_root%python' -Force"
    
    if errorlevel 1 (
        echo.
        echo ERROR: Failed to extract Python.
        echo.
        pause
        exit /b 1
    )
    
    REM 清理zip文件
    REM Clean up zip file
    del "python-3.13.7-amd64.zip"
    
    echo Python extracted successfully in project directory!
    set "PYTHON_EXEC=%project_root%python\python.exe"
)

REM 验证Python安装
REM Verify Python installation
call :verify_python_installation
goto :eof

:download_python_alternative
REM 替代下载方法
REM Alternative download methods

REM 使用powershell下载
REM Alternative download method using powershell
echo Downloading Python 3.13.7 from official source...
powershell -Command "try { Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.13.7/python-3.13.7-amd64.exe' -OutFile '%project_root%python\python-installer.exe' -ErrorAction Stop } catch { exit 1 }"

if errorlevel 1 (
    echo.
    echo ERROR: Failed to download Python from official source.
    echo Trying alternative download method...
    echo.
    
    REM 使用bitsadmin下载
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

REM 清理安装程序
REM Clean up installer
del "%project_root%python\python-installer.exe"

echo Python installed successfully in project directory!
set "PYTHON_EXEC=%project_root%python\python.exe"
goto :eof

:verify_python_installation
REM 验证Python安装
REM Verify Python installation
set "PYTHON_FOUND="
for %%p in (python.exe python3.13.exe python3.12.exe python3.11.exe python3.10.exe python3.9.exe python3.exe) do (
    if exist "%project_root%python\%%p" (
        set "PYTHON_FOUND=1"
        goto :verify_python_found
    )
)

:verify_python_found
if not defined PYTHON_FOUND (
    echo.
    echo ERROR: Python installation failed. No valid Python executable found.
    echo.
    pause
    exit /b 1
)
goto :eof

:check_python_version
REM 检查Python版本
REM Check Python version
for /f "tokens=2" %%i in ('%PYTHON_EXEC% --version 2^>^&1') do set python_version=%%i
echo Python %python_version% detected successfully

REM 检查Python版本（基本检查3.x）
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
goto :eof

:setup_virtual_environment
REM 设置虚拟环境
REM Setup virtual environment
echo Checking for virtual environment...

REM 检查现有的虚拟环境
REM Check for existing virtual environments
set "venv_path="
for %%v in (venv .venv env) do (
    if exist "%project_root%%%v\Scripts\activate.bat" (
        set "venv_path=%project_root%%%v"
        echo Found virtual environment: %%v
        goto :activate_venv
    )
)

echo No project virtual environment found. Creating new virtual environment...

REM 使用适当的Python创建虚拟环境
REM Use the appropriate Python to create virtual environment
"%PYTHON_FOR_VENV%" -m venv "%project_root%venv"
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment.
    echo Please ensure you have the venv module installed.
    pause
    exit /b 1
)
set "venv_path=%project_root%venv"
echo Project virtual environment created successfully: venv

:activate_venv
REM 激活虚拟环境
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
goto :eof

:install_dependencies
REM 安装依赖项
REM Install dependencies

REM 设置pip镜像以加快在中国的下载速度
REM Set up pip mirror for faster downloads in China
echo Setting up pip configuration for faster downloads...
set "PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple"
set "PIP_TRUSTED_HOST=pypi.tuna.tsinghua.edu.cn"

REM 在虚拟环境中升级pip
REM Upgrade pip in virtual environment
echo Upgrading pip using Tsinghua mirror...
python -m pip install --upgrade pip -i %PIP_INDEX_URL% --trusted-host %PIP_TRUSTED_HOST% >nul 2>&1
if errorlevel 1 (
    echo Failed to upgrade pip using mirror, trying default source...
    python -m pip install --upgrade pip >nul 2>&1
)

echo Installing dependencies using domestic mirror for faster speed...
echo.

REM 安装主要依赖项（如果存在）
REM Install main requirements if exists
if exist "%base_path%\requirements.txt" (
    echo Installing main project dependencies...
    python -m pip install -r "%base_path%\requirements.txt" -i %PIP_INDEX_URL% --trusted-host %PIP_TRUSTED_HOST%
    if errorlevel 1 (
        echo Some main dependencies failed with mirror, trying default source...
        python -m pip install -r "%base_path%\requirements.txt"
        if errorlevel 1 (
            echo WARNING: Some main dependencies failed to install.
        )
    )
    echo Main dependencies installed successfully!
) else (
    echo WARNING: Main requirements file not found, skipping.
)

REM 安装Web UI依赖项
REM Install Web UI requirements
echo.
echo Installing Web UI dependencies...
python -m pip install -r "%base_path%\Web_Ui\requirements.txt" -i %PIP_INDEX_URL% --trusted-host %PIP_TRUSTED_HOST%
if errorlevel 1 (
    echo Failed with mirror, trying default source...
    python -m pip install -r "%base_path%\Web_Ui\requirements.txt"
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
goto :eof

:start_web_ui
REM 启动Web UI
REM Start Web UI
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

REM 切换到Web UI目录并启动服务器
REM Change to the Web UI directory and start the server
cd /d "%base_path%\Web_Ui"

REM 如果存在项目Python，添加到PATH
REM Add project Python to PATH if it exists
REM 启动服务器并打开浏览器
REM Start server and open browser
start "" http://localhost:8000
python app.py

goto :eof