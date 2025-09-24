#!/bin/bash
# EasyKiConverter CLI 启动脚本

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

# 启动CLI
echo "启动 EasyKiConverter CLI..."
python -m src.cli.main "$@"