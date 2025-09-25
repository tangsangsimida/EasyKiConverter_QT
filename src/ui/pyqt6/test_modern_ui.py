#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
现代化界面测试脚本
使用项目根目录的even虚拟环境
"""

import sys
import os
from pathlib import Path

# 激活虚拟环境
venv_path = Path(__file__).parent.parent.parent.parent / "even"
if venv_path.exists():
    # 添加虚拟环境的site-packages到Python路径
    if os.name == 'nt':  # Windows
        site_packages = venv_path / "Lib" / "site-packages"
    else:  # Linux/Mac
        site_packages = venv_path / "lib" / f"python{sys.version_info.major}.{sys.version_info.minor}" / "site-packages"
    
    if site_packages.exists():
        sys.path.insert(0, str(site_packages))
        print(f"✅ 已激活虚拟环境: {venv_path}")
    else:
        print(f"⚠️  虚拟环境site-packages未找到: {site_packages}")
else:
    print(f"⚠️  虚拟环境未找到: {venv_path}")

# 确保可以导入同级模块
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))
sys.path.insert(0, str(current_dir.parent))
sys.path.insert(0, str(current_dir.parent.parent))

import traceback
from PyQt6.QtWidgets import QApplication
from modern_main_window import ModernMainWindow
from utils.config_manager import ConfigManager

def main():
    """主函数"""
    print("🚀 正在启动 EasyKiConverter 现代化UI...")
    
    # 创建QApplication实例
    app = QApplication(sys.argv)
    print("✅ QApplication 创建成功")
    
    # 设置应用程序属性
    app.setApplicationName("EasyKiConverter")
    app.setApplicationVersion("3.0.0")
    app.setOrganizationName("EasyKiConverter")
    app.setOrganizationDomain("easykiconverter.com")
    
    # 设置应用程序样式
    app.setStyle("Fusion")
    print("✅ 应用程序属性设置完成")
    
    try:
        # 初始化配置管理器
        print("📋 正在初始化配置管理器...")
        config_manager = ConfigManager()
        print("✅ 配置管理器初始化成功")
        
        # 创建并显示主窗口（使用现代化界面）
        print("🏗️ 正在创建现代化主窗口...")
        main_window = ModernMainWindow(config_manager)
        print("✅ 现代化主窗口创建成功")
        
        main_window.show()
        print("🎉 应用程序启动成功！")
        
        # 运行应用程序事件循环
        return app.exec()
        
    except Exception as e:
        print(f"❌ 应用程序启动失败: {e}")
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())