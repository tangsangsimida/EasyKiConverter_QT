#!/bin/bash
# EasyKiConverter Linux 打包脚本

# 进入项目根目录
cd ..

# 激活虚拟环境
source even/bin/activate

# 回到output目录
cd output

# 清理之前的构建文件
echo "清理之前的构建文件..."
rm -rf build dist

# 使用PyInstaller打包应用
echo "开始打包应用..."
pyinstaller --clean --log-level=DEBUG build.spec

# 打包完成后，可执行文件位于 dist/ 目录中
echo "打包完成！可执行文件位于 dist/ 目录中"