#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EasyKiConverter 最大化功能详细诊断测试
"""

import sys
import os
from pathlib import Path
import time

# 添加项目根目录到Python路径
current_dir = Path(__file__).parent
project_root = current_dir
sys.path.insert(0, str(project_root))

try:
    from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
    from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QSize
    from PyQt6.QtGui import QIcon
except ImportError as e:
    print(f"错误: 缺少PyQt6依赖 - {e}")
    sys.exit(1)

from src.ui.pyqt6.ultimate_main_window import UltimateMainWindow
from src.ui.pyqt6.utils.config_manager import ConfigManager


class MaximizeTestWindow(UltimateMainWindow):
    """测试窗口，用于详细诊断最大化功能"""
    
    def __init__(self, config_manager, parent=None):
        super().__init__(config_manager, parent)
        self.setup_test_controls()
        self.installEventFilter(self)
        
    def setup_test_controls(self):
        """设置测试控制面板"""
        # 创建测试控制面板
        test_panel = QWidget()
        test_layout = QVBoxLayout(test_panel)
        
        # 窗口状态显示
        self.status_label = QLabel("窗口状态监控")
        self.status_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        test_layout.addWidget(self.status_label)
        
        # 最大化测试按钮
        self.test_max_btn = QPushButton("测试最大化 (自定义)")
        self.test_max_btn.clicked.connect(self.test_maximize_custom)
        test_layout.addWidget(self.test_max_btn)
        
        # 系统最大化测试按钮
        self.sys_max_btn = QPushButton("测试最大化 (系统)")
        self.sys_max_btn.clicked.connect(self.test_maximize_system)
        test_layout.addWidget(self.sys_max_btn)
        
        # 状态检测按钮
        self.check_status_btn = QPushButton("检测窗口状态")
        self.check_status_btn.clicked.connect(self.check_window_status)
        test_layout.addWidget(self.check_status_btn)
        
        # 几何信息按钮
        self.geom_btn = QPushButton("显示几何信息")
        self.geom_btn.clicked.connect(self.show_geometry_info)
        test_layout.addWidget(self.geom_btn)
        
        # 窗口标志按钮
        self.flags_btn = QPushButton("显示窗口标志")
        self.flags_btn.clicked.connect(self.show_window_flags)
        test_layout.addWidget(self.flags_btn)
        
        # 将测试面板添加到主窗口
        self.statusBar().addPermanentWidget(test_panel)
        
    def test_maximize_custom(self):
        """测试自定义最大化逻辑"""
        print("\n🔍 测试自定义最大化逻辑")
        print(f"   当前最大化状态: {self.isMaximized()}")
        print(f"   当前窗口几何: {self.geometry()}")
        print(f"   当前屏幕几何: {self.screen().geometry()}")
        
        try:
            if self.isMaximized():
                print("   执行 showNormal()")
                self.showNormal()
            else:
                print("   执行 showMaximized()")
                self.showMaximized()
            
            # 延迟检查状态
            QTimer.singleShot(100, self.check_window_status)
            
        except Exception as e:
            print(f"   ❌ 最大化操作异常: {e}")
            import traceback
            traceback.print_exc()
    
    def test_maximize_system(self):
        """测试系统级别的最大化"""
        print("\n🔍 测试系统级别最大化")
        
        try:
            # 获取窗口句柄
            window_handle = self.windowHandle()
            if window_handle:
                print("   ✅ 窗口句柄存在")
                print(f"   窗口状态: {window_handle.windowStates()}")
                
                # 尝试使用系统API
                if window_handle.windowStates() & Qt.WindowState.WindowMaximized:
                    print("   当前已最大化，尝试恢复正常")
                    window_handle.setWindowStates(Qt.WindowState.WindowNoState)
                else:
                    print("   当前未最大化，尝试最大化")
                    window_handle.setWindowStates(Qt.WindowState.WindowMaximized)
            else:
                print("   ❌ 窗口句柄不存在")
                
        except Exception as e:
            print(f"   ❌ 系统最大化异常: {e}")
            import traceback
            traceback.print_exc()
    
    def check_window_status(self):
        """检查窗口状态"""
        print("\n📊 窗口状态检测:")
        print(f"   isMaximized(): {self.isMaximized()}")
        print(f"   isMinimized(): {self.isMinimized()}")
        print(f"   isFullScreen(): {self.isFullScreen()}")
        print(f"   isVisible(): {self.isVisible()}")
        print(f"   isActiveWindow(): {self.isActiveWindow()}")
        
        window_handle = self.windowHandle()
        if window_handle:
            states = window_handle.windowStates()
            print(f"   窗口句柄状态: {states}")
            print(f"   是否最大化: {bool(states & Qt.WindowState.WindowMaximized)}")
            print(f"   是否最小化: {bool(states & Qt.WindowState.WindowMinimized)}")
            print(f"   是否全屏: {bool(states & Qt.WindowState.WindowFullScreen)}")
        
        self.update_status_display()
    
    def show_geometry_info(self):
        """显示几何信息"""
        print("\n📐 几何信息:")
        print(f"   窗口几何: {self.geometry()}")
        print(f"   窗口框架几何: {self.frameGeometry()}")
        print(f"   正常几何: {self.normalGeometry()}")
        print(f"   屏幕几何: {self.screen().geometry()}")
        print(f"   可用几何: {self.screen().availableGeometry()}")
    
    def show_window_flags(self):
        """显示窗口标志"""
        print("\n🏷️ 窗口标志:")
        flags = self.windowFlags()
        print(f"   原始标志值: {flags}")
        print(f"   FramelessWindowHint: {bool(flags & Qt.WindowType.FramelessWindowHint)}")
        print(f"   Window: {bool(flags & Qt.WindowType.Window)}")
        print(f"   Dialog: {bool(flags & Qt.WindowType.Dialog)}")
        print(f"   WindowSystemMenuHint: {bool(flags & Qt.WindowType.WindowSystemMenuHint)}")
        print(f"   WindowMinimizeButtonHint: {bool(flags & Qt.WindowType.WindowMinimizeButtonHint)}")
        print(f"   WindowMaximizeButtonHint: {bool(flags & Qt.WindowType.WindowMaximizeButtonHint)}")
        print(f"   WindowCloseButtonHint: {bool(flags & Qt.WindowType.WindowCloseButtonHint)}")
    
    def update_status_display(self):
        """更新状态显示"""
        status_text = f"状态: {'最大化' if self.isMaximized() else '正常'} | "
        status_text += f"几何: {self.width()}×{self.height()}"
        self.status_label.setText(status_text)
    
    def eventFilter(self, obj, event):
        """事件过滤器，监控窗口状态变化"""
        if event.type() == event.Type.WindowStateChange:
            print(f"\n🔄 窗口状态变化事件: {event}")
            self.check_window_status()
        elif event.type() == event.Type.Resize:
            print(f"\n📏 窗口大小变化: {self.size()}")
        elif event.type() == event.Type.Move:
            print(f"\n📍 窗口位置变化: {self.pos()}")
        
        return super().eventFilter(obj, event)
    
    def resizeEvent(self, event):
        """重写resize事件"""
        print(f"\n📐 Resize事件: {event.size()}")
        super().resizeEvent(event)
        self.update_status_display()
    
    def moveEvent(self, event):
        """重写move事件"""
        print(f"\n📍 Move事件: {event.pos()}")
        super().moveEvent(event)


def main():
    """主函数"""
    print("🧪 EasyKiConverter 最大化功能详细诊断测试")
    print("=" * 60)
    
    app = QApplication(sys.argv)
    app.setApplicationName("EasyKiConverter")
    app.setApplicationVersion("2.0.0")
    app.setOrganizationName("EasyKiConverter")
    app.setStyle("Fusion")
    
    try:
        config_manager = ConfigManager()
        test_window = MaximizeTestWindow(config_manager)
        
        print("\n🔍 初始状态检测:")
        test_window.check_window_status()
        test_window.show_geometry_info()
        test_window.show_window_flags()
        
        print("\n✅ 测试窗口已创建，请进行以下测试:")
        print("   1. 点击系统标题栏的最大化按钮")
        print("   2. 使用测试面板中的按钮进行测试")
        print("   3. 观察控制台输出的详细信息")
        print("   4. 检查窗口行为是否符合预期")
        
        test_window.show()
        test_window.update_status_display()
        
        return app.exec()
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())