# EasyKiConverter 打包脚本

import os
import sys
import subprocess
import platform
from pathlib import Path

def get_pyinstaller_path():
    """获取PyInstaller路径"""
    # 检查虚拟环境中是否有PyInstaller
    venv_pyinstaller = Path("venv/bin/pyinstaller")
    if venv_pyinstaller.exists():
        return str(venv_pyinstaller)
    
    # 检查系统中是否有PyInstaller
    try:
        subprocess.run(["pyinstaller", "--version"], capture_output=True, check=True)
        return "pyinstaller"
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None

def build_for_platform(platform_name):
    """为指定平台打包"""
    print(f"正在为 {platform_name} 平台打包...")
    
    # 获取PyInstaller路径
    pyinstaller_path = get_pyinstaller_path()
    if not pyinstaller_path:
        print("错误: 未找到PyInstaller，请先安装PyInstaller")
        return False
    
    # 构建命令
    cmd = [
        pyinstaller_path,
        "--name", "EasyKiConverter",
        "--onefile",
        "--noconsole",
        "--clean",
        "--distpath", f"dist/{platform_name}",
        "--workpath", f"build/{platform_name}",
        "--specpath", f"build/{platform_name}",
        "--hidden-import", "PyQt6.QtCore",
        "--hidden-import", "PyQt6.QtGui",
        "--hidden-import", "PyQt6.QtWidgets",
        "--hidden-import", "PyQt6.QtNetwork",
        "--hidden-import", "pandas",
        "--hidden-import", "openpyxl",
        "--hidden-import", "requests",
        "--hidden-import", "pydantic",
        "--hidden-import", "pydantic_core",
        "--hidden-import", "numpy",
        "--hidden-import", "certifi",
        "--hidden-import", "urllib3",
        "--hidden-import", "charset_normalizer",
        "--hidden-import", "idna",
        "--hidden-import", "python_dateutil",
        "--hidden-import", "pytz",
        "--hidden-import", "tzdata",
        "--hidden-import", "et_xmlfile",
        "--hidden-import", "six",
        "--hidden-import", "annotated_types",
        "--hidden-import", "typing_extensions",
        "--hidden-import", "typing_inspection",
        "--exclude-module", "tkinter",
        "--exclude-module", "matplotlib",
        "--exclude-module", "scipy",
        "--exclude-module", "jinja2",
        "--exclude-module", "werkzeug",
        "--exclude-module", "blinker",
        "--exclude-module", "click",
        "--exclude-module", "markupsafe",
        "--exclude-module", "numpy.random._pickle",
        "--add-data", "src/ui/pyqt6/resources;resources" if platform_name == "windows" else "src/ui/pyqt6/resources:resources",
        "src/ui/pyqt6/main.py"
    ]
    
    # 添加平台特定的参数
    if platform_name == "windows":
        # Windows特定参数
        cmd.extend([
            "--windowed",
            "--icon", "src/ui/pyqt6/resources/icon.ico"
        ])
    elif platform_name == "darwin":
        # macOS特定参数
        cmd.extend([
            "--windowed",
            "--osx-bundle-identifier", "com.easykiconverter.app"
        ])
    
    print(f"执行命令: {' '.join(cmd)}")
    
    try:
        # 创建输出目录
        Path(f"dist/{platform_name}").mkdir(parents=True, exist_ok=True)
        Path(f"build/{platform_name}").mkdir(parents=True, exist_ok=True)
        
        # 执行打包命令
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ {platform_name} 平台打包成功!")
            print(f"可执行文件位置: dist/{platform_name}/EasyKiConverter{'exe' if platform_name == 'windows' else ''}")
            return True
        else:
            print(f"❌ {platform_name} 平台打包失败!")
            print(f"错误信息: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ 执行打包命令时发生错误: {e}")
        return False

def main():
    """主函数"""
    print(" EasyKiConverter 跨平台打包工具 ")
    print("=" * 50)
    
    # 获取当前系统平台
    current_platform = platform.system().lower()
    
    # 映射平台名称
    platform_map = {
        "windows": "windows",
        "linux": "linux",
        "darwin": "macos"
    }
    
    target_platform = platform_map.get(current_platform, "unknown")
    
    if target_platform == "unknown":
        print(f"不支持的平台: {current_platform}")
        return
    
    print(f"检测到当前平台: {target_platform}")
    
    # 为当前平台打包
    success = build_for_platform(target_platform)
    
    if success:
        print("\n 打包完成! ")
        print("=" * 50)
        print(f"可执行文件已生成到 dist/{target_platform}/ 目录")
    else:
        print("\n 打包失败! ")
        print("=" * 50)
        sys.exit(1)

if __name__ == "__main__":
    main()