#!/usr/bin/env python3
# 简化的PyInstaller打包命令

import subprocess
import sys

def main():
    print("EasyKiConverter PyQt6 UI 快速打包")
    print("====================================")
    
    # 基本打包命令
    cmd = [
        sys.executable, '-m', 'PyInstaller',
        'PyQt6_UI/main.py',
        '--name=EasyKiConverter-PyQt6',
        '--onefile',
        '--windowed',
        '--clean',
        '--noconfirm',
        '--add-data=EasyKiConverter:EasyKiConverter',
        '--hidden-import=PyQt6.QtCore',
        '--hidden-import=PyQt6.QtWidgets', 
        '--hidden-import=PyQt6.QtGui',
        '--hidden-import=pandas',
        '--hidden-import=openpyxl',
        '--hidden-import=requests',
        '--hidden-import=pydantic',
    ]
    
    print(f"执行命令: {' '.join(cmd)}")
    print("开始打包...")
    
    try:
        subprocess.run(cmd, check=True)
        print("✅ 打包完成！")
        print("可执行文件位置: dist/EasyKiConverter-PyQt6")
    except subprocess.CalledProcessError as e:
        print(f"❌ 打包失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
