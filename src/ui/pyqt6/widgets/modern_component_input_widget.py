#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
现代化组件输入界面
采用卡片式布局、渐变效果和现代化交互
"""

from pathlib import Path

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QListWidget, QListWidgetItem, QLabel, QCheckBox,
    QFileDialog, QMessageBox, QFrame, QProgressBar, QSplitter
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer

from src.ui.pyqt6.utils.bom_parser import BOMParser
from src.ui.pyqt6.utils.component_validator import ComponentValidator
from src.ui.pyqt6.utils.modern_style import ModernStyle, ModernButton, ModernLineEdit


class ModernComponentInputWidget(QWidget):
    """现代化组件输入界面"""
    
    # 信号定义
    export_requested = pyqtSignal(list, dict, str, str)  # 元件列表, 选项, 导出路径, 文件前缀
    import_bom_requested = pyqtSignal(str)  # BOM文件路径
    
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
        """初始化用户界面"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(25)
        
        # 标题区域
        title_section = self.create_title_section()
        main_layout.addWidget(title_section)
        
        # 主要内容区域 - 使用分割器
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # 左侧：组件输入和管理
        left_panel = self.create_left_panel()
        splitter.addWidget(left_panel)
        
        # 右侧：导出选项和预览
        right_panel = self.create_right_panel()
        splitter.addWidget(right_panel)
        
        # 设置分割器比例
        splitter.setSizes([600, 400])
        splitter.setHandleWidth(2)
        splitter.setStyleSheet("""
            QSplitter::handle {
                background-color: #e2e8f0;
            }
            QSplitter::handle:hover {
                background-color: #cbd5e1;
            }
        """)
        
        main_layout.addWidget(splitter)
        
        # 底部操作区域
        bottom_section = self.create_bottom_section()
        main_layout.addWidget(bottom_section)
        
    def create_title_section(self) -> QWidget:
        """创建标题区域"""
        container = QWidget()
        container.setObjectName("titleSection")
        container.setStyleSheet("""
            QWidget#titleSection {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                          stop:0 #f8fafc, 
                                          stop:1 #e2e8f0);
                border-radius: 16px;
                padding: 25px;
            }
        """)
        
        # 添加阴影效果
        ModernStyle.add_shadow_effect(container, blur_radius=20, offset=(0, 4))
        
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 左侧标题和描述
        text_container = QWidget()
        text_layout = QVBoxLayout(text_container)
        text_layout.setContentsMargins(0, 0, 0, 0)
        
        title = QLabel("元器件转换")
        title.setStyleSheet("""
            font-size: 24px;
            font-weight: 700;
            color: #1e293b;
            margin-bottom: 8px;
        """)
        text_layout.addWidget(title)
        
        subtitle = QLabel("支持嘉立创EDA、LCSC元器件转换为KiCad格式")
        subtitle.setStyleSheet("""
            font-size: 14px;
            color: #64748b;
            line-height: 20px;
        """)
        text_layout.addWidget(subtitle)
        
        layout.addWidget(text_container)
        layout.addStretch()
        
        # 右侧统计信息
        stats_container = QWidget()
        stats_layout = QHBoxLayout(stats_container)
        stats_layout.setSpacing(20)
        
        # 组件数量统计
        self.component_count_label = QLabel("0")
        self.component_count_label.setStyleSheet("""
            font-size: 32px;
            font-weight: 700;
            color: #2563eb;
            background: transparent;
        """)
        
        count_text = QLabel("个组件")
        count_text.setStyleSheet("""
            font-size: 14px;
            color: #64748b;
        """)
        
        count_layout = QVBoxLayout()
        count_layout.addWidget(self.component_count_label, 0, Qt.AlignmentFlag.AlignBottom)
        count_layout.addWidget(count_text, 0, Qt.AlignmentFlag.AlignTop)
        
        stats_layout.addLayout(count_layout)
        
        layout.addWidget(stats_container)
        
        return container
        
    def create_left_panel(self) -> QWidget:
        """创建左侧面板"""
        panel = QWidget()
        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(0, 0, 0, 0)
        panel_layout.setSpacing(20)
        
        # 组件输入卡片
        input_card = self.create_input_card()
        panel_layout.addWidget(input_card)
        
        # 组件列表卡片
        list_card = self.create_list_card()
        panel_layout.addWidget(list_card)
        
        return panel
        
    def create_input_card(self) -> QFrame:
        """创建输入卡片"""
        card = QFrame()
        card.setObjectName("inputCard")
        card.setStyleSheet("""
            QFrame#inputCard {
                background-color: white;
                border: 1px solid #e2e8f0;
                border-radius: 16px;
                padding: 25px;
            }
            QFrame#inputCard:hover {
                border-color: #cbd5e1;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
            }
        """)
        
        ModernStyle.add_shadow_effect(card, blur_radius=15, offset=(0, 3))
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(15)
        
        # 卡片标题
        title_layout = QHBoxLayout()
        
        icon = QLabel("🔍")
        icon.setStyleSheet("font-size: 20px;")
        title_layout.addWidget(icon)
        
        title = QLabel("添加元器件")
        title.setStyleSheet("""
            font-size: 18px;
            font-weight: 600;
            color: #1e293b;
        """)
        title_layout.addWidget(title)
        title_layout.addStretch()
        
        layout.addLayout(title_layout)
        
        # 输入区域
        input_layout = QHBoxLayout()
        input_layout.setSpacing(12)
        
        self.component_input = ModernLineEdit()
        self.component_input.setPlaceholderText("输入元器件编号，如 C2040、ESP32、STM32F103...")
        self.component_input.setMinimumHeight(50)
        self.component_input.returnPressed.connect(self.add_component)
        input_layout.addWidget(self.component_input)
        
        add_btn = ModernButton("添加")
        add_btn.setMinimumWidth(100)
        add_btn.clicked.connect(self.add_component)
        input_layout.addWidget(add_btn)
        
        layout.addLayout(input_layout)
        
        # 快捷操作
        quick_actions = QHBoxLayout()
        quick_actions.setSpacing(10)
        
        paste_btn = QPushButton("📋 从剪贴板粘贴")
        paste_btn.setStyleSheet("""
            QPushButton {
                background-color: #f1f5f9;
                color: #64748b;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 8px 16px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #e2e8f0;
                color: #475569;
            }
        """)
        paste_btn.clicked.connect(self.paste_from_clipboard)
        quick_actions.addWidget(paste_btn)
        
        clear_btn = QPushButton("🗑️ 清空")
        clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #f1f5f9;
                color: #64748b;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 8px 16px;
                font-size: 13px;
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
        
        # 格式提示
        hint_label = QLabel("💡 支持格式：C2040、C123456、ESP32、STM32F103 等")
        hint_label.setStyleSheet("""
            color: #64748b;
            font-size: 12px;
            padding-top: 10px;
        """)
        layout.addWidget(hint_label)
        
        return card
        
    def create_list_card(self) -> QFrame:
        """创建列表卡片"""
        card = QFrame()
        card.setObjectName("listCard")
        card.setStyleSheet("""
            QFrame#listCard {
                background-color: white;
                border: 1px solid #e2e8f0;
                border-radius: 16px;
                padding: 25px;
            }
            QFrame#listCard:hover {
                border-color: #cbd5e1;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
            }
        """)
        
        ModernStyle.add_shadow_effect(card, blur_radius=15, offset=(0, 3))
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(15)
        
        # 列表标题和操作
        header_layout = QHBoxLayout()
        
        title_icon = QLabel("📋")
        title_icon.setStyleSheet("font-size: 20px;")
        header_layout.addWidget(title_icon)
        
        title = QLabel("组件列表")
        title.setStyleSheet("""
            font-size: 18px;
            font-weight: 600;
            color: #1e293b;
        """)
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # 批量操作按钮
        batch_import_btn = QPushButton("📁 批量导入")
        batch_import_btn.setStyleSheet("""
            QPushButton {
                background-color: #f1f5f9;
                color: #64748b;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 6px 12px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #e2e8f0;
                color: #475569;
            }
        """)
        header_layout.addWidget(batch_import_btn)
        
        layout.addLayout(header_layout)
        
        # 组件列表
        self.component_list = QListWidget()
        self.component_list.setStyleSheet("""
            QListWidget {
                background-color: #f8fafc;
                border: 1px solid #e2e8f0;
                border-radius: 12px;
                padding: 10px;
                font-size: 14px;
            }
            QListWidget::item {
                background-color: white;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 12px;
                margin: 4px 0;
                color: #1e293b;
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
        self.component_list.setMinimumHeight(200)
        layout.addWidget(self.component_list)
        
        # 列表底部操作
        bottom_layout = QHBoxLayout()
        
        self.component_count_label = QLabel("共 0 个组件")
        self.component_count_label.setStyleSheet("""
            color: #64748b;
            font-size: 13px;
        """)
        bottom_layout.addWidget(self.component_count_label)
        
        bottom_layout.addStretch()
        
        remove_btn = QPushButton("🗑️ 删除选中")
        remove_btn.setStyleSheet("""
            QPushButton {
                background-color: #fee2e2;
                color: #dc2626;
                border: 1px solid #fecaca;
                border-radius: 8px;
                padding: 6px 12px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #fecaca;
            }
        """)
        remove_btn.clicked.connect(self.remove_selected_components)
        bottom_layout.addWidget(remove_btn)
        
        layout.addLayout(bottom_layout)
        
        return card
        
    def create_right_panel(self) -> QWidget:
        """创建右侧面板"""
        panel = QWidget()
        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(0, 0, 0, 0)
        panel_layout.setSpacing(20)
        
        # 导出选项卡片
        options_card = self.create_options_card()
        panel_layout.addWidget(options_card)
        
        # 路径设置卡片
        path_card = self.create_path_card()
        panel_layout.addWidget(path_card)
        
        panel_layout.addStretch()
        
        return panel
        
    def create_options_card(self) -> QFrame:
        """创建选项卡片"""
        card = QFrame()
        card.setObjectName("optionsCard")
        card.setStyleSheet("""
            QFrame#optionsCard {
                background-color: white;
                border: 1px solid #e2e8f0;
                border-radius: 16px;
                padding: 25px;
            }
            QFrame#optionsCard:hover {
                border-color: #cbd5e1;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
            }
        """)
        
        ModernStyle.add_shadow_effect(card, blur_radius=15, offset=(0, 3))
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(15)
        
        # 标题
        title_layout = QHBoxLayout()
        
        icon = QLabel("⚙️")
        icon.setStyleSheet("font-size: 20px;")
        title_layout.addWidget(icon)
        
        title = QLabel("导出选项")
        title.setStyleSheet("""
            font-size: 18px;
            font-weight: 600;
            color: #1e293b;
        """)
        title_layout.addWidget(title)
        title_layout.addStretch()
        
        layout.addLayout(title_layout)
        
        # 选项
        self.symbol_check = QCheckBox("📋 符号库 (.kicad_sym)")
        self.symbol_check.setChecked(True)
        self.symbol_check.setStyleSheet("""
            QCheckBox {
                font-size: 14px;
                color: #374151;
                spacing: 8px;
                padding: 8px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border-radius: 6px;
            }
        """)
        layout.addWidget(self.symbol_check)
        
        self.footprint_check = QCheckBox("📦 封装库 (.kicad_mod)")
        self.footprint_check.setChecked(True)
        self.footprint_check.setStyleSheet("""
            QCheckBox {
                font-size: 14px;
                color: #374151;
                spacing: 8px;
                padding: 8px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border-radius: 6px;
            }
        """)
        layout.addWidget(self.footprint_check)
        
        self.model3d_check = QCheckBox("🎯 3D模型 (.step/.wrl)")
        self.model3d_check.setChecked(True)
        self.model3d_check.setStyleSheet("""
            QCheckBox {
                font-size: 14px;
                color: #374151;
                spacing: 8px;
                padding: 8px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border-radius: 6px;
            }
        """)
        layout.addWidget(self.model3d_check)
        
        return card
        
    def create_path_card(self) -> QFrame:
        """创建路径卡片"""
        card = QFrame()
        card.setObjectName("pathCard")
        card.setStyleSheet("""
            QFrame#pathCard {
                background-color: white;
                border: 1px solid #e2e8f0;
                border-radius: 16px;
                padding: 25px;
            }
            QFrame#pathCard:hover {
                border-color: #cbd5e1;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
            }
        """)
        
        ModernStyle.add_shadow_effect(card, blur_radius=15, offset=(0, 3))
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(15)
        
        # 标题
        title_layout = QHBoxLayout()
        
        icon = QLabel("📁")
        icon.setStyleSheet("font-size: 20px;")
        title_layout.addWidget(icon)
        
        title = QLabel("输出设置")
        title.setStyleSheet("""
            font-size: 18px;
            font-weight: 600;
            color: #1e293b;
        """)
        title_layout.addWidget(title)
        title_layout.addStretch()
        
        layout.addLayout(title_layout)
        
        # 输出路径
        path_layout = QVBoxLayout()
        path_layout.setSpacing(8)
        
        path_label = QLabel("输出目录")
        path_label.setStyleSheet("""
            font-size: 13px;
            color: #64748b;
            font-weight: 500;
        """)
        path_layout.addWidget(path_label)
        
        path_input_layout = QHBoxLayout()
        path_input_layout.setSpacing(10)
        
        self.path_input = ModernLineEdit()
        self.path_input.setPlaceholderText("选择输出目录...")
        self.path_input.setText(str(Path.home() / "Desktop" / "KiCad_Libraries"))
        path_input_layout.addWidget(self.path_input)
        
        browse_btn = QPushButton("浏览")
        browse_btn.setStyleSheet("""
            QPushButton {
                background-color: #f1f5f9;
                color: #64748b;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 10px 16px;
                font-size: 13px;
                min-width: 60px;
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
        
        # 文件前缀
        prefix_layout = QVBoxLayout()
        prefix_layout.setSpacing(8)
        
        prefix_label = QLabel("文件前缀")
        prefix_label.setStyleSheet("""
            font-size: 13px;
            color: #64748b;
            font-weight: 500;
        """)
        prefix_layout.addWidget(prefix_label)
        
        self.prefix_input = ModernLineEdit()
        self.prefix_input.setPlaceholderText("MyLib_")
        self.prefix_input.setText("")
        prefix_layout.addWidget(self.prefix_input)
        
        layout.addLayout(prefix_layout)
        
        return card
        
    def create_bottom_section(self) -> QWidget:
        """创建底部操作区域"""
        container = QWidget()
        container.setObjectName("bottomSection")
        container.setStyleSheet("""
            QWidget#bottomSection {
                background-color: white;
                border: 1px solid #e2e8f0;
                border-radius: 16px;
                padding: 25px;
            }
        """)
        
        ModernStyle.add_shadow_effect(container, blur_radius=15, offset=(0, 3))
        
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 左侧：进度显示
        progress_container = QWidget()
        progress_layout = QVBoxLayout(progress_container)
        progress_layout.setContentsMargins(0, 0, 0, 0)
        progress_layout.setSpacing(8)
        
        self.status_label = QLabel("准备就绪")
        self.status_label.setStyleSheet("""
            font-size: 14px;
            color: #64748b;
            font-weight: 500;
        """)
        progress_layout.addWidget(self.status_label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background-color: #f1f5f9;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                height: 8px;
                text-align: center;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                          stop:0 #2563eb, 
                                          stop:1 #3b82f6);
                border-radius: 4px;
            }
        """)
        progress_layout.addWidget(self.progress_bar)
        
        layout.addWidget(progress_container)
        layout.addStretch()
        
        # 右侧：操作按钮
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)
        
        # 预览按钮
        preview_btn = QPushButton("👁️ 预览")
        preview_btn.setStyleSheet("""
            QPushButton {
                background-color: #f1f5f9;
                color: #64748b;
                border: 1px solid #e2e8f0;
                border-radius: 10px;
                padding: 12px 20px;
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
        export_btn.setMinimumHeight(50)
        export_btn.clicked.connect(self.start_export)
        button_layout.addWidget(export_btn)
        
        layout.addLayout(button_layout)
        
        return container
        
    def add_component(self):
        """添加组件（保持原有逻辑，但优化提示信息）"""
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
        """更新组件列表显示"""
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
        self.component_count_label.setText(str(len(self.components)))
        
    def remove_selected_components(self):
        """删除选中的组件"""
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
        """从剪贴板粘贴"""
        from PyQt6.QtWidgets import QApplication
        clipboard = QApplication.clipboard()
        text = clipboard.text().strip()
        if text:
            self.component_input.setText(text)
            self.add_component()
            
    def clear_all_components(self):
        """清空所有组件"""
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
        """浏览输出路径"""
        path = QFileDialog.getExistingDirectory(
            self, "选择输出目录", self.path_input.text())
        if path:
            self.path_input.setText(path)
            self.save_settings()
            
    def start_export(self):
        """开始导出"""
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
        
    def load_settings(self):
        """加载设置"""
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
        """保存设置"""
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