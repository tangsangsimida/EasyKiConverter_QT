#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
响应式布局管理器
根据窗口大小自动调整布局结构
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PyQt6.QtCore import Qt, QTimer 


class ResponsiveLayoutManager:
    """响应式布局管理器"""
    
    def __init__(self, parent_widget):
        self.parent_widget = parent_widget
        self.current_layout_mode = "desktop"  # desktop, tablet, mobile
        self.breakpoints = {
            'mobile': 1200,     # < 1200px 移动端（调整为更大的值）
            'tablet': 1600,     # 1200-1600px 平板端（调整为更大的值）
            'desktop': 1600     # > 1600px 桌面端（调整为更大的值）
        }
        self.resize_timer = QTimer()
        self.resize_timer.setSingleShot(True)
        self.resize_timer.timeout.connect(self.check_layout_mode)
        
    def on_resize(self):
        """窗口大小改变时的处理"""
        # 延迟处理，避免频繁重绘
        self.resize_timer.start(200)
        
    def check_layout_mode(self):
        """检查当前布局模式"""
        width = self.parent_widget.width()
        
        if width < self.breakpoints['mobile']:
            new_mode = "mobile"
        elif width < self.breakpoints['tablet']:
            new_mode = "tablet"
        else:
            new_mode = "desktop"
            
        if new_mode != self.current_layout_mode:
            self.current_layout_mode = new_mode
            self.apply_layout_mode(new_mode)
            
    def apply_layout_mode(self, mode):
        """应用指定布局模式"""
        if hasattr(self.parent_widget, 'apply_responsive_layout'):
            self.parent_widget.apply_responsive_layout(mode)
            
    def get_recommended_sizes(self, mode):
        """获取推荐尺寸"""
        sizes = {
            'desktop': {
                'sidebar_width': 300,      # 增加侧边栏宽度
                'side_panel_width': 350,   # 增加侧面板宽度
                'title_height': 80,        # 增加标题栏高度
                'status_height': 60,       # 增加状态栏高度
                'card_spacing': 35,        # 增加卡片间距
                'button_height': 65,       # 增加按钮高度
                'input_height': 60         # 增加输入框高度
            },
            'tablet': {
                'sidebar_width': 260,      # 调整平板侧边栏宽度
                'side_panel_width': 300,   # 调整平板侧面板宽度
                'title_height': 70,        # 调整平板标题栏高度
                'status_height': 50,       # 调整平板状态栏高度
                'card_spacing': 30,        # 调整平板卡片间距
                'button_height': 55,       # 调整平板按钮高度
                'input_height': 50         # 调整平板输入框高度
            },
            'mobile': {
                'sidebar_width': 0,        # 隐藏侧边栏
                'side_panel_width': 0,     # 隐藏侧面板
                'title_height': 60,        # 调整移动端标题栏高度
                'status_height': 45,       # 调整移动端状态栏高度
                'card_spacing': 25,        # 调整移动端卡片间距
                'button_height': 50,       # 调整移动端按钮高度
                'input_height': 45         # 调整移动端输入框高度
            }
        }
        return sizes.get(mode, sizes['desktop'])


