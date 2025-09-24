#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EasyKiConverter 系统标题栏验证测试
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
current_dir = Path(__file__).parent
project_root = current_dir
sys.path.insert(0, str(project_root))

try:
    from PyQt6.QtWidgets import QApplication, QMessageBox
    from PyQt6.QtCore import Qt, QTimer
    from PyQt6.QtGui import QIcon
except ImportError as e:
    print(f"错误: 缺少PyQt6依赖 - {e}")
    sys.exit(1)

from src.ui.pyqt6.ultimate_main_window import UltimateMainWindow
from src.ui.pyqt6.utils.config_manager import ConfigManager


def test_system_title_bar():
    """测试系统标题栏功能"""
    print("🧪 开始系统标题栏功能测试...")
    
    app = QApplication(sys.argv)
    app.setApplicationName("EasyKiConverter")
    app.setApplicationVersion("2.0.0")
    app.setOrganizationName("EasyKiConverter")
    app.setStyle("Fusion")
    
    try:
        config_manager = ConfigManager()
        main_window = UltimateMainWindow(config_manager)
        
        # 测试1: 验证窗口属性
        print("\n1️⃣ 验证窗口属性:")
        print(f"   窗口标题: {main_window.windowTitle()}")
        print(f"   最小尺寸: {main_window.minimumSize().width()}×{main_window.minimumSize().height()}")
        print(f"   当前尺寸: {main_window.size().width()}×{main_window.size().height()}")
        
        # 测试2: 验证窗口标志
        print("\n2️⃣ 验证窗口标志:")
        window_flags = main_window.windowFlags()
        print(f"   窗口标志: {window_flags}")
        print(f"   是否无边框: {bool(window_flags & Qt.WindowType.FramelessWindowHint)}")
        print(f"   是否标准窗口: {bool(window_flags & Qt.WindowType.Window)}")
        
        # 测试3: 验证系统标题栏存在
        print("\n3️⃣ 验证系统标题栏:")
        window_handle = main_window.windowHandle()
        if window_handle:
            print("   ✅ 窗口句柄存在")
            print(f"   窗口状态: {window_handle.windowStates()}")
        else:
            print("   ❌ 窗口句柄不存在")
        
        # 测试4: 验证UI组件
        print("\n4️⃣ 验证UI组件:")
        print(f"   中央部件: {type(main_window.centralWidget()).__name__}")
        print(f"   状态栏: {type(main_window.statusBar()).__name__ if main_window.statusBar() else '无'}")
        
        # 显示窗口进行视觉验证
        main_window.show()
        print("\n✅ 窗口显示成功，请检查:")
        print("   • 系统标题栏是否正常显示")
        print("   • 最小化/最大化/关闭按钮是否可用")
        print("   • 窗口是否可以拖动")
        print("   • 界面布局是否合理")
        
        # 5秒后自动关闭
        print("\n⏰ 窗口将在5秒后自动关闭...")
        QTimer.singleShot(5000, main_window.close)
        
        return app.exec()
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    print("🧪 EasyKiConverter 系统标题栏验证测试")
    print("=" * 60)
    result = test_system_title_bar()
    sys.exit(result)