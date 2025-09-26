@echo off
REM EasyKiConverter Windows 打包脚本

REM 进入项目根目录
cd ..

REM 激活虚拟环境
call even\Scripts\activate.bat

REM 回到output目录
cd output

REM 清理之前的构建文件
echo 清理之前的构建文件...
rmdir /s /q build dist 2>nul

REM 使用PyInstaller打包应用
echo 开始打包应用...
pyinstaller --clean build_windows.spec

REM 打包完成后，可执行文件位于 dist\ 目录中
echo 打包完成！可执行文件位于 dist\ 目录中