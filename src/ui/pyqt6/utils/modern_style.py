#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
现代化UI样式管理器
提供美观、现代的界面样式和主题
"""

from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt6.QtWidgets import QPushButton, QLineEdit
from PyQt6.QtGui import QColor,QFont


class ModernStyle:
    """现代化样式管理器"""
    
    # 现代配色方案
    COLORS = {
        'primary': '#2563eb',      # 主色调 - 蓝色
        'primary_dark': '#1d4ed8', # 深色主调
        'secondary': '#64748b',    # 次要色 - 灰色
        'accent': '#f59e0b',       # 强调色 - 橙色
        'success': '#10b981',      # 成功色 - 绿色
        'warning': '#f59e0b',      # 警告色 - 橙色
        'error': '#ef4444',        # 错误色 - 红色
        'background': '#ffffff',   # 背景色
        'surface': '#f8fafc',      # 表面色
        'text_primary': '#1e293b', # 主要文字
        'text_secondary': '#64748b', # 次要文字
        'border': '#e2e8f0',       # 边框色
        'shadow': 'rgba(0, 0, 0, 0.1)', # 阴影
    }
    
    # 暗色主题
    DARK_COLORS = {
        'primary': '#3b82f6',
        'primary_dark': '#2563eb',
        'secondary': '#94a3b8',
        'accent': '#fbbf24',
        'success': '#34d399',
        'warning': '#fbbf24',
        'error': '#f87171',
        'background': '#0f172a',
        'surface': '#1e293b',
        'text_primary': '#f1f5f9',
        'text_secondary': '#94a3b8',
        'border': '#334155',
        'shadow': 'rgba(0, 0, 0, 0.3)',
    }
    
    @staticmethod
    def get_main_stylesheet(theme='light'):
        """获取主窗口样式表"""
        colors = ModernStyle.DARK_COLORS if theme == 'dark' else ModernStyle.COLORS
        
        return f"""
        /* 主窗口样式 */
        QMainWindow {{
            background-color: {colors['background']};
            color: {colors['text_primary']};
        }}
        
        /* 中央部件 */
        QWidget#centralWidget {{
            background-color: {colors['background']};
        }}
        
        /* 现代卡片样式 */
        QFrame#modernCard {{
            background-color: {colors['surface']};
            border: 1px solid {colors['border']};
            border-radius: 12px;
            padding: 20px;
            margin: 5px;
        }}
        
        QFrame#modernCard:hover {{
            border-color: {colors['primary']};
        }}
        
        /* 标题栏样式 */
        QFrame#headerFrame {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                      stop:0 {colors['primary']}, 
                                      stop:1 {colors['primary_dark']});
            border-radius: 0px;
            padding: 20px;
        }}
        
        /* 导航栏样式 */
        QWidget#navigationPanel {{
            background-color: {colors['surface']};
            border-right: 1px solid {colors['border']};
        }}
        
        /* 现代按钮样式 */
        QPushButton {{
            background-color: {colors['primary']};
            color: white;
            border: none;
            border-radius: 8px;
            padding: 10px 20px;
            font-weight: 500;
            font-size: 14px;
            min-height: 40px;
        }}
        
        QPushButton:hover {{
            background-color: {colors['primary_dark']};
        }}
        
        QPushButton:pressed {{
            background-color: {colors['primary']};
        }}
        
        QPushButton:disabled {{
            background-color: {colors['secondary']};
            color: {colors['text_secondary']};
        }}
        
        /* 次要按钮样式 */
        QPushButton#secondaryButton {{
            background-color: transparent;
            color: {colors['primary']};
            border: 2px solid {colors['primary']};
        }}
        
        QPushButton#secondaryButton:hover {{
            background-color: {colors['primary']};
            color: white;
        }}
        
        /* 输入框样式 */
        QLineEdit {{
            background-color: {colors['background']};
            color: {colors['text_primary']};
            border: 2px solid {colors['border']};
            border-radius: 8px;
            padding: 12px 16px;
            font-size: 14px;
            min-height: 20px;
        }}
        
        QLineEdit:focus {{
            border-color: {colors['primary']};
            outline: none;
        }}
        
        QLineEdit:disabled {{
            background-color: {colors['surface']};
            color: {colors['text_secondary']};
        }}
        
        /* 文本编辑框样式 */
        QTextEdit {{
            background-color: {colors['background']};
            color: {colors['text_primary']};
            border: 2px solid {colors['border']};
            border-radius: 8px;
            padding: 12px;
            font-size: 14px;
        }}
        
        QTextEdit:focus {{
            border-color: {colors['primary']};
        }}
        
        /* 组合框样式 */
        QComboBox {{
            background-color: {colors['background']};
            color: {colors['text_primary']};
            border: 2px solid {colors['border']};
            border-radius: 8px;
            padding: 12px 16px;
            font-size: 14px;
            min-height: 20px;
        }}
        
        QComboBox:focus {{
            border-color: {colors['primary']};
        }}
        
        QComboBox::drop-down {{
            border: none;
            width: 30px;
        }}
        
        QComboBox::down-arrow {{
            image: none;
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-top: 5px solid {colors['text_secondary']};
        }}
        
        /* 复选框样式 */
        QCheckBox {{
            color: {colors['text_primary']};
            font-size: 14px;
            spacing: 8px;
        }}
        
        QCheckBox::indicator {{
            width: 18px;
            height: 18px;
            border: 2px solid {colors['border']};
            border-radius: 4px;
            background-color: {colors['background']};
        }}
        
        QCheckBox::indicator:checked {{
            background-color: {colors['primary']};
            border-color: {colors['primary']};
            image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iOSIgdmlld0JveD0iMCAwIDEyIDkiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxwYXRoIGQ9Ik0xIDRMNC41IDcuNUwxMSAxIiBzdHJva2U9IndoaXRlIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIvPgo8L3N2Zz4=);
        }}
        
        /* 列表样式 */
        QListWidget {{
            background-color: {colors['background']};
            color: {colors['text_primary']};
            border: 2px solid {colors['border']};
            border-radius: 8px;
            padding: 8px;
            font-size: 14px;
        }}
        
        QListWidget::item {{
            padding: 12px;
            border-radius: 6px;
            margin: 2px 0;
        }}
        
        QListWidget::item:hover {{
            background-color: {colors['surface']};
        }}
        
        QListWidget::item:selected {{
            background-color: {colors['primary']};
            color: white;
        }}
        
        /* 标签页样式 */
        QTabWidget::pane {{
            border: 1px solid {colors['border']};
            border-radius: 8px;
            background-color: {colors['background']};
        }}
        
        QTabBar::tab {{
            background-color: {colors['surface']};
            color: {colors['text_secondary']};
            border: none;
            padding: 12px 24px;
            margin-right: 2px;
            font-size: 14px;
            font-weight: 500;
        }}
        
        QTabBar::tab:hover {{
            background-color: {colors['border']};
            color: {colors['text_primary']};
        }}
        
        QTabBar::tab:selected {{
            background-color: {colors['primary']};
            color: white;
        }}
        
        /* 状态栏样式 */
        QStatusBar {{
            background-color: {colors['surface']};
            color: {colors['text_secondary']};
            border-top: 1px solid {colors['border']};
        }}
        
        /* 菜单栏样式 */
        QMenuBar {{
            background-color: {colors['surface']};
            color: {colors['text_primary']};
            border-bottom: 1px solid {colors['border']};
        }}
        
        QMenuBar::item {{
            padding: 8px 16px;
            background-color: transparent;
        }}
        
        QMenuBar::item:selected {{
            background-color: {colors['border']};
        }}
        
        /* 滚动条样式 */
        QScrollBar:vertical {{
            background-color: {colors['surface']};
            width: 12px;
            border-radius: 6px;
        }}
        
        QScrollBar::handle:vertical {{
            background-color: {colors['border']};
            border-radius: 6px;
            min-height: 20px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background-color: {colors['secondary']};
        }}
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            border: none;
            background: none;
        }}
        """
    
    @staticmethod
    def get_gradient_background(color1, color2, direction='horizontal'):
        """获取渐变背景"""
        if direction == 'horizontal':
            return f"qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {color1}, stop:1 {color2})"
        else:
            return f"qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 {color1}, stop:1 {color2})"
    
    @staticmethod
    def add_shadow_effect(widget, blur_radius=20, offset=(0, 2)):
        """添加阴影效果"""
        from PyQt6.QtWidgets import QGraphicsDropShadowEffect
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(blur_radius)
        shadow.setOffset(*offset)
        shadow.setColor(QColor(0, 0, 0, 60))
        widget.setGraphicsEffect(shadow)
    
    @staticmethod
    def add_hover_animation(button, normal_color, hover_color):
        """添加悬停动画效果"""
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {normal_color};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-weight: 500;
            }}
        """)
        
        def enter_event(event):
            button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {hover_color};
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 10px 20px;
                    font-weight: 500;
                }}
            """)
            
        def leave_event(event):
            button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {normal_color};
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 10px 20px;
                    font-weight: 500;
                }}
            """)
        
        button.enterEvent = enter_event
        button.leaveEvent = leave_event


