#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PyInstaller 打包配置文件生成器
用于创建EasyKiConverter PyQt6 UI的打包配置
"""

import os
import sys
import subprocess
from pathlib import Path

def create_pyinstaller_config():
    """创建PyInstaller配置文件"""
    
    # 创建打包脚本
    build_script = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EasyKiConverter PyQt6 UI 打包脚本
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_dependencies():
    """检查必要的依赖"""
    print("检查打包依赖...")
    
    required_packages = [
        'PyInstaller',
        'PyQt6',
        'pandas',
        'openpyxl',
        'requests',
        'pydantic'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.lower().replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ 缺少依赖包: {', '.join(missing_packages)}")
        print("正在安装缺失的依赖...")
        
        for package in missing_packages:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
        
        print("✅ 依赖安装完成")
    else:
        print("✅ 所有依赖都已安装")

def create_spec_file():
    """创建spec文件"""
    spec_content = """
# -*- mode: python ; coding: utf-8 -*-

import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

block_cipher = None

a = Analysis(
    ['PyQt6_UI/main.py'],
    pathex=[
        str(project_root),
        str(project_root / 'PyQt6_UI'),
    ],
    binaries=[],
    datas=[
        ('PyQt6_UI/utils/*.py', 'utils'),
        ('PyQt6_UI/widgets/*.py', 'widgets'),
        ('PyQt6_UI/workers/*.py', 'workers'),
        ('EasyKiConverter/*.py', 'EasyKiConverter'),
        ('EasyKiConverter/easyeda/*.py', 'easyeda'),
        ('EasyKiConverter/kicad/*.py', 'kicad'),
    ],
    hiddenimports=[
        'PyQt6.QtCore',
        'PyQt6.QtWidgets',
        'PyQt6.QtGui',
        'pandas',
        'openpyxl',
        'requests',
        'pydantic',
        'concurrent.futures',
        'threading',
        'pathlib',
        'json',
        'logging',
        're',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='EasyKiConverter-PyQt6',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)

# macOS app bundle
if sys.platform == 'darwin':
    app = BUNDLE(
        exe,
        name='EasyKiConverter-PyQt6.app',
        icon=None,
        bundle_identifier='com.easykiconverter.pyqt6',
        info_plist={
            'CFBundleName': 'EasyKiConverter PyQt6',
            'CFBundleDisplayName': 'EasyKiConverter PyQt6',
            'CFBundleShortVersionString': '1.0.0',
            'CFBundleVersion': '1.0.0',
            'CFBundleIdentifier': 'com.easykiconverter.pyqt6',
            'NSHighResolutionCapable': 'True',
        },
    )
"""
    
    with open('EasyKiConverter-PyQt6.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print("✅ spec文件已创建")

def build_executable():
    """构建可执行文件"""
    print("开始构建可执行文件...")
    
    try:
        # 使用PyInstaller构建
        cmd = [
            sys.executable, '-m', 'PyInstaller',
            'EasyKiConverter-PyQt6.spec',
            '--clean',
            '--noconfirm'
        ]
        
        print(f"执行命令: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ 构建成功！")
            
            # 显示输出文件位置
            dist_dir = Path('dist')
            if dist_dir.exists():
                print(f"\n📁 输出文件位置: {dist_dir.absolute()}")
                
                # 列出生成的文件
                print("\n生成的文件:")
                for item in dist_dir.iterdir():
                    if item.is_file():
                        size = item.stat().st_size / (1024 * 1024)  # MB
                        print(f"  📄 {item.name} ({size:.1f} MB)")
                    elif item.is_dir():
                        print(f"  📂 {item.name}/")
            
            return True
        else:
            print(f"❌ 构建失败:")
            print(f"错误输出: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ 构建过程中发生错误: {e}")
        return False

def clean_build_files():
    """清理构建文件"""
    print("清理构建文件...")
    
    build_dirs = ['build', '__pycache__']
    build_files = ['EasyKiConverter-PyQt6.spec']
    
    for dir_name in build_dirs:
        dir_path = Path(dir_name)
        if dir_path.exists():
            shutil.rmtree(dir_path)
            print(f"🗑️  删除目录: {dir_name}")
    
    for file_name in build_files:
        file_path = Path(file_name)
        if file_path.exists():
            file_path.unlink()
            print(f"🗑️  删除文件: {file_name}")

def main():
    """主函数"""
    print("===================================")
    print("  EasyKiConverter PyQt6 UI 打包工具")
    print("===================================")
    print()
    
    # 检查依赖
    check_dependencies()
    
    # 创建spec文件
    create_spec_file()
    
    # 询问是否清理之前的构建文件
    if Path('build').exists() or Path('dist').exists():
        response = input("是否清理之前的构建文件? (y/n): ").lower()
        if response == 'y':
            clean_build_files()
    
    # 构建可执行文件
    if build_executable():
        print("\n🎉 打包完成！")
        print("\n下一步:")
        print("1. 测试生成的可执行文件")
        print("2. 如果需要，可以添加图标文件")
        print("3. 创建安装程序（可选）")
    else:
        print("\n❌ 打包失败，请检查错误信息")
        sys.exit(1)

if __name__ == "__main__":
    main()
'''
    
    return build_script

def main():
    """创建PyInstaller配置文件"""
    
    # 创建打包脚本
    build_script = create_pyinstaller_build_script()
    
    with open('build_pyqt6_ui.py', 'w', encoding='utf-8') as f:
        f.write(build_script)
    
    print("✅ PyInstaller打包脚本已创建: build_pyqt6_ui.py")
    print("\n使用方法:")
    print("1. 确保已激活 @even 虚拟环境")
    print("2. 运行: python build_pyqt6_ui.py")
    print("3. 生成的可执行文件将在 dist/ 目录中")
    
    # 创建简化的打包命令脚本
    simple_build_script = '''#!/usr/bin/env python3
# 简化的PyInstaller打包命令

import subprocess
import sys
import os

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
    print("\n开始打包...")
    
    try:
        subprocess.run(cmd, check=True)
        print("\n✅ 打包完成！")
        print("可执行文件位置: dist/EasyKiConverter-PyQt6")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ 打包失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
'''
    
    with open('quick_build.py', 'w', encoding='utf-8') as f:
        f.write(simple_build_script)
    
    print("\n✅ 快速打包脚本已创建: quick_build.py")
    print("\n打包步骤:")
    print("1. 激活 @even 虚拟环境")
    print("2. 安装PyInstaller: pip install pyinstaller")
    print("3. 运行打包: python quick_build.py")
    print("4. 或使用完整脚本: python build_pyqt6_ui.py")

if __name__ == "__main__":
    main()