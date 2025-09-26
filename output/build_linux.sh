#!/bin/bash
# EasyKiConverter Linux 打包脚本

# 激活虚拟环境
source even/bin/activate

# 使用PyInstaller打包应用
pyinstaller --clean build.spec

# 打包完成后，可执行文件位于 dist/ 目录中
echo "打包完成！可执行文件位于 dist/ 目录中"