#!/bin/bash
# EasyKiConverter PyQt6 UI 启动脚本 (Linux/macOS)

echo "==================================="
echo "  EasyKiConverter PyQt6 UI"
echo "==================================="
echo ""

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# 检查是否存在 @even 虚拟环境
if [ -d "$PROJECT_ROOT/@even" ]; then
    echo "检测到 @even 虚拟环境，正在激活..."
    source "$PROJECT_ROOT/@even/bin/activate"
    echo "✅ 虚拟环境已激活"
else
    echo "⚠️  未找到 @even 虚拟环境，将使用系统Python环境"
fi

# 检查Python版本
echo "检查Python版本..."
python_version=$(python3 --version 2>&1)
echo "当前Python版本: $python_version"

# 检查PyQt6是否已安装
echo "检查PyQt6依赖..."
if python3 -c "import PyQt6" 2>/dev/null; then
    echo "✅ PyQt6 已安装"
else
    echo "❌ PyQt6 未安装，正在安装..."
    pip install PyQt6>=6.4.0 PyQt6-Qt6>=6.4.0
    if [ $? -ne 0 ]; then
        echo "❌ PyQt6 安装失败，请手动安装"
        exit 1
    fi
    echo "✅ PyQt6 安装完成"
fi

# 检查其他依赖
echo "检查其他依赖..."
dependencies=("requests" "pandas" "openpyxl")
for dep in "${dependencies[@]}"; do
    if python3 -c "import $dep" 2>/dev/null; then
        echo "✅ $dep 已安装"
    else
        echo "📦 安装 $dep..."
        pip install "$dep"
    fi
done

# 设置Python路径
cd "$PROJECT_ROOT/PyQt6_UI"

# 启动PyQt6 UI
echo ""
echo "正在启动 EasyKiConverter PyQt6 UI..."
echo ""

# 使用 @even 虚拟环境中的Python解释器
if [ -d "$PROJECT_ROOT/@even" ]; then
    "$PROJECT_ROOT/@even/bin/python3" main.py
else
    python3 main.py
fi

# 检查退出状态
if [ $? -eq 0 ]; then
    echo "✅ EasyKiConverter PyQt6 UI 正常退出"
else
    echo "❌ EasyKiConverter PyQt6 UI 异常退出"
fi

# 如果激活了虚拟环境，退出时停用
if [ -n "$VIRTUAL_ENV" ]; then
    deactivate
fi

echo ""
echo "感谢使用 EasyKiConverter！"
echo "==================================="