class ModernButton(QPushButton):
    """现代化按钮组件"""
    
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setup_style()
        self.setup_animation()
    
    def setup_style(self):
        """设置样式"""
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumHeight(45)
        
    def setup_animation(self):
        """设置动画效果"""
        # 创建缩放动画
        self.scale_animation = QPropertyAnimation(self, b"geometry")
        self.scale_animation.setDuration(150)
        self.scale_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        self.original_geometry = None
    
    def mousePressEvent(self, event):
        """鼠标按下事件"""
        if self.original_geometry is None:
            self.original_geometry = self.geometry()
        
        # 按下时缩小效果
        new_rect = self.original_geometry.adjusted(1, 1, -1, -1)
        self.scale_animation.setStartValue(self.geometry())
        self.scale_animation.setEndValue(new_rect)
        self.scale_animation.start()
        
        super().mousePressEvent(event)
    
    def mouseReleaseEvent(self, event):
        """鼠标释放事件"""
        if self.original_geometry:
            # 释放时恢复原状
            self.scale_animation.setStartValue(self.geometry())
            self.scale_animation.setEndValue(self.original_geometry)
            self.scale_animation.start()
        
        super().mouseReleaseEvent(event)


class ModernLineEdit(QLineEdit):
    """现代化输入框组件"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_style()
        self.setup_animation()
    
    def setup_style(self):
        """设置样式"""
        self.setMinimumHeight(45)
        self.setFont(QFont("Segoe UI", 11))
        
    def setup_animation(self):
        """设置动画效果"""
        # 边框颜色动画
        self.border_animation = QPropertyAnimation(self, b"styleSheet")
        self.border_animation.setDuration(200)
        
    def focusInEvent(self, event):
        """获得焦点事件"""
        super().focusInEvent(event)
        # 可以添加焦点动画效果
        
    def focusOutEvent(self, event):
        """失去焦点事件"""
        super().focusOutEvent(event)
        # 可以添加失去焦点动画效果