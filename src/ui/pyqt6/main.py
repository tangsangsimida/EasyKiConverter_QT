#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EasyKiConverter PyQt6 UI - 主程序入口
基于PyQt6的桌面应用程序，用于将嘉立创EDA元器件转换为KiCad格式
"""
import sys
from pathlib import Path
# 确保可以导入同级模块
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import traceback
from PyQt6.QtWidgets import QApplication
from ultimate_main_window import UltimateMainWindow
from utils.config_manager import ConfigManager

def main():
    """主函数"""
    print("🚀 正在启动 EasyKiConverter PyQt6 UI...")
    
    # 创建QApplication实例
    app = QApplication(sys.argv)
    print("✅ QApplication 创建成功")
    
    # 设置应用程序属性（必须在创建QApplication后）
    app.setApplicationName("EasyKiConverter")
    app.setApplicationVersion("2.0.0")
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
        
        # 创建并显示主窗口（使用优化后的界面）
        print("🏗️ 正在创建主窗口...")
        main_window = UltimateMainWindow(config_manager)
        print("✅ 主窗口创建成功")
        
        main_window.show()

        
        # 运行应用程序事件循环
        return app.exec()
        
    except Exception as e:
        print(f"❌ 应用程序启动失败: {e}")
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())