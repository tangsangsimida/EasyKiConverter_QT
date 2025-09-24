#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
现代化主窗口 - 彻底解决布局拥挤和覆盖问题
采用专业级的空间分配和视觉层次设计
"""

import sys
# 修复相对导入问题
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from pathlib import Path
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                           QPushButton, QLabel, QFrame, QStackedWidget,
                           QSplitter, QScrollArea, QSizePolicy)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtSignal
from utils.config_manager import ConfigManager
from utils.modern_style import ModernStyle
from widgets.optimized_component_input_widget import OptimizedComponentInputWidget
from utils.ui_effects import ModernCard, ModernProgressBar
from utils.responsive_layout import ResponsiveLayoutManager, AdaptiveWidget


class UltimateMainWindow(QMainWindow, AdaptiveWidget):
    """现代化主窗口"""
    
    # 信号定义
    theme_changed = pyqtSignal(str)
    
    def __init__(self, config_manager: ConfigManager, parent=None):
        QMainWindow.__init__(self, parent)
        AdaptiveWidget.__init__(self, parent)
        
        self.config_manager = config_manager
        self.current_theme = "light"
        self.animation_enabled = True
        self.layout_manager = ResponsiveLayoutManager(self)
        
        self.setup_window()
        self.setup_ui()
        self.setup_animations()
        self.setup_connections()
        self.load_settings()
        
    def setup_window(self):
        """设置窗口属性 - 优化最大化兼容性"""
        self.setWindowTitle("EasyKiConverter - 专业级EDA转换工具")
        
        # 问题：最小尺寸限制会干扰最大化功能
        # 解决方案：使用更合理的尺寸策略
        # 设置推荐尺寸而不是强制最小尺寸
        self.resize(1800, 1200)  # 默认尺寸
        
        # 设置一个合理的最小尺寸，但不要过大
        # 避免设置超过常见屏幕尺寸的最小值
        self.setMinimumSize(1200, 800)  # 减小最小尺寸要求
        
        # 使用系统默认标题栏，不移除任何窗口装饰
        self.setWindowFlags(Qt.WindowType.Window)  # 标准窗口
        
    def setup_ui(self):
        """设置用户界面 - 使用系统标题栏，简化布局"""
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局 - 垂直布局，直接使用系统标题栏
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 直接使用系统标题栏，不需要自定义标题栏
        # 系统会提供标准的标题栏、最小化/最大化/关闭按钮
        
        # 主内容区域 - 专业级分割布局
        content_area = self.create_professional_content_area()
        main_layout.addWidget(content_area, 1)  # 添加拉伸因子
        
        # 状态栏 - 固定高度
        self.status_bar = self.create_professional_status_bar()
        main_layout.addWidget(self.status_bar)
        
        # 应用样式
        self.apply_professional_style()
        
    def create_professional_title_bar(self) -> QWidget:
        """创建简洁的标题栏 - 与系统标题栏协调"""
        title_bar = QWidget()
        title_bar.setFixedHeight(50)  # 更简洁的高度
        title_bar.setObjectName("professionalTitleBar")
        title_bar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        
        layout = QHBoxLayout(title_bar)
        layout.setContentsMargins(15, 0, 15, 0)  # 更紧凑的边距
        layout.setSpacing(10)
        
        # 左侧品牌区域
        brand_container = QWidget()
        brand_layout = QHBoxLayout(brand_container)
        brand_layout.setContentsMargins(0, 0, 0, 0)
        brand_layout.setSpacing(8)
        
        # 应用图标
        app_icon = QLabel("⚡")
        app_icon.setObjectName("professionalAppIcon")
        app_icon.setStyleSheet("""
            QLabel#professionalAppIcon {
                font-size: 20px;
                font-weight: bold;
                color: white;
                background-color: #2563eb;
                border-radius: 10px;
                padding: 6px;
                min-width: 20px;
                min-height: 20px;
                qproperty-alignment: AlignCenter;
            }
        """)
        brand_layout.addWidget(app_icon)
        
        # 品牌文字
        brand_text = QWidget()
        text_layout = QVBoxLayout(brand_text)
        text_layout.setContentsMargins(0, 0, 0, 0)
        text_layout.setSpacing(1)
        
        app_title = QLabel("EasyKiConverter")
        app_title.setObjectName("professionalAppTitle")
        app_title.setStyleSheet("""
            QLabel#professionalAppTitle {
                font-size: 16px;
                font-weight: 600;
                color: #1e293b;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
        """)
        text_layout.addWidget(app_title)
        
        app_subtitle = QLabel("专业级EDA转换工具")
        app_subtitle.setStyleSheet("""
            font-size: 11px;
            color: #64748b;
            font-weight: 400;
        """)
        text_layout.addWidget(app_subtitle)
        
        brand_layout.addWidget(brand_text)
        layout.addWidget(brand_container)
        
        layout.addStretch()
        
        # 右侧控制区域 - 仅保留主题切换
        control_container = QWidget()
        control_layout = QHBoxLayout(control_container)
        control_layout.setContentsMargins(0, 0, 0, 0)
        control_layout.setSpacing(6)
        
        # 主题切换按钮
        self.theme_button = QPushButton("🌙")
        self.theme_button.setObjectName("professionalThemeButton")
        self.theme_button.setFixedSize(32, 32)
        self.theme_button.setStyleSheet("""
            QPushButton#professionalThemeButton {
                background-color: transparent;
                border: none;
                border-radius: 16px;
                font-size: 16px;
                color: #64748b;
            }
            QPushButton#professionalThemeButton:hover {
                background-color: #f1f5f9;
                color: #2563eb;
            }
        """)
        self.theme_button.clicked.connect(self.toggle_theme)
        control_layout.addWidget(self.theme_button)
        
        layout.addWidget(control_container)
        
        # 设置标题栏样式
        title_bar.setStyleSheet("""
            QWidget#professionalTitleBar {
                background-color: #f8fafc;
                border-bottom: 1px solid #e2e8f0;
            }
        """)
        
        # 实现窗口拖动功能
        def mousePressEvent(event):
            if event.button() == Qt.MouseButton.LeftButton:
                self.drag_position = event.globalPosition().toPoint()
                event.accept()
        
        def mouseMoveEvent(event):
            if event.buttons() == Qt.MouseButton.LeftButton and hasattr(self, 'drag_position'):
                # 使用系统API移动窗口
                self.window().windowHandle().startSystemMove()
                event.accept()
        
        title_bar.mousePressEvent = mousePressEvent
        title_bar.mouseMoveEvent = mouseMoveEvent
        
        return title_bar
        
    def create_professional_content_area(self) -> QWidget:
        """创建专业级内容区域 - 合理的空间分配"""
        content_area = QWidget()
        content_area.setObjectName("professionalContentArea")
        content_area.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        layout = QHBoxLayout(content_area)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 使用分割器创建三栏布局
        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        main_splitter.setHandleWidth(2)  # 细分割条
        main_splitter.setStyleSheet("""
            QSplitter::handle {
                background-color: #f1f5f9;
                margin: 0;
            }
            QSplitter::handle:hover {
                background-color: #e2e8f0;
            }
        """)
        
        # 左侧导航栏 - 固定宽度，专业级设计
        self.sidebar = self.create_professional_sidebar()
        main_splitter.addWidget(self.sidebar)
        
        # 中间主工作区 - 主要空间
        self.main_workspace = self.create_professional_main_workspace()
        main_splitter.addWidget(self.main_workspace)
        
        # 右侧辅助面板 - 固定宽度
        self.side_panel = self.create_professional_side_panel()
        main_splitter.addWidget(self.side_panel)
        
        # 设置合理的分割比例和最小尺寸
        main_splitter.setSizes([280, 1200, 320])  # 优化比例：导航栏更小，主工作区更大
        main_splitter.setStretchFactor(0, 0)  # 导航栏不拉伸
        main_splitter.setStretchFactor(1, 1)  # 主工作区拉伸
        main_splitter.setStretchFactor(2, 0)  # 辅助面板不拉伸
        
        # 设置最小尺寸防止过度压缩
        self.sidebar.setMinimumWidth(280)
        self.sidebar.setMaximumWidth(350)
        self.side_panel.setMinimumWidth(380)
        self.side_panel.setMaximumWidth(450)
        
        layout.addWidget(main_splitter)
        
        return content_area
        
    def create_professional_sidebar(self) -> QWidget:
        """创建专业级侧边栏 - 充足的空间和层次"""
        sidebar = QWidget()
        sidebar.setObjectName("professionalSidebar")
        sidebar.setMinimumWidth(300)  # 增加最小宽度
        sidebar.setMaximumWidth(380)  # 增加最大宽度
        sidebar.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sidebar.setStyleSheet("""
            QWidget#professionalSidebar {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                          stop:0 #1e293b, 
                                          stop:1 #334155);
                border-right: none;
            }
        """)
        
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(0, 30, 0, 30)  # 增加上下边距
        layout.setSpacing(25)  # 增加组件间距
        
        # Logo区域 - 更大的视觉元素
        logo_container = QWidget()
        logo_layout = QVBoxLayout(logo_container)
        logo_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # 更大的Logo
        logo_label = QLabel("⚡")
        logo_label.setStyleSheet("""
            color: white;
            font-size: 56px;
            font-weight: bold;
            background-color: rgba(255, 255, 255, 0.1);
            border-radius: 28px;
            padding: 20px;
            margin: 20px;
            min-width: 56px;
            min-height: 56px;
            qproperty-alignment: AlignCenter;
        """)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_layout.addWidget(logo_label)
        
        # 更大的应用名称
        app_name = QLabel("EasyKi\nConverter")
        app_name.setStyleSheet("""
            color: white;
            font-size: 24px;
            font-weight: 600;
            text-align: center;
            background: transparent;
            padding: 15px;
        """)
        app_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_layout.addWidget(app_name)
        
        layout.addWidget(logo_container)
        
        # 导航菜单 - 更大的按钮和间距
        nav_container = QWidget()
        nav_layout = QVBoxLayout(nav_container)
        nav_layout.setSpacing(10)  # 增加按钮间距
        
        nav_items = [
            ("🏠", "元件转换", "component"),
            ("📊", "转换历史", "history"), 
            ("⚙️", "设置", "settings"),
            ("ℹ️", "关于", "about")
        ]
        
        self.nav_buttons = {}
        for icon, text, name in nav_items:
            btn = QPushButton(f"{icon}  {text}")
            btn.setObjectName(f"professionalNav_{name}")
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: #cbd5e1;
                    border: none;
                    border-radius: 16px;
                    padding: 20px 25px;
                    font-size: 16px;
                    font-weight: 500;
                    text-align: left;
                    margin: 4px 20px;
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
        
        # 用户信息区域 - 更大的用户区域
        user_container = QWidget()
        user_layout = QHBoxLayout(user_container)
        user_layout.setContentsMargins(25, 20, 25, 20)  # 增加边距
        
        user_avatar = QLabel("👤")
        user_avatar.setStyleSheet("""
            color: white;
            font-size: 24px;
            background-color: rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 12px;
            min-width: 40px;
            min-height: 40px;
            qproperty-alignment: AlignCenter;
        """)
        user_layout.addWidget(user_avatar)
        
        user_info = QWidget()
        user_info_layout = QVBoxLayout(user_info)
        user_info_layout.setContentsMargins(0, 0, 0, 0)
        user_info_layout.setSpacing(4)  # 增加行间距
        
        user_name = QLabel("用户")
        user_name.setStyleSheet("""
            color: white;
            font-size: 16px;
            font-weight: 500;
        """)
        user_info_layout.addWidget(user_name)
        
        user_status = QLabel("在线")
        user_status.setStyleSheet("""
            color: #10b981;
            font-size: 14px;
        """)
        user_info_layout.addWidget(user_status)
        
        user_layout.addWidget(user_info)
        user_layout.addStretch()
        
        layout.addWidget(user_container)
        
        return sidebar
        
    def create_professional_main_workspace(self) -> QWidget:
        """创建专业级主工作区 - 核心功能区域"""
        workspace = QWidget()
        workspace.setObjectName("professionalMainWorkspace")
        workspace.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        workspace.setStyleSheet("""
            QWidget#professionalMainWorkspace {
                background-color: #f8fafc;
            }
        """)
        
        layout = QVBoxLayout(workspace)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 创建滚动区域以支持内容溢出
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #f8fafc;
            }
            QScrollBar:vertical {
                background-color: #f1f5f9;
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background-color: #cbd5e1;
                border-radius: 5px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #94a3b8;
            }
        """)
        
        # 创建滚动内容
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(40, 40, 40, 40)  # 充足的内边距
        scroll_layout.setSpacing(35)  # 专业级组件间距
        
        # 欢迎区域 - 更大的视觉冲击力
        welcome_area = self.create_professional_welcome_area()
        scroll_layout.addWidget(welcome_area)
        
        # 主要内容区域 - 合理的空间分配
        main_content = self.create_professional_main_content()
        scroll_layout.addWidget(main_content, 1)  # 添加拉伸因子
        
        scroll_area.setWidget(scroll_content)
        layout.addWidget(scroll_area)
        
        return workspace
        
    def create_professional_welcome_area(self) -> QWidget:
        """创建专业级欢迎区域 - 强烈的视觉层次"""
        welcome = QWidget()
        welcome.setObjectName("professionalWelcomeArea")
        welcome.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        
        # 使用卡片式设计
        card = QFrame()
        card.setObjectName("welcomeCard")
        card.setStyleSheet("""
            QFrame#welcomeCard {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                          stop:0 #2563eb, 
                                          stop:1 #3b82f6);
                border-radius: 24px;
                padding: 40px;
            }
        """)
        
        # 添加专业级阴影效果
        from utils.modern_style import ModernStyle
        ModernStyle.add_shadow_effect(card, blur_radius=40, offset=(0, 12))
        
        layout = QHBoxLayout(card)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(40)  # 充足的间距
        
        # 左侧文字区域 - 更大的字体和间距
        text_container = QWidget()
        text_layout = QVBoxLayout(text_container)
        text_layout.setContentsMargins(0, 0, 0, 0)
        text_layout.setSpacing(20)  # 增加行间距
        
        # 主标题 - 更大字体
        main_title = QLabel("欢迎使用 EasyKiConverter")
        main_title.setStyleSheet("""
            font-size: 32px;
            font-weight: 700;
            color: white;
            margin-bottom: 12px;
        """)
        text_layout.addWidget(main_title)
        
        # 副标题 - 更大字体
        subtitle = QLabel("专业级嘉立创EDA转KiCad转换工具")
        subtitle.setStyleSheet("""
            font-size: 18px;
            color: rgba(255, 255, 255, 0.9);
            margin-bottom: 20px;
        """)
        text_layout.addWidget(subtitle)
        
        # 功能特点 - 更大字体
        features = QLabel("✨ 完整转换 • 🚀 批量处理 • 🎯 精准识别 • 🎨 现代化界面")
        features.setStyleSheet("""
            font-size: 16px;
            color: rgba(255, 255, 255, 0.8);
            line-height: 28px;
        """)
        text_layout.addWidget(features)
        
        layout.addWidget(text_container)
        layout.addStretch()
        
        # 右侧装饰图标 - 更大尺寸
        icon_label = QLabel("⚡")
        icon_label.setStyleSheet("""
            font-size: 80px;
            color: rgba(255, 255, 255, 0.2);
            background: transparent;
        """)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon_label)
        
        # 外层容器用于添加外边距
        outer_container = QWidget()
        outer_layout = QVBoxLayout(outer_container)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.addWidget(card)
        
        return outer_container
        
    def create_professional_main_content(self) -> QWidget:
        """创建专业级主内容区域 - 核心功能"""
        content = QWidget()
        content.setObjectName("professionalMainContent")
        content.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        # 使用更合理的布局结构
        layout = QVBoxLayout(content)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(30)  # 专业级间距
        
        # 创建堆栈式内容区域
        self.content_stack = QStackedWidget()
        self.content_stack.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        # 创建专业级组件输入界面
        self.component_widget = OptimizedComponentInputWidget(self.config_manager)
        self.content_stack.addWidget(self.component_widget)
        
        # 添加其他页面的占位符 - 更美观的设计
        for i, (title, description, icon) in enumerate([
            ("转换历史", "查看和管理您的转换记录", "📊"),
            ("设置", "配置应用程序选项", "⚙️"),
            ("关于", "了解应用程序信息", "ℹ️")
        ]):
            placeholder = self.create_professional_placeholder_page(title, description, icon)
            self.content_stack.addWidget(placeholder)
            
        layout.addWidget(self.content_stack)
        
        return content
        
    def create_professional_placeholder_page(self, title: str, description: str, icon: str) -> QWidget:
        """创建专业级占位符页面 - 美观的提示"""
        page = QWidget()
        page.setObjectName("professionalPlaceholderPage")
        
        layout = QVBoxLayout(page)
        layout.setContentsMargins(60, 60, 60, 60)  # 充足的内边距
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # 更大的图标
        icon_label = QLabel(icon)
        icon_label.setStyleSheet("""
            font-size: 80px;
            color: #cbd5e1;
            margin-bottom: 30px;
        """)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon_label)
        
        # 更大的标题
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            font-size: 28px;
            font-weight: 600;
            color: #64748b;
            margin-bottom: 15px;
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # 更大的描述
        desc_label = QLabel(description)
        desc_label.setStyleSheet("""
            font-size: 18px;
            color: #94a3b8;
            text-align: center;
            max-width: 400px;
        """)
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)
        
        layout.addStretch()
        
        return page
        
    def create_professional_side_panel(self) -> QWidget:
        """创建专业级侧面板 - 辅助功能区域"""
        panel = QWidget()
        panel.setObjectName("professionalSidePanel")
        panel.setMinimumWidth(420)  # 增加最小宽度
        panel.setMaximumWidth(500)  # 增加最大宽度
        panel.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        panel.setStyleSheet("""
            QWidget#professionalSidePanel {
                background-color: #ffffff;
                border-left: 1px solid #f1f5f9;
            }
        """)
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(30, 40, 30, 30)  # 增加内边距
        layout.setSpacing(30)  # 专业级间距
        
        # 快速操作区域 - 更大的卡片
        quick_actions = self.create_professional_quick_actions()
        layout.addWidget(quick_actions)
        
        # 统计信息区域 - 更大的卡片
        stats_area = self.create_professional_stats_area()
        layout.addWidget(stats_area)
        
        # 帮助信息区域 - 更大的卡片
        help_area = self.create_professional_help_area()
        layout.addWidget(help_area)
        
        layout.addStretch()
        
        return panel
        
    def create_professional_quick_actions(self) -> QWidget:
        """创建专业级快速操作区域"""
        card = ModernCard(
            title="快速操作",
            icon="⚡",
            description="常用功能的快捷入口"
        )
        
        # 添加更大的操作按钮
        actions_layout = QVBoxLayout()
        actions_layout.setSpacing(12)  # 增加按钮间距
        
        actions = [
            ("📋 新建转换", self.new_conversion),
            ("📁 打开BOM", self.open_bom),
            ("💾 保存项目", self.save_project),
            ("🔄 批量处理", self.batch_process)
        ]
        
        for text, callback in actions:
            btn = QPushButton(text)
            btn.setMinimumHeight(48)  # 增加按钮高度
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #f8fafc;
                    color: #475569;
                    border: 1px solid #e2e8f0;
                    border-radius: 12px;
                    padding: 14px 18px;
                    font-size: 14px;
                    font-weight: 500;
                    text-align: left;
                }
                QPushButton:hover {
                    background-color: #f1f5f9;
                    color: #1e293b;
                    border-color: #cbd5e1;
                }
            """)
            btn.clicked.connect(callback)
            actions_layout.addWidget(btn)
            
        card.layout().addLayout(actions_layout)
        return card
        
    def create_professional_stats_area(self) -> QWidget:
        """创建专业级统计信息区域"""
        card = ModernCard(
            title="统计信息",
            icon="📊",
            description="转换数据统计"
        )
        
        # 添加更大的统计信息
        stats_layout = QVBoxLayout()
        stats_layout.setSpacing(12)  # 增加间距
        
        stats = [
            ("总转换次数", "0"),
            ("成功次数", "0"),
            ("失败次数", "0"),
            ("平均用时", "0s")
        ]
        
        for label, value in stats:
            stat_layout = QHBoxLayout()
            stat_label = QLabel(label)
            stat_label.setStyleSheet("color: #64748b; font-size: 14px; font-weight: 500;")
            stat_value = QLabel(value)
            stat_value.setStyleSheet("color: #1e293b; font-size: 14px; font-weight: 600;")
            
            stat_layout.addWidget(stat_label)
            stat_layout.addStretch()
            stat_layout.addWidget(stat_value)
            stats_layout.addLayout(stat_layout)
            
        card.layout().addLayout(stats_layout)
        return card
        
    def create_professional_help_area(self) -> QWidget:
        """创建专业级帮助信息区域"""
        card = ModernCard(
            title="使用帮助",
            icon="💡",
            description="快速入门指南"
        )
        
        # 添加更大的帮助信息
        help_layout = QVBoxLayout()
        help_layout.setSpacing(10)  # 增加间距
        
        help_items = [
            "📝 支持LCSC编号：C2040、C123456",
            "🔧 支持元件型号：ESP32、STM32F103",
            "📋 可批量导入BOM文件",
            "🎯 支持符号、封装、3D模型导出"
        ]
        
        for item in help_items:
            help_label = QLabel(item)
            help_label.setStyleSheet("color: #0c4a6e; font-size: 13px; font-weight: 500;")
            help_label.setWordWrap(True)
            help_layout.addWidget(help_label)
            
        card.layout().addLayout(help_layout)
        return card
        
    def create_professional_status_bar(self) -> QWidget:
        """创建专业级状态栏 - 充足的信息展示空间"""
        status_bar = QWidget()
        status_bar.setFixedHeight(60)  # 增加高度
        status_bar.setObjectName("professionalStatusBar")
        status_bar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        status_bar.setStyleSheet("""
            QWidget#professionalStatusBar {
                background-color: #ffffff;
                border-top: 1px solid #f1f5f9;
            }
        """)
        
        layout = QHBoxLayout(status_bar)
        layout.setContentsMargins(30, 0, 30, 0)  # 增加边距
        layout.setSpacing(20)  # 增加间距
        
        # 状态信息 - 更大的字体
        self.status_label = QLabel("就绪")
        self.status_label.setStyleSheet("""
            color: #64748b;
            font-size: 14px;
            font-weight: 500;
        """)
        layout.addWidget(self.status_label)
        
        layout.addStretch()
        
        # 进度条 - 更大的尺寸
        self.status_progress = ModernProgressBar()
        self.status_progress.setVisible(False)
        self.status_progress.setFixedWidth(250)  # 增加宽度
        self.status_progress.setFixedHeight(10)  # 增加高度
        layout.addWidget(self.status_progress)
        
        return status_bar
        
    def apply_professional_style(self):
        """应用专业级样式"""
        self.setStyleSheet(ModernStyle.get_main_stylesheet(self.current_theme))
        
    def setup_animations(self):
        """设置动画效果"""
        # 页面切换动画
        self.page_animation = QPropertyAnimation(self.content_stack, b"pos")
        self.page_animation.setDuration(300)
        self.page_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        
    def setup_connections(self):
        """设置信号连接"""
        # 主题切换功能暂时移除，后续可以添加到菜单栏或工具栏
        # self.theme_button.clicked.connect(self.toggle_theme)
        pass
        
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
        self.apply_professional_style()
        
        # 更新主题按钮图标
        icon = "☀️" if self.current_theme == "dark" else "🌙"
        self.theme_button.setText(icon)
        
        self.theme_changed.emit(self.current_theme)
        
    def toggle_maximized(self):
        """切换最大化状态 - 使用系统默认行为"""
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()
        # 移除对自定义max_button的引用，使用系统按钮
            
    def load_settings(self):
        """加载设置"""
        config = self.config_manager.get_config()
        if 'theme' in config:
            self.current_theme = config['theme']
            self.apply_professional_style()
            
    def save_settings(self):
        """保存设置"""
        config = self.config_manager.get_config()
        config['theme'] = self.current_theme
        self.config_manager.save_config(config)
        
    def resizeEvent(self, event):
        """重写大小改变事件 - 响应式布局"""
        super().resizeEvent(event)
        self.layout_manager.on_resize()
        
    def apply_responsive_layout(self, mode):
        """应用响应式布局 - 移除标题栏引用"""
        sizes = self.layout_manager.get_recommended_sizes(mode)
        
        # 根据模式调整布局
        if mode == "mobile":
            # 移动端：隐藏侧边栏，简化布局
            self.sidebar.setVisible(False)
            self.side_panel.setVisible(False)
        elif mode == "tablet":
            # 平板端：调整尺寸
            self.sidebar.setFixedWidth(sizes['sidebar_width'])
            self.side_panel.setFixedWidth(sizes['side_panel_width'])
            # 移除标题栏引用，使用系统标题栏
            self.status_bar.setFixedHeight(sizes['status_height'])
        else:
            # 桌面端：标准尺寸
            self.sidebar.setFixedWidth(sizes['sidebar_width'])
            self.side_panel.setFixedWidth(sizes['side_panel_width'])
            # 移除标题栏引用，使用系统标题栏
            self.status_bar.setFixedHeight(sizes['status_height'])
            
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