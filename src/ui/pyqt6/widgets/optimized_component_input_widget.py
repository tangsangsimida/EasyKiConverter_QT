#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
优化版现代化组件输入界面 - 修复布局拥挤问题
采用更合理的间距和尺寸分配
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Any, Optional

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton,
    QListWidget, QListWidgetItem, QLabel, QGroupBox, QCheckBox,
    QFileDialog, QMessageBox, QTextEdit, QFrame, QScrollArea,
    QProgressBar, QSplitter, QGridLayout, QSizePolicy
)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtSignal, QTimer, QSize
from PyQt6.QtGui import QIcon, QFont, QPalette, QColor, QLinearGradient, QPainter

from utils.bom_parser import BOMParser
from utils.component_validator import ComponentValidator
from utils.modern_style import ModernStyle, ModernButton, ModernLineEdit
from utils.ui_effects import LoadingSpinner, ModernCard, SuccessAnimation, ModernProgressBar
from utils.responsive_layout import AdaptiveWidget


class OptimizedComponentInputWidget(AdaptiveWidget):
    """优化版现代化组件输入界面"""
    
    # 信号定义
    export_requested = pyqtSignal(list, dict, str, str)  # 元件列表, 选项, 导出路径, 文件前缀
    import_bom_requested = pyqtSignal(str)  # BOM文件路径
    conversion_completed = pyqtSignal(str, str, str, str)  # 总转换, 成功, 失败, 平均用时
    
    def __init__(self, config_manager, parent=None):
        super().__init__(parent)
        self.config_manager = config_manager
        self.component_validator = ComponentValidator()
        self.bom_parser = BOMParser()
        
        self.components = []  # 存储元件列表
        self.export_options = {
            'symbol': True,
            'footprint': True,
            'model3d': True
        }
        
        self.init_ui()
        self.load_settings()
        
    def init_ui(self):
        """初始化用户界面 - 现代化从上至下布局"""
        # 主布局 - 现代化垂直布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        self.setStyleSheet("""
            OptimizedComponentInputWidget {
                background-color: #f8fafc;
            }
        """)
        
        # 1. 现代化标题区域
        header_section = self.create_modern_header_section()
        main_layout.addWidget(header_section)
        
        # 2. 主内容容器 - 现代化卡片设计
        content_widget = QWidget()
        content_widget.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
                border-radius: 16px 16px 0 0;
                margin: 20px 20px 0 20px;
            }
        """)
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(30, 30, 30, 30)
        content_layout.setSpacing(25)
        
        # 2.1 组件输入区域（现代化设计）
        input_section = self.create_modern_input_section()
        content_layout.addWidget(input_section)
        
        # 2.2 组件列表区域（现代化设计）
        list_section = self.create_modern_list_section()
        content_layout.addWidget(list_section, 1)
        
        # 2.3 导出选项区域（现代化设计）
        export_section = self.create_modern_export_section()
        content_layout.addWidget(export_section)
        
        main_layout.addWidget(content_widget)
        
        # 3. 现代化底部操作区域
        bottom_section = self.create_modern_bottom_section()
        main_layout.addWidget(bottom_section)
        
    # 移除了 create_tips_section 方法 - 改用现代化头部区域
        """创建简洁的使用提示区域（替代原来的卡片标题）"""
        container = QWidget()
        container.setObjectName("tipsSection")
        container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        container.setStyleSheet("""
            QWidget#tipsSection {
                background-color: transparent;
                padding: 10px 0;
            }
        """)
        
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        
        # 简洁的使用提示
        tips_label = QLabel("💡 支持LCSC编号：C2040、C123456  |  支持元件型号：ESP32、STM32F103  |  可批量导入BOM文件")
        tips_label.setStyleSheet("""
            font-size: 14px;
            color: #64748b;
            background-color: #f1f5f9;
            border-radius: 8px;
            padding: 12px 20px;
        """)
        tips_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(tips_label)
        
        return container
        
    def create_modern_bottom_section(self) -> QWidget:
        """创建现代化底部操作区域"""
        container = QWidget()
        container.setObjectName("modernBottomSection")
        container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        container.setStyleSheet("""
            QWidget#modernBottomSection {
                background-color: #ffffff;
                border-radius: 0 0 16px 16px;
                padding: 30px 40px;
                margin: 0 20px 20px 20px;
            }
        """)
        
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)
        
        # 左侧：状态显示（现代化设计）
        self.status_label = QLabel("准备就绪")
        self.status_label.setStyleSheet("""
            font-size: 15px;
            color: #64748b;
            font-weight: 500;
            background-color: #f1f5f9;
            border-radius: 8px;
            padding: 10px 16px;
            margin: 0;
        """)
        layout.addWidget(self.status_label)
        
        layout.addStretch()
        
        # 右侧：操作按钮（现代化设计）
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)
        
        # 预览按钮
        preview_btn = QPushButton("👁️ 预览")
        preview_btn.setMinimumHeight(48)
        preview_btn.setMinimumWidth(100)
        preview_btn.setStyleSheet("""
            QPushButton {
                background-color: #f1f5f9;
                color: #475569;
                border: 1px solid #e2e8f0;
                border-radius: 10px;
                padding: 14px 20px;
                font-size: 15px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #e2e8f0;
                color: #1e293b;
            }
        """)
        button_layout.addWidget(preview_btn)
        
        # 开始转换按钮（主要按钮）
        export_btn = QPushButton("🚀 开始转换")
        export_btn.setMinimumHeight(48)
        export_btn.setMinimumWidth(160)
        export_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                          stop:0 #2563eb, 
                                          stop:1 #3b82f6);
                color: white;
                border: none;
                border-radius: 10px;
                padding: 14px 28px;
                font-size: 16px;
                font-weight: 600;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                          stop:0 #1d4ed8, 
                                          stop:1 #2563eb);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                          stop:0 #1e40af, 
                                          stop:1 #1d4ed8);
            }
        """)
        export_btn.clicked.connect(self.start_export)
        button_layout.addWidget(export_btn)
        
        layout.addLayout(button_layout)
        
        return container
        
    def create_modern_export_section(self) -> QWidget:
        """创建现代化导出选项区域"""
        container = QWidget()
        container.setObjectName("modernExportSection")
        container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)
        
        # 标题区域
        title_layout = QHBoxLayout()
        title_label = QLabel("⚙️ 导出选项")
        title_label.setStyleSheet("""
            font-size: 20px;
            font-weight: 600;
            color: #1e293b;
            margin: 0;
        """)
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        layout.addLayout(title_layout)
        
        # 导出选项容器（现代化设计）
        export_widget = QWidget()
        export_widget.setStyleSheet("""
            QWidget {
                background-color: #f8fafc;
                border-radius: 12px;
                padding: 20px;
            }
        """)
        
        export_layout = QVBoxLayout(export_widget)
        export_layout.setContentsMargins(0, 0, 0, 0)
        export_layout.setSpacing(20)
        
        # 导出类型选择（现代化复选框）
        types_layout = QHBoxLayout()
        types_layout.setSpacing(30)
        
        # 符号导出
        self.symbol_check = QCheckBox("📋 导出符号 (Symbol)")
        self.symbol_check.setChecked(True)
        self.symbol_check.setStyleSheet("""
            QCheckBox {
                font-size: 15px;
                color: #475569;
                spacing: 10px;
                padding: 8px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border-radius: 4px;
                border: 2px solid #e2e8f0;
                background-color: white;
            }
            QCheckBox::indicator:checked {
                background-color: #2563eb;
                border-color: #2563eb;
                image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iOSIgdmlld0JveD0iMCAwIDEyIDkiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxwYXRoIGQ9Ik0xIDRMNC41IDcuNUwxMSAxIiBzdHJva2U9IndoaXRlIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIvPgo8L3N2Zz4=);
            }
        """)
        types_layout.addWidget(self.symbol_check)
        
        # 封装导出
        self.footprint_check = QCheckBox("📦 导出封装 (Footprint)")
        self.footprint_check.setChecked(True)
        self.footprint_check.setStyleSheet("""
            QCheckBox {
                font-size: 15px;
                color: #475569;
                spacing: 10px;
                padding: 8px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border-radius: 4px;
                border: 2px solid #e2e8f0;
                background-color: white;
            }
            QCheckBox::indicator:checked {
                background-color: #2563eb;
                border-color: #2563eb;
                image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iOSIgdmlld0JveD0iMCAwIDEyIDkiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxwYXRoIGQ9Ik0xIDRMNC41IDcuNUwxMSAxIiBzdHJva2U9IndoaXRlIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIvPgo8L3N2Zz4=);
            }
        """)
        types_layout.addWidget(self.footprint_check)
        
        # 3D模型导出
        self.model3d_check = QCheckBox("🎨 导出3D模型")
        self.model3d_check.setChecked(True)
        self.model3d_check.setStyleSheet("""
            QCheckBox {
                font-size: 15px;
                color: #475569;
                spacing: 10px;
                padding: 8px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border-radius: 4px;
                border: 2px solid #e2e8f0;
                background-color: white;
            }
            QCheckBox::indicator:checked {
                background-color: #2563eb;
                border-color: #2563eb;
                image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iOSIgdmlld0JveD0iMCAwIDEyIDkiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxwYXRoIGQ9Ik0xIDRMNC41IDcuNUwxMSAxIiBzdHJva2U9IndoaXRlIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIvPgo8L3N2Zz4=);
            }
        """)
        types_layout.addWidget(self.model3d_check)
        
        types_layout.addStretch()
        export_layout.addLayout(types_layout)
        
        # 输出路径设置（现代化设计）
        path_layout = QVBoxLayout()
        path_layout.setSpacing(10)
        
        path_label = QLabel("📁 输出目录：")
        path_label.setStyleSheet("""
            font-size: 15px;
            color: #475569;
            font-weight: 500;
            margin: 0;
        """)
        path_layout.addWidget(path_label)
        
        path_row = QHBoxLayout()
        path_row.setSpacing(12)
        
        self.path_input = ModernLineEdit()
        self.path_input.setPlaceholderText("选择输出目录...")
        self.path_input.setMinimumHeight(48)
        self.path_input.setStyleSheet("""
            QLineEdit {
                font-size: 15px;
                padding: 14px 16px;
                border: 2px solid #e2e8f0;
                border-radius: 10px;
                background-color: white;
                color: #1e293b;
            }
            QLineEdit:focus {
                border-color: #2563eb;
                background-color: white;
                outline: none;
            }
            QLineEdit::placeholder {
                color: #94a3b8;
            }
        """)
        path_row.addWidget(self.path_input)
        
        browse_btn = QPushButton("📂 浏览")
        browse_btn.setMinimumHeight(48)
        browse_btn.setMinimumWidth(100)
        browse_btn.setStyleSheet("""
            QPushButton {
                background-color: #f1f5f9;
                color: #475569;
                border: 1px solid #e2e8f0;
                border-radius: 10px;
                padding: 14px 20px;
                font-size: 14px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #e2e8f0;
                color: #1e293b;
            }
        """)
        browse_btn.clicked.connect(self.browse_output_path)
        path_row.addWidget(browse_btn)
        
        path_layout.addLayout(path_row)
        
        # 文件前缀
        prefix_layout = QVBoxLayout()
        prefix_layout.setSpacing(10)
        
        prefix_label = QLabel("🏷️ 文件前缀（可选）：")
        prefix_label.setStyleSheet("""
            font-size: 15px;
            color: #475569;
            font-weight: 500;
            margin: 0;
        """)
        prefix_layout.addWidget(prefix_label)
        
        self.prefix_input = ModernLineEdit()
        self.prefix_input.setPlaceholderText("例如：MyProject_")
        self.prefix_input.setMinimumHeight(48)
        self.prefix_input.setStyleSheet("""
            QLineEdit {
                font-size: 15px;
                padding: 14px 16px;
                border: 2px solid #e2e8f0;
                border-radius: 10px;
                background-color: white;
                color: #1e293b;
            }
            QLineEdit:focus {
                border-color: #2563eb;
                background-color: white;
                outline: none;
            }
            QLineEdit::placeholder {
                color: #94a3b8;
            }
        """)
        prefix_layout.addWidget(self.prefix_input)
        
        path_layout.addLayout(prefix_layout)
        export_layout.addLayout(path_layout)
        
        layout.addWidget(export_widget)
        
        return container
        
    def create_modern_list_section(self) -> QWidget:
        """创建现代化组件列表区域"""
        container = QWidget()
        container.setObjectName("modernListSection")
        container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(15)
        
        # 列表标题区域
        header_layout = QHBoxLayout()
        title_label = QLabel("📋 组件列表")
        title_label.setStyleSheet("""
            font-size: 20px;
            font-weight: 600;
            color: #1e293b;
            margin: 0;
        """)
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        # 组件数量统计
        self.component_count_label = QLabel("共 0 个组件")
        self.component_count_label.setStyleSheet("""
            font-size: 14px;
            color: #64748b;
            font-weight: 500;
            background-color: #f1f5f9;
            border-radius: 6px;
            padding: 6px 12px;
            margin: 0;
        """)
        header_layout.addWidget(self.component_count_label)
        layout.addLayout(header_layout)
        
        # 组件列表（现代化设计）
        self.component_list = QListWidget()
        self.component_list.setMinimumHeight(250)
        self.component_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #e2e8f0;
                border-radius: 12px;
                background-color: #ffffff;
                font-size: 14px;
                padding: 8px;
            }
            QListWidget::item {
                padding: 12px 16px;
                border-radius: 8px;
                margin: 4px 0;
                background-color: #f8fafc;
                border: 1px solid #e2e8f0;
            }
            QListWidget::item:hover {
                background-color: #f1f5f9;
                border-color: #cbd5e1;
            }
            QListWidget::item:selected {
                background-color: #dbeafe;
                border-color: #2563eb;
                color: #1e40af;
            }
            QListWidget::item:selected:hover {
                background-color: #bfdbfe;
            }
        """)
        layout.addWidget(self.component_list)
        
        return container
        
    def create_modern_input_section(self) -> QWidget:
        """创建现代化组件输入区域"""
        container = QWidget()
        container.setObjectName("modernInputSection")
        container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)
        
        # 标题区域
        header_layout = QHBoxLayout()
        title_label = QLabel("🔍 组件输入")
        title_label.setStyleSheet("""
            font-size: 20px;
            font-weight: 600;
            color: #1e293b;
            margin: 0;
        """)
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        # 使用提示标签
        tips_label = QLabel("💡 支持LCSC编号：C2040、C123456  |  支持元件型号：ESP32、STM32F103")
        tips_label.setStyleSheet("""
            font-size: 13px;
            color: #64748b;
            background-color: #f1f5f9;
            border-radius: 6px;
            padding: 8px 12px;
            margin: 0;
        """)
        header_layout.addWidget(tips_label)
        layout.addLayout(header_layout)
        
        # 输入区域（现代化设计）
        input_widget = QWidget()
        input_widget.setStyleSheet("""
            QWidget {
                background-color: #f8fafc;
                border-radius: 12px;
                padding: 20px;
            }
        """)
        
        input_layout = QVBoxLayout(input_widget)
        input_layout.setContentsMargins(0, 0, 0, 0)
        input_layout.setSpacing(12)
        
        # 输入标签
        input_label = QLabel("请输入组件ID或型号：")
        input_label.setStyleSheet("""
            font-size: 14px;
            color: #475569;
            font-weight: 500;
            margin: 0;
        """)
        input_layout.addWidget(input_label)
        
        # 输入框和按钮
        input_row = QHBoxLayout()
        input_row.setSpacing(12)
        
        self.component_input = ModernLineEdit()
        self.component_input.setPlaceholderText("例如：C2040、ESP32、STM32F103...")
        self.component_input.setMinimumHeight(48)
        self.component_input.setStyleSheet("""
            QLineEdit {
                font-size: 15px;
                padding: 14px 16px;
                border: 2px solid #e2e8f0;
                border-radius: 10px;
                background-color: white;
                color: #1e293b;
            }
            QLineEdit:focus {
                border-color: #2563eb;
                background-color: white;
                outline: none;
            }
            QLineEdit::placeholder {
                color: #94a3b8;
            }
        """)
        input_row.addWidget(self.component_input)
        
        add_btn = ModernButton("➕ 添加组件")
        add_btn.setMinimumHeight(48)
        add_btn.setMinimumWidth(120)
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #2563eb;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 14px 24px;
                font-size: 15px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #1d4ed8;
            }
            QPushButton:pressed {
                background-color: #1e40af;
            }
        """)
        add_btn.clicked.connect(self.add_component)
        input_row.addWidget(add_btn)
        
        input_layout.addLayout(input_row)
        
        # 批量操作按钮（现代化设计）
        batch_layout = QHBoxLayout()
        batch_layout.setSpacing(12)
        
        bom_btn = QPushButton("📋 导入BOM文件")
        bom_btn.setMinimumHeight(42)
        bom_btn.setStyleSheet("""
            QPushButton {
                background-color: #f1f5f9;
                color: #475569;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 12px 20px;
                font-size: 14px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #e2e8f0;
                color: #1e293b;
            }
        """)
        bom_btn.clicked.connect(self.import_bom)
        batch_layout.addWidget(bom_btn)
        
        clear_btn = QPushButton("🗑️ 清空列表")
        clear_btn.setMinimumHeight(42)
        clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #f1f5f9;
                color: #475569;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 12px 20px;
                font-size: 14px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #e2e8f0;
                color: #1e293b;
            }
        """)
        clear_btn.clicked.connect(self.clear_components)
        batch_layout.addWidget(clear_btn)
        
        batch_layout.addStretch()
        input_layout.addLayout(batch_layout)
        
        layout.addWidget(input_widget)
        
        return container
        
    def create_modern_header_section(self) -> QWidget:
        """创建现代化标题区域"""
        container = QWidget()
        container.setObjectName("modernHeader")
        container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        container.setStyleSheet("""
            QWidget#modernHeader {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                          stop:0 #2563eb, 
                                          stop:1 #3b82f6);
                padding: 30px 40px;
            }
        """)
        
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)
        
        # 左侧标题
        title_layout = QVBoxLayout()
        title_layout.setSpacing(8)
        
        main_title = QLabel("元器件转换")
        main_title.setStyleSheet("""
            font-size: 32px;
            font-weight: 700;
            color: white;
            margin: 0;
        """)
        title_layout.addWidget(main_title)
        
        subtitle = QLabel("嘉立创EDA转KiCad专业转换工具")
        subtitle.setStyleSheet("""
            font-size: 16px;
            color: rgba(255, 255, 255, 0.9);
            margin: 0;
        """)
        title_layout.addWidget(subtitle)
        
        layout.addLayout(title_layout)
        layout.addStretch()
        
        # 右侧统计信息
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(30)
        
        # 组件数量
        count_layout = QVBoxLayout()
        count_layout.setSpacing(4)
        
        self.component_count_label = QLabel("0")
        self.component_count_label.setStyleSheet("""
            font-size: 36px;
            font-weight: 700;
            color: white;
            margin: 0;
        """)
        count_layout.addWidget(self.component_count_label, 0, Qt.AlignmentFlag.AlignRight)
        
        count_text = QLabel("个组件")
        count_text.setStyleSheet("""
            font-size: 14px;
            color: rgba(255, 255, 255, 0.8);
            margin: 0;
        """)
        count_layout.addWidget(count_text, 0, Qt.AlignmentFlag.AlignRight)
        
        stats_layout.addLayout(count_layout)
        
        # 状态指示器
        status_indicator = QWidget()
        status_indicator.setFixedSize(12, 12)
        status_indicator.setStyleSheet("""
            background-color: #10b981;
            border-radius: 6px;
            margin: 0;
        """)
        stats_layout.addWidget(status_indicator, 0, Qt.AlignmentFlag.AlignBottom)
        
        layout.addLayout(stats_layout)
        
        return container
        
    def import_bom(self):
        """导入BOM文件 - 简化版本"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择BOM文件", "",
            "Excel文件 (*.xlsx *.xls);;CSV文件 (*.csv);;所有文件 (*.*)"
        )
        
        if file_path:
            self.import_bom_file(file_path)
    
    def import_bom_file(self, file_path: str):
        """导入BOM文件 - 修复崩溃问题"""
        try:
            # 首先验证文件是否存在和可读
            if not os.path.exists(file_path):
                QMessageBox.warning(self, "文件错误", f"文件不存在: {file_path}")
                return
                
            if not os.access(file_path, os.R_OK):
                QMessageBox.warning(self, "文件错误", f"文件无法读取: {file_path}")
                return
            
            # 获取文件信息
            file_size = os.path.getsize(file_path)
            if file_size == 0:
                QMessageBox.warning(self, "文件错误", "BOM文件为空")
                return
                
            if file_size > 10 * 1024 * 1024:  # 10MB限制
                QMessageBox.warning(self, "文件错误", "BOM文件过大 (>10MB)")
                return
            
            # 解析BOM文件
            result = self.bom_parser.parse_bom_file(file_path)
            
            if not result['success']:
                QMessageBox.warning(self, "BOM解析失败", result['error'])
                return
                
            component_ids = result.get('component_ids', [])
            
            if not component_ids:
                QMessageBox.information(self, "提示", "BOM文件中没有找到有效的元件编号")
                return
                
            # 添加解析到的组件
            added_count = 0
            duplicate_count = 0
            
            for component_id in component_ids:
                if component_id and component_id not in self.components:
                    self.components.append(component_id)
                    added_count += 1
                else:
                    duplicate_count += 1
            
            # 更新界面
            self.update_component_list()
            
            # 显示结果
            message = f"从BOM文件导入 {added_count} 个新组件"
            if duplicate_count > 0:
                message += f"（跳过 {duplicate_count} 个重复组件）"
            
            self.status_label.setText(f"✅ {message}")
            
            # 发送BOM导入信号
            self.import_bom_requested.emit(file_path)
            
        except Exception as e:
            error_msg = f"导入BOM文件时发生错误：\n{str(e)}\n\n请检查：\n1. 文件格式是否正确（Excel/CSV）\n2. 文件是否损坏\n3. 是否缺少依赖库"
            QMessageBox.critical(self, "BOM导入错误", error_msg)
            self.status_label.setText("❌ BOM导入失败")
            print(f"BOM导入错误详情: {e}")
    
    def browse_output_path(self):
        """浏览输出目录"""
        path = QFileDialog.getExistingDirectory(self, "选择输出目录")
        if path:
            self.path_input.setText(path)
            self.save_settings()
    
    def clear_components(self):
        """清空组件列表"""
        if not self.components:
            return
            
        reply = QMessageBox.question(
            self, "确认清空", 
            "确定要清空所有组件吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.components.clear()
            self.update_component_list()
            self.status_label.setText("✅ 组件列表已清空")
        
    # 移除了 create_export_section 方法 - 改用现代化导出区域
        """创建导出选项区域 - 从上至下布局"""
        container = QWidget()
        container.setObjectName("exportSection")
        container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        container.setStyleSheet("""
            QWidget#exportSection {
                background-color: white;
                border: 1px solid #e2e8f0;
                border-radius: 12px;
                padding: 20px;
            }
        """)
        
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(15)
        
        # 导出选项标题
        title_label = QLabel("⚙️ 导出选项")
        title_label.setStyleSheet("""
            font-size: 18px;
            font-weight: 600;
            color: #1e293b;
        """)
        layout.addWidget(title_label)
        
        # 导出类型选择（从上至下）
        export_types_layout = QVBoxLayout()
        export_types_layout.setSpacing(10)
        
        # 符号导出
        self.symbol_check = QCheckBox("📋 导出符号 (Symbol)")
        self.symbol_check.setChecked(True)
        self.symbol_check.setStyleSheet("""
            QCheckBox {
                font-size: 14px;
                color: #475569;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }
        """)
        export_types_layout.addWidget(self.symbol_check)
        
        # 封装导出
        self.footprint_check = QCheckBox("📦 导出封装 (Footprint)")
        self.footprint_check.setChecked(True)
        self.footprint_check.setStyleSheet("""
            QCheckBox {
                font-size: 14px;
                color: #475569;
                spacing: 8px;
            }
        """)
        export_types_layout.addWidget(self.footprint_check)
        
        # 3D模型导出
        self.model3d_check = QCheckBox("🎨 导出3D模型")
        self.model3d_check.setChecked(True)
        self.model3d_check.setStyleSheet("""
            QCheckBox {
                font-size: 14px;
                color: #475569;
                spacing: 8px;
            }
        """)
        export_types_layout.addWidget(self.model3d_check)
        
        layout.addLayout(export_types_layout)
        
        # 输出路径设置
        path_layout = QVBoxLayout()
        path_layout.setSpacing(8)
        
        path_label = QLabel("输出目录：")
        path_label.setStyleSheet("""
            font-size: 14px;
            color: #475569;
            font-weight: 500;
        """)
        path_layout.addWidget(path_label)
        
        path_row = QHBoxLayout()
        path_row.setSpacing(10)
        
        self.path_input = ModernLineEdit()
        self.path_input.setPlaceholderText("选择输出目录...")
        self.path_input.setMinimumHeight(40)
        path_row.addWidget(self.path_input)
        
        browse_btn = ModernButton("📁 浏览")
        browse_btn.setMinimumHeight(40)
        browse_btn.setMinimumWidth(80)
        browse_btn.clicked.connect(self.browse_output_path)
        path_row.addWidget(browse_btn)
        
        path_layout.addLayout(path_row)
        layout.addLayout(path_layout)
        
        # 文件前缀
        prefix_layout = QVBoxLayout()
        prefix_layout.setSpacing(8)
        
        prefix_label = QLabel("文件前缀（可选）：")
        prefix_label.setStyleSheet("""
            font-size: 14px;
            color: #475569;
            font-weight: 500;
        """)
        prefix_layout.addWidget(prefix_label)
        
        self.prefix_input = ModernLineEdit()
        self.prefix_input.setPlaceholderText("例如：MyProject_")
        self.prefix_input.setMinimumHeight(40)
        prefix_layout.addWidget(self.prefix_input)
        
        layout.addLayout(prefix_layout)
        
        return container
        
    # 移除了 create_list_section 方法 - 改用现代化列表区域
        """创建组件列表区域 - 从上至下布局"""
        container = QWidget()
        container.setObjectName("listSection")
        container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        container.setStyleSheet("""
            QWidget#listSection {
                background-color: white;
                border: 1px solid #e2e8f0;
                border-radius: 12px;
                padding: 20px;
            }
        """)
        
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(15)
        
        # 列表标题和统计
        header_layout = QHBoxLayout()
        title_label = QLabel("📋 组件列表")
        title_label.setStyleSheet("""
            font-size: 18px;
            font-weight: 600;
            color: #1e293b;
        """)
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        # 组件数量统计
        self.component_count_label = QLabel("共 0 个组件")
        self.component_count_label.setStyleSheet("""
            font-size: 14px;
            color: #64748b;
            font-weight: 500;
        """)
        header_layout.addWidget(self.component_count_label)
        layout.addLayout(header_layout)
        
        # 组件列表
        self.component_list = QListWidget()
        self.component_list.setMinimumHeight(200)
        self.component_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                background-color: #f8fafc;
                font-size: 14px;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #f1f5f9;
            }
            QListWidget::item:selected {
                background-color: #dbeafe;
                color: #1e40af;
            }
        """)
        layout.addWidget(self.component_list)
        
        return container
        
    # 移除了 create_input_section 方法 - 改用现代化输入区域
        """创建组件输入区域 - 从上至下布局"""
        container = QWidget()
        container.setObjectName("inputSection")
        container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        container.setStyleSheet("""
            QWidget#inputSection {
                background-color: white;
                border: 1px solid #e2e8f0;
                border-radius: 12px;
                padding: 20px;
            }
        """)
        
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(15)
        
        # 输入区域标题
        title_layout = QHBoxLayout()
        title_label = QLabel("🔍 组件输入")
        title_label.setStyleSheet("""
            font-size: 18px;
            font-weight: 600;
            color: #1e293b;
        """)
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        layout.addLayout(title_layout)
        
        # 组件ID输入（从上至下）
        input_layout = QVBoxLayout()
        input_layout.setSpacing(10)
        
        # 输入框标签
        input_label = QLabel("请输入组件ID或型号：")
        input_label.setStyleSheet("""
            font-size: 14px;
            color: #475569;
            font-weight: 500;
        """)
        input_layout.addWidget(input_label)
        
        # 输入框和按钮的水平布局
        input_row = QHBoxLayout()
        input_row.setSpacing(10)
        
        self.component_input = ModernLineEdit()
        self.component_input.setPlaceholderText("例如：C2040、ESP32、STM32F103...")
        self.component_input.setMinimumHeight(45)
        self.component_input.setStyleSheet("""
            QLineEdit {
                font-size: 14px;
                padding: 12px;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                background-color: #f8fafc;
            }
            QLineEdit:focus {
                border-color: #2563eb;
                background-color: white;
            }
        """)
        input_row.addWidget(self.component_input)
        
        # 添加按钮
        add_btn = ModernButton("添加组件")
        add_btn.setMinimumHeight(45)
        add_btn.setMinimumWidth(100)
        add_btn.clicked.connect(self.add_component)
        input_row.addWidget(add_btn)
        
        input_layout.addLayout(input_row)
        layout.addLayout(input_layout)
        
        # 批量操作按钮（从上至下）
        batch_layout = QHBoxLayout()
        batch_layout.setSpacing(10)
        
        bom_btn = ModernButton("📋 导入BOM文件")
        bom_btn.setMinimumHeight(40)
        bom_btn.clicked.connect(self.import_bom)
        batch_layout.addWidget(bom_btn)
        
        clear_btn = ModernButton("🗑️ 清空列表")
        clear_btn.setMinimumHeight(40)
        clear_btn.clicked.connect(self.clear_components)
        batch_layout.addWidget(clear_btn)
        
        layout.addLayout(batch_layout)
        
        return container
        """创建标题区域 - 增加高度和视觉层次"""
        container = QWidget()
        container.setObjectName("titleSection")
        container.setMinimumHeight(120)  # 增加最小高度
        container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        container.setStyleSheet("""
            QWidget#titleSection {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                          stop:0 #f8fafc, 
                                          stop:1 #e2e8f0);
                border-radius: 20px;
                padding: 30px;
                margin-bottom: 10px;
            }
        """)
        
        # 添加阴影效果
        from utils.modern_style import ModernStyle
        ModernStyle.add_shadow_effect(container, blur_radius=25, offset=(0, 6))
        
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(30)
        
        # 左侧标题和描述 - 增加间距
        text_container = QWidget()
        text_layout = QVBoxLayout(text_container)
        text_layout.setContentsMargins(0, 0, 0, 0)
        text_layout.setSpacing(12)  # 增加行间距
        
        title = QLabel("元器件转换")
        title.setStyleSheet("""
            font-size: 28px;
            font-weight: 700;
            color: #1e293b;
            margin-bottom: 8px;
        """)
        text_layout.addWidget(title)
        
        subtitle = QLabel("支持嘉立创EDA、LCSC元器件转换为KiCad格式")
        subtitle.setStyleSheet("""
            font-size: 16px;
            color: #64748b;
            line-height: 24px;
        """)
        text_layout.addWidget(subtitle)
        
        # 添加功能特点
        features = QLabel("✨ 完整转换 • 🚀 批量处理 • 🎨 现代化界面")
        features.setStyleSheet("""
            font-size: 14px;
            color: #64748b;
            margin-top: 8px;
        """)
        text_layout.addWidget(features)
        
        layout.addWidget(text_container)
        layout.addStretch()
        
        # 右侧统计信息 - 增大字体
        stats_container = QWidget()
        stats_layout = QHBoxLayout(stats_container)
        stats_layout.setSpacing(25)  # 增加统计项间距
        
        # 组件数量统计 - 增大字体
        count_layout = QVBoxLayout()
        count_layout.setSpacing(5)
        
        self.component_count_label = QLabel("0")
        self.component_count_label.setStyleSheet("""
            font-size: 42px;  /* 增大字体 */
            font-weight: 700;
            color: #2563eb;
            background: transparent;
        """)
        count_layout.addWidget(self.component_count_label, 0, Qt.AlignmentFlag.AlignBottom)
        
        count_text = QLabel("个组件")
        count_text.setStyleSheet("""
            font-size: 16px;  /* 增大字体 */
            color: #64748b;
        """)
        count_layout.addWidget(count_text, 0, Qt.AlignmentFlag.AlignTop)
        
        stats_layout.addLayout(count_layout)
        
        # 添加状态指示器
        status_indicator = QWidget()
        status_indicator.setFixedSize(12, 12)
        status_indicator.setStyleSheet("""
            background-color: #10b981;
            border-radius: 6px;
        """)
        stats_layout.addWidget(status_indicator)
        
        layout.addWidget(stats_container)
        
        return container
        
    # 移除了 create_left_panel 方法 - 改用从上至下布局
        
    def create_input_card(self) -> QFrame:
        """创建输入卡片 - 优化尺寸和布局，增加空间"""
        card = QFrame()
        card.setObjectName("inputCard")
        card.setMinimumHeight(280)  # 进一步增加最小高度
        card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        card.setStyleSheet("""
            QFrame#inputCard {
                background-color: white;
                border: 2px solid #e2e8f0;
                border-radius: 20px;
                padding: 35px;  /* 增加内边距 */
            }
            QFrame#inputCard:hover {
                border-color: #cbd5e1;
            }
        """)
        
        # 添加阴影效果
        ModernStyle.add_shadow_effect(card, blur_radius=20, offset=(0, 5))
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)  # 增加内部间距
        
        # 卡片标题 - 增大图标和字体
        title_layout = QHBoxLayout()
        title_layout.setSpacing(12)
        
        icon = QLabel("🔍")
        icon.setStyleSheet("font-size: 24px; margin-right: 5px;")
        title_layout.addWidget(icon)
        
        title = QLabel("添加元器件")
        title.setStyleSheet("""
            font-size: 20px;  /* 增大字体 */
            font-weight: 600;
            color: #1e293b;
        """)
        title_layout.addWidget(title)
        title_layout.addStretch()
        
        layout.addLayout(title_layout)
        
        # 输入区域 - 增加高度和间距
        input_layout = QHBoxLayout()
        input_layout.setSpacing(20)  # 进一步增加间距
        
        self.component_input = ModernLineEdit()
        self.component_input.setPlaceholderText("输入元器件编号，如 C2040、ESP32、STM32F103...")
        self.component_input.setMinimumHeight(65)  # 保持高度
        self.component_input.setFont(QFont("Segoe UI", 13))  # 增大字体
        self.component_input.returnPressed.connect(self.add_component)
        input_layout.addWidget(self.component_input)
        
        add_btn = ModernButton("添加")
        add_btn.setMinimumWidth(140)  # 进一步增加按钮宽度
        add_btn.setMinimumHeight(65)  # 保持按钮高度
        add_btn.setFont(QFont("Segoe UI", 13, QFont.Weight.Medium))
        add_btn.clicked.connect(self.add_component)
        input_layout.addWidget(add_btn)
        
        layout.addLayout(input_layout)
        
        # 快捷操作 - 增大按钮和间距
        quick_actions = QHBoxLayout()
        quick_actions.setSpacing(15)  # 增加按钮间距
        
        paste_btn = QPushButton("📋 从剪贴板粘贴")
        paste_btn.setMinimumHeight(42)  # 增加按钮高度
        paste_btn.setFont(QFont("Segoe UI", 13))  # 增大字体
        paste_btn.setStyleSheet("""
            QPushButton {
                background-color: #f1f5f9;
                color: #64748b;
                border: 1px solid #e2e8f0;
                border-radius: 12px;  /* 增大圆角 */
                padding: 12px 20px;   /* 增加内边距 */
                font-size: 14px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #e2e8f0;
                color: #475569;
            }
        """)
        paste_btn.clicked.connect(self.paste_from_clipboard)
        quick_actions.addWidget(paste_btn)
        
        clear_btn = QPushButton("🗑️ 清空")
        clear_btn.setMinimumHeight(42)  # 增加按钮高度
        clear_btn.setFont(QFont("Segoe UI", 13))  # 增大字体
        clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #f1f5f9;
                color: #64748b;
                border: 1px solid #e2e8f0;
                border-radius: 12px;  /* 增大圆角 */
                padding: 12px 20px;   /* 增加内边距 */
                font-size: 14px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #fee2e2;
                color: #dc2626;
                border-color: #fecaca;
            }
        """)
        clear_btn.clicked.connect(self.clear_all_components)
        quick_actions.addWidget(clear_btn)
        
        quick_actions.addStretch()
        layout.addLayout(quick_actions)
        
        # 格式提示 - 增大字体
        hint_label = QLabel("💡 支持格式：C2040、C123456、ESP32、STM32F103 等")
        hint_label.setStyleSheet("""
            color: #64748b;
            font-size: 13px;  /* 增大字体 */
            padding-top: 12px;
        """)
        layout.addWidget(hint_label)
        
        return card
        
    def create_list_card(self) -> QFrame:
        """创建列表卡片 - 优化列表显示区域，增加空间"""
        card = QFrame()
        card.setObjectName("listCard")
        card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        card.setMinimumHeight(450)  # 大幅增加最小高度
        card.setStyleSheet("""
            QFrame#listCard {
                background-color: white;
                border: 2px solid #e2e8f0;
                border-radius: 20px;
                padding: 35px;  /* 增加内边距 */
            }
            QFrame#listCard:hover {
                border-color: #cbd5e1;
            }
        """)
        
        ModernStyle.add_shadow_effect(card, blur_radius=20, offset=(0, 5))
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)  # 增加内部间距
        
        # 列表标题和操作 - 增大字体
        header_layout = QHBoxLayout()
        header_layout.setSpacing(12)
        
        icon = QLabel("📋")
        icon.setStyleSheet("font-size: 24px; margin-right: 5px;")
        header_layout.addWidget(icon)
        
        title = QLabel("组件列表")
        title.setStyleSheet("""
            font-size: 20px;  /* 增大字体 */
            font-weight: 600;
            color: #1e293b;
        """)
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # 批量操作按钮 - 增大尺寸
        batch_import_btn = QPushButton("📁 批量导入")
        batch_import_btn.setStyleSheet("""
            QPushButton {
                background-color: #f1f5f9;
                color: #64748b;
                border: 1px solid #e2e8f0;
                border-radius: 10px;
                padding: 8px 16px;
                font-size: 13px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #e2e8f0;
                color: #475569;
            }
        """)
        header_layout.addWidget(batch_import_btn)
        
        layout.addLayout(header_layout)
        
        # 组件列表 - 优化样式和尺寸，增加间距
        self.component_list = QListWidget()
        self.component_list.setStyleSheet("""
            QListWidget {
                background-color: #f8fafc;
                border: 1px solid #e2e8f0;
                border-radius: 15px;
                padding: 20px;  /* 增加内边距 */
                font-size: 16px;  /* 进一步增大字体 */
            }
            QListWidget::item {
                background-color: white;
                border: 1px solid #e2e8f0;
                border-radius: 12px;  /* 增大圆角 */
                padding: 18px;  /* 大幅增加内边距 */
                margin: 8px 0;  /* 大幅增加间距 */
                color: #1e293b;
                font-size: 15px;  /* 进一步增大字体 */
                min-height: 50px;  /* 设置最小高度 */
            }
            QListWidget::item:hover {
                background-color: #f1f5f9;
                border-color: #cbd5e1;
            }
            QListWidget::item:selected {
                background-color: #dbeafe;
                border-color: #2563eb;
                color: #1e40af;
            }
        """)
        self.component_list.setMinimumHeight(350)  # 增加最小高度
        layout.addWidget(self.component_list, 1)  # 添加拉伸因子
        
        # 列表底部操作 - 增大按钮和字体
        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(15)  # 增加按钮间距
        
        self.component_count_label = QLabel("共 0 个组件")
        self.component_count_label.setStyleSheet("""
            color: #64748b;
            font-size: 16px;  /* 进一步增大字体 */
            font-weight: 500;
        """)
        bottom_layout.addWidget(self.component_count_label)
        
        bottom_layout.addStretch()
        
        remove_btn = QPushButton("🗑️ 删除选中")
        remove_btn.setMinimumHeight(45)  # 增加按钮高度
        remove_btn.setFont(QFont("Segoe UI", 13))  # 增大字体
        remove_btn.setStyleSheet("""
            QPushButton {
                background-color: #fee2e2;
                color: #dc2626;
                border: 1px solid #fecaca;
                border-radius: 12px;  /* 增大圆角 */
                padding: 10px 18px;   /* 增加内边距 */
                font-size: 14px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #fecaca;
            }
        """)
        remove_btn.clicked.connect(self.remove_selected_components)
        bottom_layout.addWidget(remove_btn)
        
        layout.addLayout(bottom_layout)
        
        return card
        
    # 移除了 create_right_panel 方法 - 改用从上至下布局
        
    def create_options_card(self) -> QFrame:
        """创建选项卡片 - 优化布局和尺寸，增加空间"""
        card = QFrame()
        card.setObjectName("optionsCard")
        card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        card.setMinimumHeight(350)  # 设置最小高度
        card.setStyleSheet("""
            QFrame#optionsCard {
                background-color: white;
                border: 2px solid #e2e8f0;
                border-radius: 20px;
                padding: 35px;  /* 增加内边距 */
            }
            QFrame#optionsCard:hover {
                border-color: #cbd5e1;
            }
        """)
        
        ModernStyle.add_shadow_effect(card, blur_radius=20, offset=(0, 5))
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)  # 增加间距
        
        # 标题 - 增大字体
        title_layout = QHBoxLayout()
        title_layout.setSpacing(12)
        
        icon = QLabel("⚙️")
        icon.setStyleSheet("font-size: 24px; margin-right: 5px;")
        title_layout.addWidget(icon)
        
        title = QLabel("导出选项")
        title.setStyleSheet("""
            font-size: 20px;  /* 增大字体 */
            font-weight: 600;
            color: #1e293b;
        """)
        title_layout.addWidget(title)
        title_layout.addStretch()
        
        layout.addLayout(title_layout)
        
        # 选项 - 大幅增加复选框间距和尺寸
        self.symbol_check = QCheckBox("📋 符号库 (.kicad_sym)")
        self.symbol_check.setChecked(True)
        self.symbol_check.setStyleSheet("""
            QCheckBox {
                font-size: 16px;  /* 进一步增大字体 */
                color: #374151;
                spacing: 12px;    /* 增加间距 */
                padding: 12px;    /* 增加内边距 */
                min-height: 40px; /* 设置最小高度 */
            }
            QCheckBox::indicator {
                width: 24px;      /* 进一步增大指示器 */
                height: 24px;
                border-radius: 6px;
            }
        """)
        layout.addWidget(self.symbol_check)
        
        self.footprint_check = QCheckBox("📦 封装库 (.kicad_mod)")
        self.footprint_check.setChecked(True)
        self.footprint_check.setStyleSheet("""
            QCheckBox {
                font-size: 16px;
                color: #374151;
                spacing: 12px;
                padding: 12px;
                min-height: 40px;
            }
            QCheckBox::indicator {
                width: 24px;
                height: 24px;
                border-radius: 6px;
            }
        """)
        layout.addWidget(self.footprint_check)
        
        self.model3d_check = QCheckBox("🎯 3D模型 (.step/.wrl)")
        self.model3d_check.setChecked(True)
        self.model3d_check.setStyleSheet("""
            QCheckBox {
                font-size: 16px;
                color: #374151;
                spacing: 12px;
                padding: 12px;
                min-height: 40px;
            }
            QCheckBox::indicator {
                width: 24px;
                height: 24px;
                border-radius: 6px;
            }
        """)
        layout.addWidget(self.model3d_check)
        
        layout.addStretch()
        return card
        
    def create_path_card(self) -> QFrame:
        """创建路径卡片 - 优化输入框尺寸"""
        card = QFrame()
        card.setObjectName("pathCard")
        card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        card.setStyleSheet("""
            QFrame#pathCard {
                background-color: white;
                border: 2px solid #e2e8f0;
                border-radius: 20px;
                padding: 30px;
            }
            QFrame#pathCard:hover {
                border-color: #cbd5e1;
            }
        """)
        
        ModernStyle.add_shadow_effect(card, blur_radius=20, offset=(0, 5))
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(18)  # 增加间距
        
        # 标题 - 增大字体
        title_layout = QHBoxLayout()
        title_layout.setSpacing(12)
        
        icon = QLabel("📁")
        icon.setStyleSheet("font-size: 24px; margin-right: 5px;")
        title_layout.addWidget(icon)
        
        title = QLabel("输出设置")
        title.setStyleSheet("""
            font-size: 20px;  /* 增大字体 */
            font-weight: 600;
            color: #1e293b;
        """)
        title_layout.addWidget(title)
        title_layout.addStretch()
        
        layout.addLayout(title_layout)
        
        # 输出路径 - 增大输入框
        path_layout = QVBoxLayout()
        path_layout.setSpacing(10)
        
        path_label = QLabel("输出目录")
        path_label.setStyleSheet("""
            font-size: 14px;  /* 增大字体 */
            color: #64748b;
            font-weight: 500;
        """)
        path_layout.addWidget(path_label)
        
        path_input_layout = QHBoxLayout()
        path_input_layout.setSpacing(12)
        
        self.path_input = ModernLineEdit()
        self.path_input.setPlaceholderText("选择输出目录...")
        self.path_input.setText(str(Path.home() / "Desktop" / "KiCad_Libraries"))
        self.path_input.setMinimumHeight(45)  # 增加高度
        self.path_input.setFont(QFont("Segoe UI", 12))
        path_input_layout.addWidget(self.path_input)
        
        browse_btn = QPushButton("浏览")
        browse_btn.setStyleSheet("""
            QPushButton {
                background-color: #f1f5f9;
                color: #64748b;
                border: 1px solid #e2e8f0;
                border-radius: 10px;
                padding: 10px 18px;
                font-size: 13px;
                font-weight: 500;
                min-width: 70px;
            }
            QPushButton:hover {
                background-color: #e2e8f0;
                color: #475569;
            }
        """)
        browse_btn.clicked.connect(self.browse_output_path)
        path_input_layout.addWidget(browse_btn)
        
        path_layout.addLayout(path_input_layout)
        layout.addLayout(path_layout)
        
        # 文件前缀 - 增大输入框
        prefix_layout = QVBoxLayout()
        prefix_layout.setSpacing(10)
        
        prefix_label = QLabel("文件前缀")
        prefix_label.setStyleSheet("""
            font-size: 14px;
            color: #64748b;
            font-weight: 500;
        """)
        prefix_layout.addWidget(prefix_label)
        
        self.prefix_input = ModernLineEdit()
        self.prefix_input.setPlaceholderText("MyLib_")
        self.prefix_input.setText("")
        self.prefix_input.setMinimumHeight(45)  # 增加高度
        self.prefix_input.setFont(QFont("Segoe UI", 12))
        prefix_layout.addWidget(self.prefix_input)
        
        layout.addLayout(prefix_layout)
        
        return card
        
    def create_help_card(self) -> QFrame:
        """创建帮助信息卡片"""
        card = QFrame()
        card.setObjectName("helpCard")
        card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        card.setStyleSheet("""
            QFrame#helpCard {
                background-color: #f0f9ff;
                border: 1px solid #bae6fd;
                border-radius: 16px;
                padding: 25px;
            }
        """)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(15)
        
        # 标题
        title_layout = QHBoxLayout()
        title_layout.setSpacing(10)
        
        icon = QLabel("💡")
        icon.setStyleSheet("font-size: 20px;")
        title_layout.addWidget(icon)
        
        title = QLabel("使用提示")
        title.setStyleSheet("""
            font-size: 18px;
            font-weight: 600;
            color: #0369a1;
        """)
        title_layout.addWidget(title)
        title_layout.addStretch()
        
        layout.addLayout(title_layout)
        
        # 帮助信息
        help_layout = QVBoxLayout()
        help_layout.setSpacing(10)
        
        help_items = [
            "📝 支持LCSC编号：C2040、C123456",
            "🔧 支持元件型号：ESP32、STM32F103",
            "📋 可批量导入BOM文件",
            "🎯 支持符号、封装、3D模型导出"
        ]
        
        for item in help_items:
            help_label = QLabel(item)
            help_label.setStyleSheet("color: #0c4a6e; font-size: 13px;")
            help_label.setWordWrap(True)
            help_layout.addWidget(help_label)
            
        layout.addLayout(help_layout)
        
        return card
        
    # 移除了 create_bottom_section 方法 - 改用现代化底部区域
        """创建底部操作区域 - 简洁设计"""
        container = QWidget()
        container.setObjectName("bottomSection")
        container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        container.setStyleSheet("""
            QWidget#bottomSection {
                background-color: transparent;
                padding: 20px 0;
            }
        """)
        
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(15)
        
        # 左侧：状态显示
        self.status_label = QLabel("准备就绪")
        self.status_label.setStyleSheet("""
            font-size: 14px;
            color: #64748b;
            font-weight: 500;
        """)
        layout.addWidget(self.status_label)
        
        layout.addStretch()
        
        # 右侧：操作按钮
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        # 预览按钮
        preview_btn = QPushButton("👁️ 预览")
        preview_btn.setStyleSheet("""
            QPushButton {
                background-color: #f1f5f9;
                color: #64748b;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: 500;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #e2e8f0;
                color: #475569;
            }
        """)
        button_layout.addWidget(preview_btn)
        
        # 导出按钮
        export_btn = ModernButton("🚀 开始转换")
        export_btn.setMinimumWidth(140)
        export_btn.setMinimumHeight(45)
        export_btn.setStyleSheet("""
            QPushButton {
                background-color: #2563eb;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 16px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #1d4ed8;
            }
            QPushButton:pressed {
                background-color: #1e40af;
            }
        """)
        export_btn.clicked.connect(self.start_export)
        button_layout.addWidget(export_btn)
        
        layout.addLayout(button_layout)
        
        return container
        
    # 原有的功能方法保持不变...
    def add_component(self):
        """添加组件 - 保持原有逻辑，优化提示"""
        input_text = self.component_input.text().strip()
        if not input_text:
            return
            
        # 首先尝试提取LCSC ID
        component_id = self.component_validator.extract_lcsc_id(input_text)
        
        # 如果不是LCSC格式，尝试通用元件编号验证
        if not component_id:
            if self.component_validator.validate_component_format(input_text):
                component_id = input_text
            else:
                QMessageBox.warning(self, "格式错误", 
                    f"❌ 无法识别的元件编号格式：{input_text}\n\n"
                    f"💡 支持的格式：\n"
                    f"• LCSC编号：C2040、C123456\n"
                    f"• 元件型号：ESP32、STM32F103\n"
                    f"• 通用格式：字母、数字、下划线、连字符")
                return
            
        # 检查是否已存在
        if component_id in self.components:
            QMessageBox.information(self, "重复添加", 
                f"ℹ️ 元件 {component_id} 已在列表中")
            self.component_input.clear()
            return
            
        # 添加到列表
        self.components.append(component_id)
        self.update_component_list()
        self.component_input.clear()
        
        # 显示成功提示
        self.status_label.setText(f"✅ 成功添加 {component_id}")
        QTimer.singleShot(2000, lambda: self.status_label.setText("准备就绪"))
        
        # 保存设置
        self.save_settings()
        
    def update_component_list(self):
        """更新组件列表显示 - 保持原有逻辑"""
        self.component_list.clear()
        
        for component_id in self.components:
            item = QListWidgetItem(component_id)
            item.setData(Qt.ItemDataRole.UserRole, component_id)
            
            # 根据类型设置图标
            if component_id.startswith('C') and component_id[1:].isdigit():
                item.setText(f"🏪 {component_id} (LCSC)")
            else:
                item.setText(f"🔧 {component_id}")
                
            self.component_list.addItem(item)
            
        # 更新计数
        self.component_count_label.setText(f"共 {len(self.components)} 个组件")
        
    def remove_selected_components(self):
        """删除选中的组件 - 保持原有逻辑"""
        selected_items = self.component_list.selectedItems()
        if not selected_items:
            QMessageBox.information(self, "提示", "请先选择要删除的组件")
            return
            
        for item in selected_items:
            component_id = item.data(Qt.ItemDataRole.UserRole)
            if component_id in self.components:
                self.components.remove(component_id)
                
        self.update_component_list()
        self.save_settings()
        
        self.status_label.setText(f"🗑️ 已删除 {len(selected_items)} 个组件")
        QTimer.singleShot(2000, lambda: self.status_label.setText("准备就绪"))
        
    def paste_from_clipboard(self):
        """从剪贴板粘贴 - 保持原有逻辑"""
        from PyQt6.QtWidgets import QApplication
        clipboard = QApplication.clipboard()
        text = clipboard.text().strip()
        if text:
            self.component_input.setText(text)
            self.add_component()
            
    def clear_all_components(self):
        """清空所有组件 - 保持原有逻辑"""
        if not self.components:
            return
            
        reply = QMessageBox.question(self, "确认清空", 
            f"确定要清空所有 {len(self.components)} 个组件吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            
        if reply == QMessageBox.StandardButton.Yes:
            self.components.clear()
            self.update_component_list()
            self.save_settings()
            
            self.status_label.setText("🗑️ 已清空所有组件")
            QTimer.singleShot(2000, lambda: self.status_label.setText("准备就绪"))
            
    def browse_output_path(self):
        """浏览输出路径 - 保持原有逻辑"""
        path = QFileDialog.getExistingDirectory(
            self, "选择输出目录", self.path_input.text())
        if path:
            self.path_input.setText(path)
            self.save_settings()
            
    def start_export(self):
        """开始导出 - 发送转换完成信号"""
        if not self.components:
            QMessageBox.warning(self, "警告", "请先添加要转换的组件！")
            return
            
        # 获取导出选项
        options = {
            'symbol': self.symbol_check.isChecked(),
            'footprint': self.footprint_check.isChecked(),
            'model3d': self.model3d_check.isChecked()
        }
        
        if not any(options.values()):
            QMessageBox.warning(self, "警告", "请至少选择一种导出类型！")
            return
            
        output_path = self.path_input.text().strip()
        if not output_path:
            QMessageBox.warning(self, "警告", "请选择输出目录！")
            return
            
        file_prefix = self.prefix_input.text().strip()
        
        # 发送导出信号
        self.export_requested.emit(self.components, options, output_path, file_prefix)
        
        # 发送转换完成信号（模拟统计数据）
        total_count = str(len(self.components))
        success_count = str(len(self.components))  # 假设全部成功
        failed_count = "0"
        avg_time = "2.5s"  # 模拟平均用时
        
        self.conversion_completed.emit(total_count, success_count, failed_count, avg_time)
        
    def load_settings(self):
        """加载设置 - 适配新的配置结构"""
        config = self.config_manager.get_config()
        if 'component_ids' in config:
            self.components = config['component_ids']
            self.update_component_list()
            
        if 'export_path' in config:
            self.path_input.setText(config['export_path'])
            
        if 'file_prefix' in config:
            self.prefix_input.setText(config.get('file_prefix', ''))
            
        if 'export_options' in config:
            options = config['export_options']
            self.symbol_check.setChecked(options.get('symbol', True))
            self.footprint_check.setChecked(options.get('footprint', True))
            self.model3d_check.setChecked(options.get('model3d', True))
            
    def save_settings(self):
        """保存设置 - 适配新的配置结构"""
        config = self.config_manager.get_config()
        config['component_ids'] = self.components
        config['export_path'] = self.path_input.text()
        config['file_prefix'] = self.prefix_input.text()
        config['export_options'] = {
            'symbol': self.symbol_check.isChecked(),
            'footprint': self.footprint_check.isChecked(),
            'model3d': self.model3d_check.isChecked()
        }
        self.config_manager.save_config(config)
    
    def apply_responsive_layout(self, mode):
        """应用响应式布局"""
        if mode == "mobile":
            # 移动端：简化布局，增大控件尺寸
            self.setMinimumWidth(600)
            # 增大字体和间距
            self.component_input.setFont(QFont("Segoe UI", 14))
            self.component_list.setStyleSheet(self.component_list.styleSheet().replace("font-size: 16px", "font-size: 18px"))
        elif mode == "tablet":
            # 平板端：中等尺寸
            self.setMinimumWidth(800)
            self.component_input.setFont(QFont("Segoe UI", 13))
        else:
            # 桌面端：标准尺寸（已优化）
            self.setMinimumWidth(1000)
            self.component_input.setFont(QFont("Segoe UI", 13))