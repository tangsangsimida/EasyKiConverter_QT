#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
现代化主窗口 - 酷炫界面设计
采用从上至下的清晰布局，现代化UI元素
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                           QPushButton, QLabel, QFrame, QStackedWidget,
                           QScrollArea, QSizePolicy, QMenuBar, QMenu, QGraphicsDropShadowEffect,
                           QListWidget, QListWidgetItem, QLineEdit, QCheckBox, QFileDialog, QMessageBox,
                           QApplication)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtSignal, QPoint
from PyQt6.QtGui import QLinearGradient, QColor, QPalette, QPainter, QBrush, QPen

from utils.config_manager import ConfigManager
from widgets.optimized_component_input_widget import OptimizedComponentInputWidget
from utils.modern_ui_components import ModernCard, ModernProgressBar


class ModernMainWindow(QMainWindow):
    """现代化主窗口 - 酷炫界面"""
    
    def __init__(self, config_manager: ConfigManager, parent=None):
        super().__init__(parent)
        
        self.config_manager = config_manager
        self.animation_enabled = True
        
        self.setup_window()
        self.setup_ui()
        self.setup_animations()
        self.setup_connections()
        self.load_settings()
        
    def setup_window(self):
        """设置窗口属性"""
        self.setWindowTitle("EasyKiConverter - EDA转换工具")
        self.resize(1600, 1000)
        self.setMinimumSize(1200, 800)
        
        # 设置窗口样式
        self.setWindowFlags(Qt.WindowType.Window)
        
    def setup_ui(self):
        """设置用户界面"""
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局 - 垂直布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 顶部标题栏
        title_bar = self.create_modern_title_bar()
        main_layout.addWidget(title_bar)
        
        # 主内容区域
        content_area = self.create_modern_content_area()
        main_layout.addWidget(content_area, 1)
        
        # 应用样式
        self.apply_modern_style()
        
    def create_modern_title_bar(self) -> QWidget:
        """创建现代化标题栏"""
        title_bar = QWidget()
        title_bar.setFixedHeight(70)
        title_bar.setObjectName("modernTitleBar")
        
        # 创建渐变背景
        gradient = QLinearGradient(0, 0, title_bar.width(), title_bar.height())
        gradient.setColorAt(0, QColor("#667eea"))
        gradient.setColorAt(1, QColor("#764ba2"))
        
        layout = QHBoxLayout(title_bar)
        layout.setContentsMargins(30, 0, 30, 0)
        layout.setSpacing(20)
        
        # 左侧品牌区域
        brand_container = QWidget()
        brand_layout = QHBoxLayout(brand_container)
        brand_layout.setContentsMargins(0, 0, 0, 0)
        brand_layout.setSpacing(15)
        
        # 应用图标
        app_icon = QLabel("⚡")
        app_icon.setObjectName("appIcon")
        app_icon.setStyleSheet("""
            QLabel#appIcon {
                font-size: 32px;
                font-weight: bold;
                color: white;
                background-color: rgba(255, 255, 255, 0.2);
                border-radius: 15px;
                padding: 10px;
                min-width: 30px;
                min-height: 30px;
                qproperty-alignment: AlignCenter;
            }
        """)
        brand_layout.addWidget(app_icon)
        
        # 品牌文字
        brand_text = QWidget()
        text_layout = QVBoxLayout(brand_text)
        text_layout.setContentsMargins(0, 0, 0, 0)
        text_layout.setSpacing(2)
        
        app_title = QLabel("EasyKiConverter")
        app_title.setObjectName("appTitle")
        app_title.setStyleSheet("""
            QLabel#appTitle {
                font-size: 24px;
                font-weight: 700;
                color: white;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
        """)
        text_layout.addWidget(app_title)
        
        app_subtitle = QLabel("嘉立创EDA → KiCad 转换工具")
        app_subtitle.setStyleSheet("""
            font-size: 14px;
            color: rgba(255, 255, 255, 0.8);
            font-weight: 400;
        """)
        text_layout.addWidget(app_subtitle)
        
        brand_layout.addWidget(brand_text)
        layout.addWidget(brand_container)
        
        layout.addStretch()
        
        # 右侧控制区域（移除主题切换）
        control_container = QWidget()
        control_layout = QHBoxLayout(control_container)
        control_layout.setContentsMargins(0, 0, 0, 0)
        control_layout.setSpacing(10)
        
        layout.addWidget(control_container)
        
        # 设置标题栏样式
        title_bar.setStyleSheet("""
            QWidget#modernTitleBar {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #667eea, stop:1 #764ba2);
            }
        """)
        
        return title_bar
        
    def create_modern_content_area(self) -> QWidget:
        """创建现代化内容区域"""
        content_area = QWidget()
        content_area.setObjectName("modernContentArea")
        
        layout = QVBoxLayout(content_area)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 创建滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                background-color: #f8fafc;
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background-color: #cbd5e1;
                border-radius: 4px;
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
        scroll_layout.setSpacing(30)
        
        # 欢迎标题
        welcome_title = self.create_welcome_section()
        scroll_layout.addWidget(welcome_title)
        
        # 核心功能区域（使用卡片布局）
        
        # 1. 元件输入卡片
        input_card = self.create_input_card()
        scroll_layout.addWidget(input_card)
        
        # 2. BOM导入卡片
        bom_card = self.create_bom_card()
        scroll_layout.addWidget(bom_card)
        
        # 3. 元件列表卡片
        list_card = self.create_list_card()
        scroll_layout.addWidget(list_card)
        
        # 4. 导出选项卡片
        options_card = self.create_options_card()
        scroll_layout.addWidget(options_card)
        
        # 5. 输出设置卡片
        output_card = self.create_output_card()
        scroll_layout.addWidget(output_card)
        
        # 6. 转换执行卡片
        export_card = self.create_export_card()
        scroll_layout.addWidget(export_card)
        
        scroll_layout.addStretch()
        
        scroll_area.setWidget(scroll_content)
        layout.addWidget(scroll_area)
        
        return content_area
        
    def create_welcome_section(self) -> QWidget:
        """创建欢迎区域"""
        welcome = QWidget()
        welcome_layout = QVBoxLayout(welcome)
        welcome_layout.setContentsMargins(0, 0, 0, 20)
        welcome_layout.setSpacing(10)
        
        title = QLabel("🚀 开始您的EDA转换之旅")
        title.setStyleSheet("""
            font-size: 32px;
            font-weight: 700;
            color: #1e293b;
            text-align: center;
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome_layout.addWidget(title)
        
        subtitle = QLabel("输入嘉立创元器件编号，一键导出KiCad符号库、封装库和3D模型")
        subtitle.setStyleSheet("""
            font-size: 16px;
            color: #64748b;
            text-align: center;
        """)
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setWordWrap(True)
        welcome_layout.addWidget(subtitle)
        
        return welcome
        
    def create_input_card(self) -> ModernCard:
        """创建输入卡片"""
        card = ModernCard("📝 添加元器件", "输入嘉立创元器件编号或URL")
        
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # 输入区域
        input_layout = QHBoxLayout()
        input_layout.setSpacing(10)
        
        self.component_input = QLineEdit()
        self.component_input.setPlaceholderText("输入元器件编号，例如：C2040 或 https://item.szlcsc.com/12345.html")
        self.component_input.setClearButtonEnabled(True)
        self.component_input.setStyleSheet("""
            QLineEdit {
                padding: 15px 20px;
                border: 2px solid #e2e8f0;
                border-radius: 10px;
                font-size: 16px;
                min-height: 50px;
                background-color: #ffffff;
            }
            QLineEdit:focus {
                border-color: #667eea;
                outline: none;
            }
        """)
        input_layout.addWidget(self.component_input)
        
        # 添加按钮
        add_btn = QPushButton("添加")
        add_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #667eea, stop:1 #764ba2);
                color: white;
                border: none;
                padding: 15px 30px;
                border-radius: 10px;
                font-size: 16px;
                font-weight: 600;
                min-height: 50px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #5a67d8, stop:1 #6b46c1);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #4c51bf, stop:1 #553c9a);
            }
        """)
        add_btn.clicked.connect(self.add_component)
        input_layout.addWidget(add_btn)
        
        layout.addLayout(input_layout)
        
        # 快捷操作
        quick_actions = QHBoxLayout()
        quick_actions.setSpacing(10)
        
        paste_btn = QPushButton("📋 从剪贴板粘贴")
        paste_btn.setStyleSheet("""
            QPushButton {
                background-color: #f8fafc;
                color: #475569;
                border: 1px solid #e2e8f0;
                padding: 10px 20px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #f1f5f9;
                border-color: #cbd5e1;
            }
        """)
        paste_btn.clicked.connect(self.paste_from_clipboard)
        quick_actions.addWidget(paste_btn)
        
        quick_actions.addStretch()
        layout.addLayout(quick_actions)
        
        card.content_layout.addLayout(layout)
        return card
        
    def create_bom_card(self) -> ModernCard:
        """创建BOM导入卡片"""
        card = ModernCard("📊 BOM文件导入", "批量导入Excel或CSV格式的BOM文件")
        
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # 文件选择区域
        file_layout = QHBoxLayout()
        file_layout.setSpacing(10)
        
        self.bom_file_label = QLabel("未选择BOM文件")
        self.bom_file_label.setStyleSheet("color: #64748b; font-size: 14px;")
        file_layout.addWidget(self.bom_file_label)
        
        file_layout.addStretch()
        
        select_file_btn = QPushButton("选择BOM文件")
        select_file_btn.setStyleSheet("""
            QPushButton {
                background-color: #8b5cf6;
                color: white;
                border: none;
                padding: 12px 25px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #7c3aed;
            }
        """)
        select_file_btn.clicked.connect(self.select_bom_file)
        file_layout.addWidget(select_file_btn)
        
        layout.addLayout(file_layout)
        
        # BOM解析结果显示
        self.bom_result_label = QLabel("")
        self.bom_result_label.setStyleSheet("color: #10b981; font-size: 13px;")
        self.bom_result_label.setWordWrap(True)
        layout.addWidget(self.bom_result_label)
        
        card.content_layout.addLayout(layout)
        return card
        
    def create_list_card(self) -> ModernCard:
        """创建元件列表卡片"""
        card = ModernCard("📋 待转换列表", "已添加的元器件编号")
        
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # 列表头部
        header_layout = QHBoxLayout()
        
        self.component_count_label = QLabel("共 0 个元器件")
        self.component_count_label.setStyleSheet("color: #64748b; font-size: 16px; font-weight: 600;")
        header_layout.addWidget(self.component_count_label)
        
        header_layout.addStretch()
        
        # 清除按钮
        clear_btn = QPushButton("🗑️ 清除全部")
        clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #ef4444;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                font-size: 13px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #dc2626;
            }
        """)
        clear_btn.clicked.connect(self.clear_all_components)
        header_layout.addWidget(clear_btn)
        
        layout.addLayout(header_layout)
        
        # 元件列表
        self.component_list = QListWidget()
        self.component_list.setStyleSheet("""
            QListWidget {
                border: 2px solid #e2e8f0;
                border-radius: 10px;
                background-color: white;
                font-size: 15px;
                padding: 10px;
            }
            QListWidget::item {
                padding: 12px 15px;
                border-bottom: 1px solid #f1f5f9;
                border-radius: 6px;
                margin: 2px 0;
            }
            QListWidget::item:hover {
                background-color: #f8fafc;
            }
            QListWidget::item:selected {
                background-color: #667eea;
                color: white;
            }
        """)
        self.component_list.setFixedHeight(200)
        self.component_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.component_list.customContextMenuRequested.connect(self.show_component_menu)
        layout.addWidget(self.component_list)
        
        card.content_layout.addLayout(layout)
        return card
        
    def create_options_card(self) -> ModernCard:
        """创建导出选项卡片"""
        card = ModernCard("⚙️ 导出选项", "选择要导出的文件类型")
        
        layout = QHBoxLayout()
        layout.setSpacing(30)
        
        # 符号导出选项
        self.symbol_checkbox = QCheckBox("导出原理图符号 (.kicad_sym)")
        self.symbol_checkbox.setChecked(True)
        self.symbol_checkbox.setStyleSheet("""
            QCheckBox {
                font-size: 15px;
                font-weight: 500;
                color: #374151;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border-radius: 4px;
                border: 2px solid #d1d5db;
            }
            QCheckBox::indicator:checked {
                background-color: #667eea;
                border-color: #667eea;
            }
        """)
        self.symbol_checkbox.stateChanged.connect(self.update_export_options)
        layout.addWidget(self.symbol_checkbox)
        
        # 封装导出选项
        self.footprint_checkbox = QCheckBox("导出PCB封装 (.kicad_mod)")
        self.footprint_checkbox.setChecked(True)
        self.footprint_checkbox.setStyleSheet("""
            QCheckBox {
                font-size: 15px;
                font-weight: 500;
                color: #374151;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border-radius: 4px;
                border: 2px solid #d1d5db;
            }
            QCheckBox::indicator:checked {
                background-color: #667eea;
                border-color: #667eea;
            }
        """)
        self.footprint_checkbox.stateChanged.connect(self.update_export_options)
        layout.addWidget(self.footprint_checkbox)
        
        # 3D模型导出选项
        self.model3d_checkbox = QCheckBox("导出3D模型 (.step)")
        self.model3d_checkbox.setChecked(True)
        self.model3d_checkbox.setStyleSheet("""
            QCheckBox {
                font-size: 15px;
                font-weight: 500;
                color: #374151;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border-radius: 4px;
                border: 2px solid #d1d5db;
            }
            QCheckBox::indicator:checked {
                background-color: #667eea;
                border-color: #667eea;
            }
        """)
        self.model3d_checkbox.stateChanged.connect(self.update_export_options)
        layout.addWidget(self.model3d_checkbox)
        
        layout.addStretch()
        
        card.content_layout.addLayout(layout)
        return card
        
    def create_output_card(self) -> ModernCard:
        """创建输出设置卡片"""
        card = ModernCard("📁 输出设置", "自定义输出路径和库名称")
        
        layout = QVBoxLayout()
        layout.setSpacing(20)
        
        # 输出路径
        path_layout = QHBoxLayout()
        path_layout.setSpacing(10)
        
        path_label = QLabel("输出路径：")
        path_label.setStyleSheet("font-size: 15px; font-weight: 500; color: #374151; min-width: 80px;")
        path_layout.addWidget(path_label)
        
        self.output_path_input = QLineEdit()
        self.output_path_input.setPlaceholderText("留空将默认保存到工作区根目录的output文件夹")
        self.output_path_input.setClearButtonEnabled(True)
        self.output_path_input.setStyleSheet("""
            QLineEdit {
                padding: 12px 15px;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                font-size: 14px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #667eea;
                outline: none;
            }
        """)
        path_layout.addWidget(self.output_path_input)
        
        browse_btn = QPushButton("浏览...")
        browse_btn.setStyleSheet("""
            QPushButton {
                background-color: #6b7280;
                color: white;
                border: none;
                padding: 12px 20px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: 500;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #4b5563;
            }
        """)
        browse_btn.clicked.connect(self.browse_output_path)
        path_layout.addWidget(browse_btn)
        
        layout.addLayout(path_layout)
        
        # 库名称
        name_layout = QHBoxLayout()
        name_layout.setSpacing(10)
        
        name_label = QLabel("库名称：")
        name_label.setStyleSheet("font-size: 15px; font-weight: 500; color: #374151; min-width: 80px;")
        name_layout.addWidget(name_label)
        
        self.lib_name_input = QLineEdit()
        self.lib_name_input.setPlaceholderText("例如：my_project，留空默认为easyeda_convertlib")
        self.lib_name_input.setClearButtonEnabled(True)
        self.lib_name_input.setStyleSheet("""
            QLineEdit {
                padding: 12px 15px;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                font-size: 14px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #667eea;
                outline: none;
            }
        """)
        name_layout.addWidget(self.lib_name_input)
        
        name_layout.addStretch()
        
        layout.addLayout(name_layout)
        
        card.content_layout.addLayout(layout)
        return card
        
    def create_export_card(self) -> ModernCard:
        """创建转换执行卡片"""
        card = ModernCard("🚀 开始转换", "一键导出所有元器件库文件")
        
        layout = QVBoxLayout()
        layout.setSpacing(20)
        
        # 转换按钮
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.export_btn = QPushButton("开始导出")
        self.export_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #10b981, stop:1 #059669);
                color: white;
                border: none;
                padding: 18px 50px;
                border-radius: 12px;
                font-size: 20px;
                font-weight: 700;
                min-width: 200px;
                letter-spacing: 1px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #059669, stop:1 #047857);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #047857, stop:1 #065f46);
            }
            QPushButton:disabled {
                background: #9ca3af;
                color: #d1d5db;
            }
        """)
        self.export_btn.clicked.connect(self.request_export)
        button_layout.addWidget(self.export_btn)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        # 进度条（初始隐藏）
        self.progress_bar = ModernProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # 状态标签
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("""
            color: #6b7280;
            font-size: 14px;
            text-align: center;
        """)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)
        
        card.content_layout.addLayout(layout)
        return card
        
    def apply_modern_style(self):
        """应用现代化样式（固定浅色主题）"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f8fafc;
            }
            
            QWidget#modernContentArea {
                background-color: #f8fafc;
            }
            
            /* 卡片样式 */
            ModernCard {
                background-color: white;
                border-radius: 16px;
                border: 1px solid #e2e8f0;
            }
            
            /* 输入框样式 */
            QLineEdit {
                background-color: white;
                color: #1e293b;
                selection-background-color: #667eea;
                selection-color: white;
            }
            
            /* 列表样式 */
            QListWidget {
                background-color: white;
                color: #1e293b;
            }
            
            /* 复选框样式 */
            QCheckBox {
                background-color: transparent;
            }
        """)
            
    def setup_animations(self):
        """设置动画效果"""
        # 页面切换动画
        self.page_animation = QPropertyAnimation(self, b"windowOpacity")
        self.page_animation.setDuration(300)
        self.page_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        
    def setup_connections(self):
        """设置信号连接"""
        # 这里可以连接实际的业务逻辑
        pass
        
    # 主题切换功能已移除
        
    def load_settings(self):
        """加载设置（移除主题相关）"""
        pass
            
    def save_settings(self):
        """保存设置（移除主题相关）"""
        pass
        
    # 功能方法
    def add_component(self):
        """添加元件"""
        input_text = self.component_input.text().strip()
        if not input_text:
            return
            
        # 添加到列表（这里需要实现实际的验证逻辑）
        item = QListWidgetItem(input_text)
        self.component_list.addItem(item)
        self.component_input.clear()
        
        # 更新计数
        self.component_count_label.setText(f"共 {self.component_list.count()} 个元器件")
        
    def paste_from_clipboard(self):
        """从剪贴板粘贴"""
        from PyQt6.QtWidgets import QApplication
        clipboard = QApplication.clipboard()
        text = clipboard.text().strip()
        if text:
            self.component_input.setText(text)
            self.add_component()
            
    def clear_all_components(self):
        """清除所有元件"""
        self.component_list.clear()
        self.component_count_label.setText("共 0 个元器件")
        
    def show_component_menu(self, position):
        """显示元件右键菜单"""
        # 实现右键菜单逻辑
        pass
        
    def select_bom_file(self):
        """选择BOM文件"""
        from PyQt6.QtWidgets import QFileDialog
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择BOM文件", "",
            "Excel文件 (*.xlsx *.xls);;CSV文件 (*.csv);;所有文件 (*.*)"
        )
        
        if file_path:
            self.bom_file_label.setText(file_path.split('/')[-1])
            # 这里需要实现BOM解析逻辑
            
    def browse_output_path(self):
        """浏览输出路径"""
        from PyQt6.QtWidgets import QFileDialog
        path = QFileDialog.getExistingDirectory(
            self, "选择输出目录", "",
            QFileDialog.Option.ShowDirsOnly
        )
        
        if path:
            self.output_path_input.setText(path)
            
    def update_export_options(self):
        """更新导出选项"""
        # 确保至少选择一个选项
        if not any([self.symbol_checkbox.isChecked(), 
                   self.footprint_checkbox.isChecked(), 
                   self.model3d_checkbox.isChecked()]):
            self.symbol_checkbox.setChecked(True)
            
    def request_export(self):
        """请求导出"""
        if self.component_list.count() == 0:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "警告", "请先添加要转换的元器件编号")
            return
            
        # 显示进度条
        self.progress_bar.setVisible(True)
        self.status_label.setText("正在转换中...")
        self.export_btn.setEnabled(False)
        
        # 这里需要实现实际的导出逻辑
        
    def resizeEvent(self, event):
        """重写大小改变事件"""
        super().resizeEvent(event)
        # 可以在这里添加响应式布局逻辑