class AdaptiveWidget(QWidget):
    """自适应组件基类"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.responsive_manager = ResponsiveLayoutManager(self)
        self.current_mode = "desktop"
        
    def resizeEvent(self, event):
        """重写大小改变事件"""
        super().resizeEvent(event)
        self.responsive_manager.on_resize()
        
    def apply_responsive_layout(self, mode):
        """应用响应式布局 - 子类重写此方法"""
        self.current_mode = mode
        sizes = self.responsive_manager.get_recommended_sizes(mode)
        self.update_layout_sizes(sizes)
        
    def update_layout_sizes(self, sizes):
        """更新布局尺寸 - 子类重写此方法"""
        pass


class ResponsiveCard(QWidget):
    """响应式卡片组件"""
    
    def __init__(self, parent=None, title="", content_widget=None):
        super().__init__(parent)
        self.title = title
        self.content_widget = content_widget
        self.current_mode = "desktop"
        self.setup_ui()
        
    def setup_ui(self):
        """设置UI"""
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(15)
        
        # 标题
        if self.title:
            from PyQt6.QtWidgets import QLabel
            self.title_label = QLabel(self.title)
            self.title_label.setStyleSheet("""
                font-size: 18px;
                font-weight: 600;
                color: #1e293b;
                margin-bottom: 10px;
            """)
            self.layout.addWidget(self.title_label)
            
        # 内容
        if self.content_widget:
            self.layout.addWidget(self.content_widget)
            
        # 基础样式
        self.setStyleSheet("""
            QWidget {
                background-color: white;
                border: 1px solid #e2e8f0;
                border-radius: 12px;
            }
        """)
        
    def apply_responsive_layout(self, mode):
        """应用响应式布局"""
        self.current_mode = mode
        
        if mode == "mobile":
            # 移动端：减小内边距和字体
            self.layout.setContentsMargins(15, 15, 15, 15)
            self.layout.setSpacing(10)
            if hasattr(self, 'title_label'):
                self.title_label.setStyleSheet("""
                    font-size: 16px;
                    font-weight: 600;
                    color: #1e293b;
                    margin-bottom: 8px;
                """)
        elif mode == "tablet":
            # 平板端：中等尺寸
            self.layout.setContentsMargins(18, 18, 18, 18)
            self.layout.setSpacing(12)
            if hasattr(self, 'title_label'):
                self.title_label.setStyleSheet("""
                    font-size: 17px;
                    font-weight: 600;
                    color: #1e293b;
                    margin-bottom: 9px;
                """)
        else:
            # 桌面端：标准尺寸
            self.layout.setContentsMargins(20, 20, 20, 20)
            self.layout.setSpacing(15)
            if hasattr(self, 'title_label'):
                self.title_label.setStyleSheet("""
                    font-size: 18px;
                    font-weight: 600;
                    color: #1e293b;
                    margin-bottom: 10px;
                """)


class ResponsiveInputWidget(QWidget):
    """响应式输入组件"""
    
    def __init__(self, parent=None, placeholder=""):
        super().__init__(parent)
        self.placeholder = placeholder
        self.current_mode = "desktop"
        self.setup_ui()
        
    def setup_ui(self):
        """设置UI"""
        from PyQt6.QtWidgets import QHBoxLayout, QLineEdit, QPushButton
        
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(10)
        
        # 输入框
        self.input = QLineEdit()
        self.input.setPlaceholderText(self.placeholder)
        self.layout.addWidget(self.input)
        
        # 按钮
        self.button = QPushButton("添加")
        self.layout.addWidget(self.button)
        
    def apply_responsive_layout(self, mode):
        """应用响应式布局"""
        self.current_mode = mode
        
        if mode == "mobile":
            # 移动端：垂直布局
            from PyQt6.QtWidgets import QVBoxLayout
            self.layout.setDirection(QVBoxLayout.Direction.TopToBottom)
            self.input.setMinimumHeight(40)
            self.button.setMinimumHeight(40)
        else:
            # 桌面/平板端：水平布局
            from PyQt6.QtWidgets import QHBoxLayout
            self.layout.setDirection(QHBoxLayout.Direction.LeftToRight)
            if mode == "tablet":
                self.input.setMinimumHeight(45)
                self.button.setMinimumHeight(45)
            else:
                self.input.setMinimumHeight(50)
                self.button.setMinimumHeight(50)


class ResponsiveListWidget(QWidget):
    """响应式列表组件"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_mode = "desktop"
        self.setup_ui()
        
    def setup_ui(self):
        """设置UI"""
        from PyQt6.QtWidgets import QVBoxLayout, QListWidget, QLabel
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(10)
        
        # 标题
        self.title_label = QLabel("组件列表")
        self.title_label.setStyleSheet("""
            font-size: 16px;
            font-weight: 600;
            color: #1e293b;
        """)
        self.layout.addWidget(self.title_label)
        
        # 列表
        self.list_widget = QListWidget()
        self.layout.addWidget(self.list_widget)
        
        # 统计信息
        self.stats_label = QLabel("共 0 个组件")
        self.stats_label.setStyleSheet("color: #64748b; font-size: 12px;")
        self.layout.addWidget(self.stats_label)
        
    def apply_responsive_layout(self, mode):
        """应用响应式布局"""
        self.current_mode = mode
        
        if mode == "mobile":
            # 移动端：紧凑布局
            self.title_label.setStyleSheet("""
                font-size: 14px;
                font-weight: 600;
                color: #1e293b;
            """)
            self.stats_label.setStyleSheet("color: #64748b; font-size: 11px;")
            self.list_widget.setStyleSheet("""
                QListWidget {
                    font-size: 12px;
                }
                QListWidget::item {
                    padding: 8px;
                    margin: 3px 0;
                }
            """)
        elif mode == "tablet":
            # 平板端：中等布局
            self.title_label.setStyleSheet("""
                font-size: 15px;
                font-weight: 600;
                color: #1e293b;
            """)
            self.stats_label.setStyleSheet("color: #64748b; font-size: 11px;")
            self.list_widget.setStyleSheet("""
                QListWidget {
                    font-size: 13px;
                }
                QListWidget::item {
                    padding: 10px;
                    margin: 4px 0;
                }
            """)
        else:
            # 桌面端：标准布局
            self.title_label.setStyleSheet("""
                font-size: 16px;
                font-weight: 600;
                color: #1e293b;
            """)
            self.stats_label.setStyleSheet("color: #64748b; font-size: 12px;")
            self.list_widget.setStyleSheet("""
                QListWidget {
                    font-size: 14px;
                }
                QListWidget::item {
                    padding: 12px;
                    margin: 5px 0;
                }
            """)


