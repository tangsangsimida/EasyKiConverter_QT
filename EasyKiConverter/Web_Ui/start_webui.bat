@echo off
title EasyKiConverter Web UI
echo.
echo =====================================
echo   EasyKiConverter Web UI 启动器
echo =====================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: Python未安装或不在PATH中
    echo 请安装Python 3.7+ 并添加到系统PATH
    pause
    exit /b 1
)

REM 检查依赖
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo 正在安装依赖...
    pip install flask flask-cors
    if errorlevel 1 (
        echo 错误: 依赖安装失败
        pause
        exit /b 1
    )
)

echo.
echo 正在启动Web UI服务器...
echo.
echo 启动成功后，浏览器将自动打开 http://localhost:8000
echo 如果浏览器没有自动打开，请手动访问该地址
echo.
echo 按Ctrl+C停止服务器
echo.

REM 启动服务器并打开浏览器
start "" http://localhost:8000
python app.py

pause