#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
现代化主窗口 - 彻底解决布局拥挤和覆盖问题
采用的空间分配和视觉层次设计
"""

import sys
# 修复相对导入问题
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from pathlib import Path
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                           QPushButton, QLabel, QStackedWidget,
                           QScrollArea, QSizePolicy, QMenuBar)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtSignal
from utils.config_manager import ConfigManager
from utils.modern_style import ModernStyle
from widgets.optimized_component_input_widget import OptimizedComponentInputWidget
from utils.ui_effects import ModernProgressBar
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
        self.setWindowTitle("EasyKiConverter - EDA转换工具")
        
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
        """设置用户界面 - Web风格，无状态栏"""
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局 - 垂直布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 主内容区域 - Web风格布局
        content_area = self.create_professional_content_area()
        main_layout.addWidget(content_area, 1)  # 添加拉伸因子
        
        # 移除状态栏 - 统计信息将在转换后显示
        # self.status_bar = self.create_professional_status_bar()
        # main_layout.addWidget(self.status_bar)
        
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
        
        app_subtitle = QLabel("EDA转换工具")
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
        """创建内容区域 - 纯Web风格布局（无导航栏）"""
        content_area = QWidget()
        content_area.setObjectName("professionalContentArea")
        content_area.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        layout = QVBoxLayout(content_area)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 顶部菜单栏 - Web风格
        self.top_menu_bar = self.create_web_style_menu_bar()
        layout.addWidget(self.top_menu_bar)
        
        # 主内容区域 - 单栏布局（仅中央工作区）
        self.main_workspace = self.create_professional_main_workspace()
        layout.addWidget(self.main_workspace, 1)  # 添加拉伸因子
        
        return content_area
        
    # 移除了 create_professional_sidebar 方法 - 不再需要导航栏
        
    def create_professional_main_workspace(self) -> QWidget:
        """创建主工作区 - 简化Web风格核心功能区域"""
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
        scroll_layout.setContentsMargins(40, 40, 40, 40)
        scroll_layout.setSpacing(35)
        
        # 主要内容区域（包含欢迎页面和转换界面）
        main_content = self.create_professional_main_content()
        scroll_layout.addWidget(main_content, 1)
        
        # 转换统计信息 - 初始隐藏，转换后显示
        self.conversion_stats_widget = self.create_conversion_stats_widget()
        scroll_layout.addWidget(self.conversion_stats_widget)
        
        scroll_area.setWidget(scroll_content)
        layout.addWidget(scroll_area)
        
        return workspace
        
    # 移除了 create_simplified_welcome_page 方法 - 不再需要欢迎页
        
    def create_professional_main_content(self) -> QWidget:
        """创建主内容区域 - 直接显示转换界面"""
        content = QWidget()
        content.setObjectName("professionalMainContent")
        content.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        # 使用更合理的布局结构
        layout = QVBoxLayout(content)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(30)  # 间距
        
        # 创建堆栈式内容区域
        self.content_stack = QStackedWidget()
        self.content_stack.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        # 直接创建组件输入界面作为默认页面
        self.component_widget = OptimizedComponentInputWidget(self.config_manager)
        self.content_stack.addWidget(self.component_widget)
        
        # 添加其他页面的占位符
        for i, (title, description, icon) in enumerate([
            ("转换历史", "查看和管理您的转换记录", "📊"),
            ("设置", "配置应用程序选项", "⚙️"),
            ("关于", "了解应用程序信息", "ℹ️")
        ]):
            placeholder = self.create_professional_placeholder_page(title, description, icon)
            self.content_stack.addWidget(placeholder)
            
        layout.addWidget(self.content_stack)
        
        # 默认直接显示转换界面
        self.content_stack.setCurrentIndex(0)
        
        return content
        
    def create_professional_placeholder_page(self, title: str, description: str, icon: str) -> QWidget:
        """创建占位符页面 - 美观的提示"""
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
        
    def create_web_style_menu_bar(self) -> QMenuBar:
        """创建Web风格的顶部菜单栏"""
        menu_bar = QMenuBar()
        menu_bar.setObjectName("webStyleMenuBar")
        menu_bar.setStyleSheet("""
            QMenuBar#webStyleMenuBar {
                background-color: #ffffff;
                border-bottom: 1px solid #e2e8f0;
                padding: 8px 20px;
                font-size: 14px;
                font-weight: 500;
            }
            QMenuBar::item {
                background-color: transparent;
                color: #475569;
                padding: 8px 16px;
                margin: 0 4px;
                border-radius: 6px;
            }
            QMenuBar::item:selected {
                background-color: #f1f5f9;
                color: #1e293b;
            }
            QMenuBar::item:pressed {
                background-color: #e2e8f0;
            }
        """)
        
        # 文件菜单 - 简化菜单结构
        file_menu = menu_bar.addMenu("文件")
        file_menu.addAction("新建转换", lambda: self.switch_page("component"))
        file_menu.addAction("打开BOM文件", self.open_bom)
        file_menu.addAction("保存项目", self.save_project)
        file_menu.addSeparator()
        file_menu.addAction("退出", self.close)
        
        # 帮助菜单 - 保留核心帮助功能
        help_menu = menu_bar.addMenu("帮助")
        help_menu.addAction("使用指南", self.show_help)
        help_menu.addAction("关于软件", lambda: self.switch_page("about"))
        
        return menu_bar
        
    # 移除右侧面板相关方法，改为统计信息显示在转换后
    def create_conversion_stats_widget(self) -> QWidget:
        """创建转换统计信息组件 - 在转换后显示"""
        stats_widget = QWidget()
        stats_widget.setObjectName("conversionStatsWidget")
        stats_widget.setVisible(False)  # 初始隐藏
        stats_widget.setStyleSheet("""
            QWidget#conversionStatsWidget {
                background-color: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 12px;
                padding: 20px;
                margin: 20px 40px;
            }
        """)
        
        layout = QHBoxLayout(stats_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(30)
        
        # 统计信息
        stats = [
            ("总转换次数", "0", "#2563eb"),
            ("成功次数", "0", "#10b981"),
            ("失败次数", "0", "#ef4444"),
            ("平均用时", "0s", "#f59e0b")
        ]
        
        self.stats_labels = {}
        for label, value, color in stats:
            stat_container = QWidget()
            stat_layout = QVBoxLayout(stat_container)
            stat_layout.setContentsMargins(0, 0, 0, 0)
            stat_layout.setSpacing(5)
            
            stat_value = QLabel(value)
            stat_value.setStyleSheet(f"""
                color: {color};
                font-size: 24px;
                font-weight: 700;
            """)
            stat_value.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            stat_label = QLabel(label)
            stat_label.setStyleSheet("""
                color: #64748b;
                font-size: 14px;
                font-weight: 500;
            """)
            stat_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            stat_layout.addWidget(stat_value)
            stat_layout.addWidget(stat_label)
            
            layout.addWidget(stat_container)
            self.stats_labels[label] = stat_value
            
        return stats_widget
        
    def create_professional_status_bar(self) -> QWidget:
        """创建状态栏 - 充足的信息展示空间"""
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
        """应用样式"""
        self.setStyleSheet(ModernStyle.get_main_stylesheet(self.current_theme))
        
    def setup_animations(self):
        """设置动画效果"""
        # 页面切换动画
        self.page_animation = QPropertyAnimation(self.content_stack, b"pos")
        self.page_animation.setDuration(300)
        self.page_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        
    def setup_connections(self):
        """设置信号连接"""
        # 连接组件转换信号以显示统计信息
        if hasattr(self, 'component_widget'):
            self.component_widget.conversion_completed.connect(self.on_conversion_completed)
        
    def switch_page(self, page_name: str):
        """切换页面 - 更新页面映射（移除欢迎页）"""
        # 页面映射（转换界面为索引0）
        page_map = {
            "component": 0,
            "history": 1,
            "settings": 2,
            "about": 3
        }
        
        if page_name in page_map:
            index = page_map[page_name]
            self.content_stack.setCurrentIndex(index)
            
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
        """应用响应式布局 - 简化版本"""
        # 简化响应式布局，不再处理侧边栏和右侧面板
        pass
            
    # 快速操作槽函数
    def new_conversion(self):
        """新建转换"""
        self.switch_page("component")
        
    def open_bom(self):
        """打开BOM文件"""
        # 状态显示已移除，直接调用组件界面的方法
        if hasattr(self, 'component_widget'):
            self.component_widget.import_bom()
        
    def save_project(self):
        """保存项目"""
        # 状态显示已移除，可添加实际保存逻辑
        pass
        
    # 移除了不需要的菜单方法：batch_process, open_bom_parser, open_component_validator
        
    def show_help(self):
        """显示帮助"""
        # 状态显示已移除，可添加帮助逻辑
        self.show_conversion_stats("使用指南", "0", "0", "0s")
        
    def on_conversion_completed(self, total, success, failed, avg_time):
        """转换完成回调 - 显示统计信息"""
        self.show_conversion_stats(total, success, failed, avg_time)
        
    def show_conversion_stats(self, total="0", success="0", failed="0", avg_time="0s"):
        """显示转换统计信息"""
        if hasattr(self, 'conversion_stats_widget'):
            self.conversion_stats_widget.setVisible(True)
            if hasattr(self, 'stats_labels'):
                self.stats_labels["总转换次数"].setText(total)
                self.stats_labels["成功次数"].setText(success)
                self.stats_labels["失败次数"].setText(failed)
                self.stats_labels["平均用时"].setText(avg_time)
        
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