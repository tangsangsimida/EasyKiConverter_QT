#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
优化版现代化主窗口 - 修复布局问题
采用清晰的三栏式布局结构
"""

import sys
from pathlib import Path
from typing import Optional

from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                           QPushButton, QLabel, QFrame, QStackedWidget, QStatusBar,
                           QSplitter, QScrollArea, QGridLayout)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QPoint, QTimer, pyqtSignal
from PyQt6.QtGui import QColor, QPalette, QLinearGradient, QBrush, QPainter, QFont, QIcon

# 导入必要的模块
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.insert(0, str(parent_dir))

from utils.config_manager import ConfigManager
from utils.modern_style import ModernStyle, ModernButton, ModernLineEdit
from widgets.optimized_component_input_widget import OptimizedComponentInputWidget
from utils.ui_effects import LoadingSpinner, ModernCard, SuccessAnimation


class OptimizedMainWindow(QMainWindow):
    """优化版现代化主窗口"""
    
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
        self.setMinimumSize(1200, 800)
        self.resize(1400, 900)
        
        # 设置窗口图标
        # self.setWindowIcon(QIcon(":/icons/app_icon.png"))
        
        # 设置窗口属性
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowSystemMenuHint)
        
    def setup_ui(self):
        """设置用户界面 - 采用清晰的三栏式布局"""
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局 - 垂直布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 1. 标题栏
        self.title_bar = self.create_title_bar()
        main_layout.addWidget(self.title_bar)
        
        # 2. 主内容区域 - 水平分割
        content_splitter = QSplitter(Qt.Orientation.Horizontal)
        content_splitter.setHandleWidth(1)
        content_splitter.setStyleSheet("""
            QSplitter::handle {
                background-color: #e2e8f0;
            }
            QSplitter::handle:hover {
                background-color: #cbd5e1;
            }
        """)
        
        # 左侧导航栏
        self.sidebar = self.create_sidebar()
        content_splitter.addWidget(self.sidebar)
        
        # 中间主工作区
        self.main_workspace = self.create_main_workspace()
        content_splitter.addWidget(self.main_workspace)
        
        # 右侧辅助面板（可选）
        self.side_panel = self.create_side_panel()
        content_splitter.addWidget(self.side_panel)
        
        # 设置分割器比例
        content_splitter.setSizes([280, 800, 320])
        content_splitter.setStretchFactor(0, 0)  # 导航栏不拉伸
        content_splitter.setStretchFactor(1, 1)  # 主工作区拉伸
        content_splitter.setStretchFactor(2, 0)  # 辅助面板不拉伸
        
        main_layout.addWidget(content_splitter)
        
        # 3. 状态栏
        self.status_bar = self.create_status_bar()
        main_layout.addWidget(self.status_bar)
        
        # 应用样式
        self.apply_modern_style()
        
    def create_title_bar(self) -> QWidget:
        """创建现代化标题栏"""
        title_bar = QWidget()
        title_bar.setFixedHeight(70)
        title_bar.setObjectName("titleBar")
        
        layout = QHBoxLayout(title_bar)
        layout.setContentsMargins(25, 0, 25, 0)
        layout.setSpacing(15)
        
        # 应用图标
        app_icon = QLabel("⚡")
        app_icon.setObjectName("appIcon")
        app_icon.setStyleSheet("""
            QLabel#appIcon {
                font-size: 28px;
                font-weight: bold;
                color: white;
                background-color: #2563eb;
                border-radius: 14px;
                padding: 10px;
                min-width: 28px;
                min-height: 28px;
                qproperty-alignment: AlignCenter;
            }
        """)
        layout.addWidget(app_icon)
        
        # 应用标题
        title_container = QWidget()
        title_layout = QVBoxLayout(title_container)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(2)
        
        app_title = QLabel("EasyKiConverter")
        app_title.setObjectName("appTitle")
        app_title.setStyleSheet("""
            QLabel#appTitle {
                font-size: 20px;
                font-weight: 700;
                color: #1e293b;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
        """)
        title_layout.addWidget(app_title)
        
        app_subtitle = QLabel("嘉立创EDA转KiCad工具")
        app_subtitle.setStyleSheet("""
            font-size: 12px;
            color: #64748b;
            font-weight: 400;
        """)
        title_layout.addWidget(app_subtitle)
        layout.addWidget(title_container)
        
        layout.addStretch()
        
        # 主题切换按钮
        self.theme_button = QPushButton("🌙")
        self.theme_button.setObjectName("themeButton")
        self.theme_button.setFixedSize(42, 42)
        self.theme_button.setStyleSheet("""
            QPushButton#themeButton {
                background-color: transparent;
                border: none;
                border-radius: 21px;
                font-size: 20px;
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
        self.min_button.setFixedSize(42, 42)
        self.min_button.clicked.connect(self.showMinimized)
        layout.addWidget(self.min_button)
        
        self.max_button = QPushButton("□")
        self.max_button.setObjectName("windowButton")
        self.max_button.setFixedSize(42, 42)
        self.max_button.clicked.connect(self.toggle_maximized)
        layout.addWidget(self.max_button)
        
        self.close_button = QPushButton("×")
        self.close_button.setObjectName("windowButton")
        self.close_button.setFixedSize(42, 42)
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
                border-radius: 21px;
                font-size: 18px;
                font-weight: 300;
                color: #64748b;
                min-width: 42px;
                min-height: 42px;
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
        sidebar.setMinimumWidth(280)
        sidebar.setMaximumWidth(320)
        sidebar.setStyleSheet("""
            QWidget#sidebar {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                          stop:0 #1e293b, 
                                          stop:1 #334155);
                border-right: none;
            }
        """)
        
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(0, 25, 0, 25)
        layout.setSpacing(20)
        
        # Logo区域
        logo_container = QWidget()
        logo_layout = QVBoxLayout(logo_container)
        logo_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        logo_label = QLabel("⚡")
        logo_label.setStyleSheet("""
            color: white;
            font-size: 52px;
            font-weight: bold;
            background-color: rgba(255, 255, 255, 0.1);
            border-radius: 26px;
            padding: 18px;
            margin: 15px;
            min-width: 52px;
            min-height: 52px;
            qproperty-alignment: AlignCenter;
        """)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_layout.addWidget(logo_label)
        
        app_name = QLabel("EasyKi\nConverter")
        app_name.setStyleSheet("""
            color: white;
            font-size: 22px;
            font-weight: 600;
            text-align: center;
            background: transparent;
            padding: 12px;
        """)
        app_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_layout.addWidget(app_name)
        
        layout.addWidget(logo_container)
        
        # 导航菜单
        nav_container = QWidget()
        nav_layout = QVBoxLayout(nav_container)
        nav_layout.setSpacing(8)
        
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
                    border-radius: 14px;
                    padding: 18px 24px;
                    font-size: 15px;
                    font-weight: 500;
                    text-align: left;
                    margin: 3px 18px;
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
        user_layout.setContentsMargins(20, 15, 20, 15)
        
        user_avatar = QLabel("👤")
        user_avatar.setStyleSheet("""
            color: white;
            font-size: 22px;
            background-color: rgba(255, 255, 255, 0.1);
            border-radius: 18px;
            padding: 10px;
            min-width: 36px;
            min-height: 36px;
            qproperty-alignment: AlignCenter;
        """)
        user_layout.addWidget(user_avatar)
        
        user_info = QWidget()
        user_info_layout = QVBoxLayout(user_info)
        user_info_layout.setContentsMargins(0, 0, 0, 0)
        user_info_layout.setSpacing(3)
        
        user_name = QLabel("用户")
        user_name.setStyleSheet("""
            color: white;
            font-size: 15px;
            font-weight: 500;
        """)
        user_info_layout.addWidget(user_name)
        
        user_status = QLabel("在线")
        user_status.setStyleSheet("""
            color: #10b981;
            font-size: 13px;
        """)
        user_info_layout.addWidget(user_status)
        
        user_layout.addWidget(user_info)
        user_layout.addStretch()
        
        layout.addWidget(user_container)
        
        return sidebar
        
    def create_main_workspace(self) -> QWidget:
        """创建主工作区"""
        workspace = QWidget()
        workspace.setObjectName("mainWorkspace")
        workspace.setStyleSheet("""
            QWidget#mainWorkspace {
                background-color: #f8fafc;
            }
        """)
        
        layout = QVBoxLayout(workspace)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 创建堆栈式内容区域
        self.content_stack = QStackedWidget()
        
        # 创建各个页面
        self.component_widget = OptimizedComponentInputWidget(self.config_manager)
        self.content_stack.addWidget(self.component_widget)
        
        # 添加其他页面的占位符
        for i, (title, description) in enumerate([
            ("转换历史", "查看和管理您的转换记录"),
            ("设置", "配置应用程序选项"),
            ("关于", "了解应用程序信息")
        ]):
            placeholder = self.create_placeholder_page(title, description)
            self.content_stack.addWidget(placeholder)
            
        layout.addWidget(self.content_stack)
        
        return workspace
        
    def create_side_panel(self) -> QWidget:
        """创建右侧辅助面板"""
        panel = QWidget()
        panel.setObjectName("sidePanel")
        panel.setMinimumWidth(300)
        panel.setMaximumWidth(400)
        panel.setStyleSheet("""
            QWidget#sidePanel {
                background-color: #ffffff;
                border-left: 1px solid #e2e8f0;
            }
        """)
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)
        
        # 快速操作区域
        quick_actions = self.create_quick_actions_card()
        layout.addWidget(quick_actions)
        
        # 统计信息区域
        stats_card = self.create_stats_card()
        layout.addWidget(stats_card)
        
        # 帮助信息区域
        help_card = self.create_help_card()
        layout.addWidget(help_card)
        
        layout.addStretch()
        
        return panel
        
    def create_placeholder_page(self, title: str, description: str) -> QWidget:
        """创建占位符页面"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # 图标
        icon = QLabel("🚧")
        icon.setStyleSheet("""
            font-size: 64px;
            color: #cbd5e1;
            margin-bottom: 20px;
        """)
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon)
        
        # 标题
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: 600;
            color: #64748b;
            margin-bottom: 10px;
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # 描述
        desc_label = QLabel(description)
        desc_label.setStyleSheet("""
            font-size: 16px;
            color: #94a3b8;
            text-align: center;
        """)
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)
        
        layout.addStretch()
        
        return page
        
    def create_quick_actions_card(self) -> QWidget:
        """创建快速操作卡片"""
        card = ModernCard(
            title="快速操作",
            icon="⚡",
            description="常用功能的快捷入口"
        )
        
        # 添加快速操作按钮
        actions_layout = QVBoxLayout()
        actions_layout.setSpacing(10)
        
        actions = [
            ("📋 新建转换", self.new_conversion),
            ("📁 打开BOM", self.open_bom),
            ("💾 保存项目", self.save_project),
            ("🔄 批量处理", self.batch_process)
        ]
        
        for text, callback in actions:
            btn = QPushButton(text)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #f1f5f9;
                    color: #475569;
                    border: 1px solid #e2e8f0;
                    border-radius: 8px;
                    padding: 10px 15px;
                    font-size: 13px;
                    font-weight: 500;
                    text-align: left;
                }
                QPushButton:hover {
                    background-color: #e2e8f0;
                    color: #1e293b;
                }
            """)
            btn.clicked.connect(callback)
            actions_layout.addWidget(btn)
            
        card.layout().addLayout(actions_layout)
        return card
        
    def create_stats_card(self) -> QWidget:
        """创建统计信息卡片"""
        card = ModernCard(
            title="统计信息",
            icon="📊",
            description="转换数据统计"
        )
        
        # 添加统计信息
        stats_layout = QVBoxLayout()
        stats_layout.setSpacing(8)
        
        stats = [
            ("总转换次数", "0"),
            ("成功次数", "0"),
            ("失败次数", "0"),
            ("平均用时", "0s")
        ]
        
        for label, value in stats:
            stat_layout = QHBoxLayout()
            stat_label = QLabel(label)
            stat_label.setStyleSheet("color: #64748b; font-size: 12px;")
            stat_value = QLabel(value)
            stat_value.setStyleSheet("color: #1e293b; font-size: 12px; font-weight: 600;")
            
            stat_layout.addWidget(stat_label)
            stat_layout.addStretch()
            stat_layout.addWidget(stat_value)
            stats_layout.addLayout(stat_layout)
            
        card.layout().addLayout(stats_layout)
        return card
        
    def create_help_card(self) -> QWidget:
        """创建帮助信息卡片"""
        card = ModernCard(
            title="使用帮助",
            icon="❓",
            description="快速入门指南"
        )
        
        # 添加帮助信息
        help_layout = QVBoxLayout()
        help_layout.setSpacing(8)
        
        help_items = [
            "1. 在左侧输入元器件编号",
            "2. 选择需要导出的类型",
            "3. 设置输出目录",
            "4. 点击开始转换"
        ]
        
        for item in help_items:
            help_label = QLabel(item)
            help_label.setStyleSheet("color: #64748b; font-size: 12px;")
            help_label.setWordWrap(True)
            help_layout.addWidget(help_label)
            
        card.layout().addLayout(help_layout)
        return card
        
    def create_status_bar(self) -> QWidget:
        """创建状态栏"""
        status_bar = QWidget()
        status_bar.setFixedHeight(50)
        status_bar.setObjectName("statusBar")
        status_bar.setStyleSheet("""
            QWidget#statusBar {
                background-color: #ffffff;
                border-top: 1px solid #e2e8f0;
            }
        """)
        
        layout = QHBoxLayout(status_bar)
        layout.setContentsMargins(25, 0, 25, 0)
        layout.setSpacing(10)
        
        # 状态信息
        self.status_label = QLabel("就绪")
        self.status_label.setStyleSheet("""
            color: #64748b;
            font-size: 13px;
            font-weight: 500;
        """)
        layout.addWidget(self.status_label)
        
        layout.addStretch()
        
        # 进度条
        self.status_progress = ModernProgressBar()
        self.status_progress.setVisible(False)
        self.status_progress.setFixedWidth(200)
        layout.addWidget(self.status_progress)
        
        return status_bar
        
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
            self.content_stack.setCurrentIndex(index)
            
            # 更新状态栏
            page_titles = {
                "component": "元件转换 - 添加和管理元器件",
                "history": "转换历史 - 查看转换记录",
                "settings": "设置 - 配置应用程序选项",
                "about": "关于 - 了解应用程序信息"
            }
            self.status_label.setText(page_titles.get(page_name, "就绪"))
            
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
        
    # 快速操作槽函数
    def new_conversion(self):
        """新建转换"""
        self.switch_page("component")
        self.status_label.setText("🆕 新建转换任务")
        
    def open_bom(self):
        """打开BOM文件"""
        self.status_label.setText("📁 选择BOM文件...")
        
    def save_project(self):
        """保存项目"""
        self.status_label.setText("💾 项目保存成功")
        
    def batch_process(self):
        """批量处理"""
        self.status_label.setText("🔄 批量处理模式")
        
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


# 导入进度条组件
from utils.ui_effects import ModernProgressBar