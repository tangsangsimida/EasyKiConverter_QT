#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
现代化主窗口
采用毛玻璃效果、渐变背景和现代化布局
"""

import sys
from pathlib import Path
from typing import Optional

from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                           QPushButton, QLabel, QFrame, QStackedWidget, QStatusBar,
                           QGraphicsDropShadowEffect, QApplication)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QPoint, QTimer, pyqtSignal
from PyQt6.QtGui import QColor, QPalette, QLinearGradient, QBrush, QPainter, QFont, QIcon

# 导入必要的模块
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.insert(0, str(parent_dir))

from utils.config_manager import ConfigManager
from utils.modern_style import ModernStyle, ModernButton, ModernLineEdit
from widgets.modern_component_input_widget import ModernComponentInputWidget
from widgets.navigation_widget import NavigationWidget
from widgets.progress_widget import ProgressWidget
from widgets.results_widget import ResultsWidget


class ModernMainWindow(QMainWindow):
    """现代化主窗口"""
    
    # 信号定义
    theme_changed = pyqtSignal(str)
    
    def __init__(self, config_manager: ConfigManager, parent=None):
        super().__init__(parent)
        self.config_manager = config_manager
        self.current_theme = "light"
        self.animation_enabled = True
        
        self.setup_window()
        self.setup_ui()
        self.setup_animations()
        self.setup_connections()
        self.load_settings()
        
    def setup_window(self):
        """设置窗口属性"""
        self.setWindowTitle("EasyKiConverter - 现代化EDA转换工具")
        self.setMinimumSize(1400, 900)
        self.resize(1600, 1000)
        
        # 设置窗口图标
        # self.setWindowIcon(QIcon(":/icons/app_icon.png"))
        
        # 设置窗口属性
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowSystemMenuHint)
        
    def setup_ui(self):
        """设置用户界面"""
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 创建侧边导航栏
        self.sidebar = self.create_sidebar()
        main_layout.addWidget(self.sidebar)
        
        # 创建主内容区域
        self.main_content = self.create_main_content()
        main_layout.addWidget(self.main_content, 1)
        
        # 创建标题栏
        self.title_bar = self.create_title_bar()
        
        # 重新组织布局
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        content_layout.addWidget(self.title_bar)
        content_layout.addWidget(self.main_content)
        
        # 创建主容器
        main_container = QWidget()
        main_container.setLayout(content_layout)
        main_layout.addWidget(main_container, 1)
        
        # 应用样式
        self.apply_modern_style()
        
    def create_title_bar(self) -> QWidget:
        """创建现代化标题栏"""
        title_bar = QWidget()
        title_bar.setFixedHeight(60)
        title_bar.setObjectName("titleBar")
        
        layout = QHBoxLayout(title_bar)
        layout.setContentsMargins(20, 0, 20, 0)
        layout.setSpacing(10)
        
        # 应用图标
        app_icon = QLabel("⚡")
        app_icon.setObjectName("appIcon")
        app_icon.setStyleSheet("""
            QLabel#appIcon {
                font-size: 24px;
                font-weight: bold;
                color: white;
                background-color: #2563eb;
                border-radius: 12px;
                padding: 8px;
                min-width: 24px;
                min-height: 24px;
                qproperty-alignment: AlignCenter;
            }
        """)
        layout.addWidget(app_icon)
        
        # 应用标题
        app_title = QLabel("EasyKiConverter")
        app_title.setObjectName("appTitle")
        app_title.setStyleSheet("""
            QLabel#appTitle {
                font-size: 18px;
                font-weight: 600;
                color: #1e293b;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
        """)
        layout.addWidget(app_title)
        
        layout.addStretch()
        
        # 主题切换按钮
        self.theme_button = QPushButton("🌙")
        self.theme_button.setObjectName("themeButton")
        self.theme_button.setFixedSize(40, 40)
        self.theme_button.setStyleSheet("""
            QPushButton#themeButton {
                background-color: transparent;
                border: none;
                border-radius: 20px;
                font-size: 18px;
                color: #64748b;
            }
            QPushButton#themeButton:hover {
                background-color: #f1f5f9;
                color: #2563eb;
            }
        """)
        self.theme_button.clicked.connect(self.toggle_theme)
        layout.addWidget(self.theme_button)
        
        # 窗口控制按钮
        self.min_button = QPushButton("−")
        self.min_button.setObjectName("windowButton")
        self.min_button.setFixedSize(40, 40)
        self.min_button.clicked.connect(self.showMinimized)
        layout.addWidget(self.min_button)
        
        self.max_button = QPushButton("□")
        self.max_button.setObjectName("windowButton")
        self.max_button.setFixedSize(40, 40)
        self.max_button.clicked.connect(self.toggle_maximized)
        layout.addWidget(self.max_button)
        
        self.close_button = QPushButton("×")
        self.close_button.setObjectName("windowButton")
        self.close_button.setFixedSize(40, 40)
        self.close_button.clicked.connect(self.close)
        layout.addWidget(self.close_button)
        
        # 设置标题栏样式
        title_bar.setStyleSheet("""
            QWidget#titleBar {
                background-color: #ffffff;
                border-bottom: 1px solid #e2e8f0;
            }
            QPushButton#windowButton {
                background-color: transparent;
                border: none;
                border-radius: 20px;
                font-size: 16px;
                font-weight: 300;
                color: #64748b;
                min-width: 40px;
                min-height: 40px;
            }
            QPushButton#windowButton:hover {
                background-color: #f1f5f9;
                color: #1e293b;
            }
            QPushButton#windowButton:pressed {
                background-color: #e2e8f0;
            }
            QPushButton#windowButton[text="×"]:hover {
                background-color: #ef4444;
                color: white;
            }
        """)
        
        return title_bar
        
    def create_sidebar(self) -> QWidget:
        """创建现代化侧边栏"""
        sidebar = QWidget()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(280)
        sidebar.setStyleSheet("""
            QWidget#sidebar {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                          stop:0 #1e293b, 
                                          stop:1 #334155);
                border-right: none;
            }
        """)
        
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(0, 20, 0, 20)
        layout.setSpacing(10)
        
        # Logo区域
        logo_container = QWidget()
        logo_layout = QVBoxLayout(logo_container)
        logo_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        logo_label = QLabel("⚡")
        logo_label.setStyleSheet("""
            color: white;
            font-size: 48px;
            font-weight: bold;
            background-color: rgba(255, 255, 255, 0.1);
            border-radius: 24px;
            padding: 16px;
            margin: 10px;
        """)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_layout.addWidget(logo_label)
        
        app_name = QLabel("EasyKi\nConverter")
        app_name.setStyleSheet("""
            color: white;
            font-size: 20px;
            font-weight: 600;
            text-align: center;
            background: transparent;
            padding: 10px;
        """)
        app_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_layout.addWidget(app_name)
        
        layout.addWidget(logo_container)
        
        # 导航菜单
        nav_container = QWidget()
        nav_layout = QVBoxLayout(nav_container)
        nav_layout.setSpacing(5)
        
        nav_items = [
            ("🏠", "元件转换", "component"),
            ("📊", "转换历史", "history"),
            ("⚙️", "设置", "settings"),
            ("ℹ️", "关于", "about")
        ]
        
        self.nav_buttons = {}
        for icon, text, name in nav_items:
            btn = QPushButton(f"{icon}  {text}")
            btn.setObjectName(f"nav_{name}")
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: #cbd5e1;
                    border: none;
                    border-radius: 12px;
                    padding: 15px 20px;
                    font-size: 14px;
                    font-weight: 500;
                    text-align: left;
                    margin: 2px 15px;
                }
                QPushButton:hover {
                    background-color: rgba(255, 255, 255, 0.1);
                    color: white;
                }
                QPushButton:pressed {
                    background-color: rgba(255, 255, 255, 0.2);
                }
                QPushButton:checked {
                    background-color: #2563eb;
                    color: white;
                }
            """)
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, n=name: self.switch_page(n))
            nav_layout.addWidget(btn)
            self.nav_buttons[name] = btn
            
        nav_layout.addStretch()
        layout.addWidget(nav_container)
        
        # 用户信息区域
        user_container = QWidget()
        user_layout = QHBoxLayout(user_container)
        user_layout.setContentsMargins(15, 10, 15, 10)
        
        user_avatar = QLabel("👤")
        user_avatar.setStyleSheet("""
            color: white;
            font-size: 20px;
            background-color: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 8px;
            min-width: 30px;
            min-height: 30px;
            qproperty-alignment: AlignCenter;
        """)
        user_layout.addWidget(user_avatar)
        
        user_info = QWidget()
        user_info_layout = QVBoxLayout(user_info)
        user_info_layout.setContentsMargins(0, 0, 0, 0)
        user_info_layout.setSpacing(2)
        
        user_name = QLabel("用户")
        user_name.setStyleSheet("""
            color: white;
            font-size: 14px;
            font-weight: 500;
        """)
        user_info_layout.addWidget(user_name)
        
        user_status = QLabel("在线")
        user_status.setStyleSheet("""
            color: #10b981;
            font-size: 12px;
        """)
        user_info_layout.addWidget(user_status)
        
        user_layout.addWidget(user_info)
        user_layout.addStretch()
        
        layout.addWidget(user_container)
        
        return sidebar
        
    def create_main_content(self) -> QWidget:
        """创建主内容区域"""
        content = QWidget()
        content.setObjectName("mainContent")
        content.setStyleSheet("""
            QWidget#mainContent {
                background-color: #f8fafc;
                border-radius: 0px;
            }
        """)
        
        layout = QVBoxLayout(content)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(25)
        
        # 欢迎区域
        welcome_frame = self.create_welcome_frame()
        layout.addWidget(welcome_frame)
        
        # 主要内容堆栈
        self.content_stack = QStackedWidget()
        
        # 创建各个页面
        self.component_widget = ModernComponentInputWidget(self.config_manager)
        self.content_stack.addWidget(self.component_widget)
        
        # 添加占位页面
        for i in range(3):
            placeholder = QWidget()
            placeholder_layout = QVBoxLayout(placeholder)
            placeholder_layout.addStretch()
            label = QLabel("功能开发中...")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setStyleSheet("""
                color: #64748b;
                font-size: 18px;
                font-weight: 500;
            """)
            placeholder_layout.addWidget(label)
            placeholder_layout.addStretch()
            self.content_stack.addWidget(placeholder)
            
        layout.addWidget(self.content_stack, 1)
        
        return content
        
    def create_welcome_frame(self) -> QFrame:
        """创建欢迎区域"""
        frame = QFrame()
        frame.setObjectName("welcomeFrame")
        frame.setStyleSheet("""
            QFrame#welcomeFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                          stop:0 #2563eb, 
                                          stop:1 #3b82f6);
                border-radius: 16px;
                padding: 30px;
                color: white;
            }
        """)
        
        # 添加阴影效果
        ModernStyle.add_shadow_effect(frame, blur_radius=30, offset=(0, 8))
        
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 左侧文字
        text_container = QWidget()
        text_layout = QVBoxLayout(text_container)
        text_layout.setContentsMargins(0, 0, 0, 0)
        
        title = QLabel("欢迎使用 EasyKiConverter")
        title.setStyleSheet("""
            font-size: 28px;
            font-weight: 700;
            color: white;
            margin-bottom: 10px;
        """)
        text_layout.addWidget(title)
        
        subtitle = QLabel("将嘉立创EDA元器件轻松转换为KiCad格式")
        subtitle.setStyleSheet("""
            font-size: 16px;
            color: rgba(255, 255, 255, 0.9);
            margin-bottom: 20px;
        """)
        text_layout.addWidget(subtitle)
        
        features = QLabel("✨ 支持符号、封装、3D模型完整转换\n🚀 批量处理，高效便捷\n🎨 现代化界面，操作简单")
        features.setStyleSheet("""
            font-size: 14px;
            color: rgba(255, 255, 255, 0.8);
            line-height: 24px;
        """)
        text_layout.addWidget(features)
        
        layout.addWidget(text_container)
        layout.addStretch()
        
        # 右侧图标
        icon_label = QLabel("⚡")
        icon_label.setStyleSheet("""
            font-size: 72px;
            color: rgba(255, 255, 255, 0.3);
            background: transparent;
        """)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon_label)
        
        return frame
        
    def apply_modern_style(self):
        """应用现代化样式"""
        self.setStyleSheet(ModernStyle.get_main_stylesheet(self.current_theme))
        
    def setup_animations(self):
        """设置动画效果"""
        # 页面切换动画
        self.page_animation = QPropertyAnimation(self.content_stack, b"pos")
        self.page_animation.setDuration(300)
        self.page_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        
    def setup_connections(self):
        """设置信号连接"""
        self.theme_button.clicked.connect(self.toggle_theme)
        
    def switch_page(self, page_name: str):
        """切换页面"""
        # 更新导航按钮状态
        for name, btn in self.nav_buttons.items():
            btn.setChecked(name == page_name)
        
        # 页面映射
        page_map = {
            "component": 0,
            "history": 1,
            "settings": 2,
            "about": 3
        }
        
        if page_name in page_map:
            index = page_map[page_name]
            if self.animation_enabled:
                # 添加切换动画
                current_pos = self.content_stack.pos()
                self.content_stack.move(current_pos.x() + 50, current_pos.y())
                self.content_stack.setGraphicsEffect(None)
                
                self.page_animation.setStartValue(self.content_stack.pos())
                self.page_animation.setEndValue(current_pos)
                self.page_animation.start()
            
            self.content_stack.setCurrentIndex(index)
            
    def toggle_theme(self):
        """切换主题"""
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        self.apply_modern_style()
        
        # 更新主题按钮图标
        icon = "☀️" if self.current_theme == "dark" else "🌙"
        self.theme_button.setText(icon)
        
        self.theme_changed.emit(self.current_theme)
        
    def toggle_maximized(self):
        """切换最大化状态"""
        if self.isMaximized():
            self.showNormal()
            self.max_button.setText("□")
        else:
            self.showMaximized()
            self.max_button.setText("❐")
            
    def load_settings(self):
        """加载设置"""
        config = self.config_manager.get_config()
        if 'theme' in config:
            self.current_theme = config['theme']
            self.apply_modern_style()
            
    def save_settings(self):
        """保存设置"""
        config = self.config_manager.get_config()
        config['theme'] = self.current_theme
        self.config_manager.save_config(config)
        
    def mousePressEvent(self, event):
        """鼠标按下事件（用于窗口拖动）"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()
            
    def mouseMoveEvent(self, event):
        """鼠标移动事件（用于窗口拖动）"""
        if event.buttons() == Qt.MouseButton.LeftButton and hasattr(self, 'drag_position'):
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()