class ResponsiveButton(QPushButton):
    """响应式按钮"""
    
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.current_mode = "desktop"
        self.setup_style()
        
    def setup_style(self):
        """设置样式"""
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.apply_responsive_layout("desktop")
        
    def apply_responsive_layout(self, mode):
        """应用响应式布局"""
        self.current_mode = mode
        
        if mode == "mobile":
            self.setMinimumHeight(45)
            self.setStyleSheet("""
                QPushButton {
                    background-color: #2563eb;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 12px 16px;
                    font-size: 14px;
                    font-weight: 500;
                }
                QPushButton:hover {
                    background-color: #1d4ed8;
                }
            """)
        elif mode == "tablet":
            self.setMinimumHeight(48)
            self.setStyleSheet("""
                QPushButton {
                    background-color: #2563eb;
                    color: white;
                    border: none;
                    border-radius: 10px;
                    padding: 14px 20px;
                    font-size: 15px;
                    font-weight: 500;
                }
                QPushButton:hover {
                    background-color: #1d4ed8;
                }
            """)
        else:
            self.setMinimumHeight(50)
            self.setStyleSheet("""
                QPushButton {
                    background-color: #2563eb;
                    color: white;
                    border: none;
                    border-radius: 12px;
                    padding: 16px 24px;
                    font-size: 16px;
                    font-weight: 500;
                }
                QPushButton:hover {
                    background-color: #1d4ed8;
                }
            """)


# 布局工具函数
def create_responsive_spacing(mode):
    """创建响应式间距"""
    spacing = {
        "mobile": {
            "small": 8,
            "medium": 12,
            "large": 16
        },
        "tablet": {
            "small": 10,
            "medium": 15,
            "large": 20
        },
        "desktop": {
            "small": 12,
            "medium": 18,
            "large": 25
        }
    }
    return spacing.get(mode, spacing["desktop"])


def create_responsive_margins(mode):
    """创建响应式边距"""
    margins = {
        "mobile": {
            "small": (10, 10, 10, 10),
            "medium": (15, 15, 15, 15),
            "large": (20, 20, 20, 20)
        },
        "tablet": {
            "small": (15, 15, 15, 15),
            "medium": (20, 20, 20, 20),
            "large": (25, 25, 25, 25)
        },
        "desktop": {
            "small": (20, 20, 20, 20),
            "medium": (25, 25, 25, 25),
            "large": (30, 30, 30, 30)
        }
    }
    return margins.get(mode, margins["desktop"])