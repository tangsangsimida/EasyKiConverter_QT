@echo off
REM EasyKiConverter Windows 打包脚本

REM 激活虚拟环境
call even\Scripts\activate.bat

REM 使用PyInstaller打包应用
pyinstaller --clean build.spec

REM 打包完成后，可执行文件位于 dist\ 目录中
echo 打包完成！可执行文件位于 dist\ 目录中