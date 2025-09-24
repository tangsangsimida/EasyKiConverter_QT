#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EasyKiConverter PyQt6 UI - 主程序入口
基于PyQt6的桌面应用程序，用于将嘉立创EDA元器件转换为KiCad格式
"""

import sys
import os
from pathlib import Path

# 添加父目录到Python路径，确保可以导入EasyKiConverter模块
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.insert(0, str(parent_dir))

try:
    from PyQt6.QtWidgets import QApplication
    from PyQt6.QtCore import Qt
    from PyQt6.QtGui import QIcon
except ImportError as e:
    print(f"错误: 缺少PyQt6依赖 - {e}")
    print("请运行: pip install -r requirements.txt")
    sys.exit(1)

from main_window import MainWindow
from modern_main_window import ModernMainWindow
from optimized_main_window import OptimizedMainWindow
from utils.config_manager import ConfigManager


def main():
    """主函数"""
    # 创建QApplication实例
    app = QApplication(sys.argv)
    
    # 设置应用程序属性
    app.setApplicationName("EasyKiConverter")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("EasyKiConverter")
    app.setOrganizationDomain("easykiconverter.com")
    
    # 启用高DPI支持
    app.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    
    # 设置应用程序样式
    app.setStyle("Fusion")
    
    try:
        # 初始化配置管理器
        config_manager = ConfigManager()
        
        # 创建并显示主窗口（使用优化版现代化界面）
        main_window = OptimizedMainWindow(config_manager)
        main_window.show()
        
        # 运行应用程序事件循环
        return app.exec()
        
    except Exception as e:
        print(f"应用程序启动失败: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())