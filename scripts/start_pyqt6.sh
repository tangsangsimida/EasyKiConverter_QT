#!/bin/bash
# EasyKiConverter PyQt6 UI 启动脚本

# 激活虚拟环境
if [ -d "even/bin" ]; then
    source even/bin/activate
elif [ -d "even/Scripts" ]; then
    source even/Scripts/activate
else
    echo "警告: 未找到虚拟环境目录"
fi

# 设置Python路径
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"

# 启动PyQt6 UI
echo "启动 EasyKiConverter PyQt6 UI..."
python -m src.ui.pyqt6.main "$@"