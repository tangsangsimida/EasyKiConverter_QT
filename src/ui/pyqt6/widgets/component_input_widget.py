# -*- coding: utf-8 -*-
"""
元件输入管理组件
"""

import os

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton,
    QListWidget, QListWidgetItem, QLabel, QGroupBox, QCheckBox,
    QFileDialog, QMessageBox 
)
from PyQt6.QtCore import Qt, pyqtSignal 

from utils.bom_parser import BOMParser
from utils.component_validator import ComponentValidator


class ComponentInputWidget(QWidget):
    """元件输入管理组件"""
    
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
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(15)
        
        # 创建输入区域
        input_group = self.create_input_group()
        layout.addWidget(input_group)
        
        # 创建元件列表区域
        list_group = self.create_list_group()
        layout.addWidget(list_group)
        
        # 创建BOM导入区域
        bom_group = self.create_bom_group()
        layout.addWidget(bom_group)
        
        # 创建导出选项区域
        options_group = self.create_options_group()
        layout.addWidget(options_group)
        
        # 创建路径设置区域
        path_group = self.create_path_group()
        layout.addWidget(path_group)
        
        # 创建导出按钮
        export_layout = self.create_export_section()
        layout.addLayout(export_layout)
        
        # 添加弹簧
        layout.addStretch()
        
    def create_input_group(self) -> QGroupBox:
        """创建输入区域"""
        group = QGroupBox("添加元器件")
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #2c3e50;
            }
        """)
        
        layout = QHBoxLayout()
        layout.setSpacing(10)
        
        # 输入框
        self.component_input = QLineEdit()
        self.component_input.setPlaceholderText("输入元器件编号，例如：C2040 或 https://item.szlcsc.com/12345.html")
        self.component_input.setClearButtonEnabled(True)
        self.component_input.setStyleSheet("""
            QLineEdit {
                padding: 8px 12px;
                border: 2px solid #ddd;
                border-radius: 6px;
                font-size: 14px;
                min-height: 40px;
            }
            QLineEdit:focus {
                border-color: #3498db;
                outline: none;
            }
        """)
        self.component_input.returnPressed.connect(self.add_component)
        layout.addWidget(self.component_input)
        
        # 添加按钮
        add_btn = QPushButton("添加")
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: bold;
                min-height: 40px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
        """)
        add_btn.clicked.connect(self.add_component)
        layout.addWidget(add_btn)
        
        # 粘贴按钮
        paste_btn = QPushButton("粘贴")
        paste_btn.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                border: none;
                padding: 10px 15px;
                border-radius: 6px;
                font-weight: bold;
                min-height: 40px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        paste_btn.clicked.connect(self.paste_from_clipboard)
        layout.addWidget(paste_btn)
        
        group.setLayout(layout)
        return group
        
    def create_list_group(self) -> QGroupBox:
        """创建元件列表区域"""
        group = QGroupBox("待转换列表")
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #2c3e50;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(10)
        
        # 列表头部
        header_layout = QHBoxLayout()
        
        self.component_count_label = QLabel("共 0 个元器件")
        self.component_count_label.setStyleSheet("color: #7f8c8d; font-size: 12px;")
        header_layout.addWidget(self.component_count_label)
        
        header_layout.addStretch()
        
        # 清除按钮
        clear_btn = QPushButton("清除全部")
        clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 4px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        clear_btn.clicked.connect(self.clear_all_components)
        header_layout.addWidget(clear_btn)
        
        layout.addLayout(header_layout)
        
        # 元件列表
        self.component_list = QListWidget()
        self.component_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #ddd;
                border-radius: 6px;
                background-color: white;
                font-size: 14px;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #f0f0f0;
            }
            QListWidget::item:hover {
                background-color: #f8f9fa;
            }
            QListWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
        """)
        self.component_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.component_list.customContextMenuRequested.connect(self.show_component_menu)
        layout.addWidget(self.component_list)
        
        group.setLayout(layout)
        return group
        
    def create_bom_group(self) -> QGroupBox:
        """创建BOM导入区域"""
        group = QGroupBox("BOM文件导入（可选）")
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #2c3e50;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(10)
        
        # 文件选择区域
        file_layout = QHBoxLayout()
        
        self.bom_file_label = QLabel("未选择BOM文件")
        self.bom_file_label.setStyleSheet("color: #7f8c8d; font-size: 12px;")
        file_layout.addWidget(self.bom_file_label)
        
        file_layout.addStretch()
        
        select_file_btn = QPushButton("选择BOM文件")
        select_file_btn.setStyleSheet("""
            QPushButton {
                background-color: #9b59b6;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #8e44ad;
            }
        """)
        select_file_btn.clicked.connect(self.select_bom_file)
        file_layout.addWidget(select_file_btn)
        
        layout.addLayout(file_layout)
        
        # BOM解析结果显示
        self.bom_result_label = QLabel("")
        self.bom_result_label.setStyleSheet("color: #27ae60; font-size: 12px;")
        self.bom_result_label.setWordWrap(True)
        layout.addWidget(self.bom_result_label)
        
        group.setLayout(layout)
        return group
        
    def create_options_group(self) -> QGroupBox:
        """创建导出选项区域"""
        group = QGroupBox("导出选项")
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #2c3e50;
            }
        """)
        
        layout = QHBoxLayout()
        layout.setSpacing(20)
        
        # 符号导出选项
        self.symbol_checkbox = QCheckBox("导出原理图符号 (.kicad_sym)")
        self.symbol_checkbox.setChecked(True)
        self.symbol_checkbox.stateChanged.connect(self.update_export_options)
        layout.addWidget(self.symbol_checkbox)
        
        # 封装导出选项
        self.footprint_checkbox = QCheckBox("导出PCB封装 (.kicad_mod)")
        self.footprint_checkbox.setChecked(True)
        self.footprint_checkbox.stateChanged.connect(self.update_export_options)
        layout.addWidget(self.footprint_checkbox)
        
        # 3D模型导出选项
        self.model3d_checkbox = QCheckBox("导出3D模型 (.step/.wrl)")
        self.model3d_checkbox.setChecked(True)
        self.model3d_checkbox.stateChanged.connect(self.update_export_options)
        layout.addWidget(self.model3d_checkbox)
        
        layout.addStretch()
        
        group.setLayout(layout)
        return group
        
    def create_path_group(self) -> QGroupBox:
        """创建路径设置区域"""
        group = QGroupBox("输出设置（可选）")
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #2c3e50;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(10)
        
        # 输出路径
        path_layout = QHBoxLayout()
        
        path_label = QLabel("输出路径：")
        path_layout.addWidget(path_label)
        
        self.output_path_input = QLineEdit()
        self.output_path_input.setPlaceholderText("留空将默认保存到工作区根目录的output文件夹")
        self.output_path_input.setClearButtonEnabled(True)
        path_layout.addWidget(self.output_path_input)
        
        browse_btn = QPushButton("浏览...")
        browse_btn.clicked.connect(self.browse_output_path)
        path_layout.addWidget(browse_btn)
        
        layout.addLayout(path_layout)
        
        # 库名称
        name_layout = QHBoxLayout()
        
        name_label = QLabel("库名称：")
        name_layout.addWidget(name_label)
        
        self.lib_name_input = QLineEdit()
        self.lib_name_input.setPlaceholderText("例如：my_project，留空默认为easyeda_convertlib")
        self.lib_name_input.setClearButtonEnabled(True)
        name_layout.addWidget(self.lib_name_input)
        
        name_layout.addStretch()
        
        layout.addLayout(name_layout)
        
        group.setLayout(layout)
        return group
        
    def create_export_section(self) -> QHBoxLayout:
        """创建导出按钮区域"""
        layout = QHBoxLayout()
        layout.setSpacing(10)
        
        layout.addStretch()
        
        # 导出按钮
        self.export_btn = QPushButton("开始导出")
        self.export_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                padding: 12px 30px;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
                min-width: 150px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
            QPushButton:pressed {
                background-color: #1e8449;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
                color: #7f8c8d;
            }
        """)
        self.export_btn.clicked.connect(self.request_export)
        layout.addWidget(self.export_btn)
        
        layout.addStretch()
        
        return layout
        
    def add_component(self):
        """添加元件"""
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
                QMessageBox.warning(self, "警告", f"无法识别的元件编号格式：{input_text}\n\n支持的格式：\n• LCSC编号：C123456\n• 元件型号：CC2040、ESP32等")
                return
            
        # 检查是否已存在
        if component_id in self.components:
            QMessageBox.information(self, "提示", f"元件 {component_id} 已在列表中")
            self.component_input.clear()
            return
            
        # 添加到列表
        self.components.append(component_id)
        self.update_component_list()
        self.component_input.clear()
        
        # 保存设置
        self.save_settings()
        
    def paste_from_clipboard(self):
        """从剪贴板粘贴"""
        clipboard = QApplication.clipboard()
        text = clipboard.text().strip()
        if text:
            self.component_input.setText(text)
            self.add_component()
            
    def update_component_list(self):
        """更新元件列表显示"""
        self.component_list.clear()
        
        for component_id in self.components:
            item = QListWidgetItem(component_id)
            item.setData(Qt.ItemDataRole.UserRole, component_id)
            self.component_list.addItem(item)
            
        # 更新计数
        self.component_count_label.setText(f"共 {len(self.components)} 个元器件")
        
    def clear_all_components(self):
        """清除所有元件"""
        if not self.components:
            return
            
        reply = QMessageBox.question(
            self, "确认清除",
            f"确定要清除所有 {len(self.components)} 个元器件吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.components.clear()
            self.update_component_list()
            self.save_settings()
            
    def show_component_menu(self, position):
        """显示元件右键菜单"""
        if not self.component_list.selectedItems():
            return
            
        from PyQt6.QtWidgets import QMenu
        
        menu = QMenu()
        
        # 删除选中项
        delete_action = menu.addAction("删除选中项")
        delete_action.triggered.connect(self.delete_selected_components)
        
        # 复制到剪贴板
        copy_action = menu.addAction("复制到剪贴板")
        copy_action.triggered.connect(self.copy_selected_components)
        
        menu.exec(self.component_list.mapToGlobal(position))
        
    def delete_selected_components(self):
        """删除选中的元件"""
        selected_items = self.component_list.selectedItems()
        if not selected_items:
            return
            
        for item in selected_items:
            component_id = item.data(Qt.ItemDataRole.UserRole)
            if component_id in self.components:
                self.components.remove(component_id)
                
        self.update_component_list()
        self.save_settings()
        
    def copy_selected_components(self):
        """复制选中的元件到剪贴板"""
        selected_items = self.component_list.selectedItems()
        if not selected_items:
            return
            
        component_ids = [item.data(Qt.ItemDataRole.UserRole) for item in selected_items]
        clipboard = QApplication.clipboard()
        clipboard.setText("\n".join(component_ids))
        
    def select_bom_file(self):
        """选择BOM文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择BOM文件", "",
            "Excel文件 (*.xlsx *.xls);;CSV文件 (*.csv);;所有文件 (*.*)"
        )
        
        if file_path:
            self.import_bom_file(file_path)
            
    def import_bom_file(self, file_path: str):
        """导入BOM文件"""
        try:
            # 解析BOM文件
            result = self.bom_parser.parse_bom_file(file_path)
            
            if not result['success']:
                QMessageBox.warning(self, "BOM解析失败", result['error'])
                return
                
            component_ids = result['component_ids']
            if not component_ids:
                QMessageBox.information(self, "提示", "BOM文件中没有找到有效的元件编号")
                return
                
            # 添加到列表
            added_count = 0
            duplicate_count = 0
            
            for component_id in component_ids:
                if component_id not in self.components:
                    self.components.append(component_id)
                    added_count += 1
                else:
                    duplicate_count += 1
                    
            self.update_component_list()
            self.save_settings()
            
            # 更新BOM结果显示
            message = f"从BOM文件解析出 {len(component_ids)} 个元件编号"
            if added_count > 0:
                message += f"，新增 {added_count} 个"
            if duplicate_count > 0:
                message += f"，跳过 {duplicate_count} 个重复项"
                
            self.bom_file_label.setText(os.path.basename(file_path))
            self.bom_result_label.setText(message)
            
            QMessageBox.information(self, "BOM导入成功", message)
            
        except Exception as e:
            QMessageBox.critical(self, "BOM导入错误", f"导入BOM文件时发生错误：\n{str(e)}")
            
    def browse_output_path(self):
        """浏览输出路径"""
        path = QFileDialog.getExistingDirectory(
            self, "选择输出目录", "",
            QFileDialog.Option.ShowDirsOnly
        )
        
        if path:
            self.output_path_input.setText(path)
            self.save_settings()
            
    def update_export_options(self):
        """更新导出选项"""
        self.export_options = {
            'symbol': self.symbol_checkbox.isChecked(),
            'footprint': self.footprint_checkbox.isChecked(),
            'model3d': self.model3d_checkbox.isChecked()
        }
        
        # 确保至少选择一个选项
        if not any(self.export_options.values()):
            self.symbol_checkbox.setChecked(True)
            self.export_options['symbol'] = True
            
        self.save_settings()
        
    def request_export(self):
        """请求导出"""
        if not self.components:
            QMessageBox.warning(self, "警告", "请先添加要转换的元器件编号")
            return
            
        # 获取导出设置
        export_path = self.output_path_input.text().strip()
        lib_name = self.lib_name_input.text().strip()
        
        # 发送导出请求信号
        self.export_requested.emit(
            self.components.copy(),
            self.export_options.copy(),
            export_path,
            lib_name
        )
        
    def set_export_enabled(self, enabled: bool):
        """设置导出按钮状态"""
        self.export_btn.setEnabled(enabled)
        
    def load_settings(self):
        """加载设置"""
        try:
            settings = self.config_manager.get_last_settings()
            
            # 加载导出选项
            export_options = settings.get("export_options", self.export_options)
            self.symbol_checkbox.setChecked(export_options.get('symbol', True))
            self.footprint_checkbox.setChecked(export_options.get('footprint', True))
            self.model3d_checkbox.setChecked(export_options.get('model3d', True))
            
            # 加载路径设置
            export_path = settings.get("export_path", "")
            if export_path:
                self.output_path_input.setText(export_path)
                
            file_prefix = settings.get("file_prefix", "")
            if file_prefix:
                self.lib_name_input.setText(file_prefix)
                
            # 加载元件列表
            component_ids = settings.get("component_ids", [])
            if component_ids:
                self.components = component_ids
                self.update_component_list()
                
        except Exception as e:
            print(f"加载设置失败: {e}")
            
    def save_settings(self):
        """保存设置"""
        try:
            settings = {
                "export_options": self.export_options,
                "export_path": self.output_path_input.text().strip(),
                "file_prefix": self.lib_name_input.text().strip(),
                "component_ids": self.components
            }
            
            current_config = self.config_manager.get_last_settings()
            current_config.update(settings)
            self.config_manager.save_config(current_config)
            
        except Exception as e:
            print(f"保存设置失败: {e}")