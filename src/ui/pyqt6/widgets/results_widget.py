# -*- coding: utf-8 -*-
"""
结果显示组件
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGroupBox,
    QListWidget, QListWidgetItem, QPushButton, QFileDialog, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal, QUrl
from PyQt6.QtGui import QDesktopServices
from pathlib import Path
import os


class ResultsWidget(QWidget):
    """结果显示组件"""
    
    # 信号定义
    file_open_requested = pyqtSignal(str)  # 文件路径
    export_path_open_requested = pyqtSignal(str)  # 导出路径
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.results = []  # 存储所有结果
        self.export_path = ""  # 导出路径
        
        self.init_ui()
        self.hide_results()  # 初始状态隐藏
        
    def init_ui(self):
        """初始化用户界面"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(15)
        
        # 创建结果组
        results_group = QGroupBox("转换结果")
        results_group.setStyleSheet("""
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
        
        group_layout = QVBoxLayout(results_group)
        group_layout.setSpacing(15)
        
        # 结果统计区域
        stats_layout = self.create_stats_section()
        group_layout.addLayout(stats_layout)
        
        # 结果列表区域
        list_layout = self.create_results_list_section()
        group_layout.addLayout(list_layout)
        
        # 导出路径区域
        path_layout = self.create_export_path_section()
        group_layout.addLayout(path_layout)
        
        # 操作按钮区域
        action_layout = self.create_action_section()
        group_layout.addLayout(action_layout)
        
        layout.addWidget(results_group)
        
    def create_stats_section(self) -> QHBoxLayout:
        """创建统计信息区域"""
        layout = QHBoxLayout()
        layout.setSpacing(20)
        
        # 总元件数
        self.total_label = QLabel("总元件数: 0")
        self.total_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #2c3e50;
                font-weight: bold;
                padding: 8px 15px;
                background-color: #ecf0f1;
                border-radius: 6px;
            }
        """)
        layout.addWidget(self.total_label)
        
        # 成功数
        self.success_label = QLabel("成功: 0")
        self.success_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #27ae60;
                font-weight: bold;
                padding: 8px 15px;
                background-color: #d5f4e6;
                border-radius: 6px;
            }
        """)
        layout.addWidget(self.success_label)
        
        # 失败数
        self.failed_label = QLabel("失败: 0")
        self.failed_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #e74c3c;
                font-weight: bold;
                padding: 8px 15px;
                background-color: #fadbd8;
                border-radius: 6px;
            }
        """)
        layout.addWidget(self.failed_label)
        
        # 生成文件数
        self.files_label = QLabel("生成文件: 0")
        self.files_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #3498db;
                font-weight: bold;
                padding: 8px 15px;
                background-color: #ebf3fd;
                border-radius: 6px;
            }
        """)
        layout.addWidget(self.files_label)
        
        layout.addStretch()
        
        return layout
        
    def create_results_list_section(self) -> QVBoxLayout:
        """创建结果列表区域"""
        layout = QVBoxLayout()
        
        # 列表头部
        header_layout = QHBoxLayout()
        
        header_label = QLabel("详细结果:")
        header_label.setStyleSheet("font-weight: bold; color: #2c3e50;")
        header_layout.addWidget(header_label)
        
        header_layout.addStretch()
        
        # 展开/收起按钮
        self.expand_btn = QPushButton("展开全部")
        self.expand_btn.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 4px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        self.expand_btn.clicked.connect(self.toggle_expand_all)
        header_layout.addWidget(self.expand_btn)
        
        layout.addLayout(header_layout)
        
        # 结果列表
        self.results_list = QListWidget()
        self.results_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #ddd;
                border-radius: 6px;
                background-color: white;
                font-size: 13px;
            }
            QListWidget::item {
                padding: 10px;
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
        self.results_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.results_list.customContextMenuRequested.connect(self.show_context_menu)
        layout.addWidget(self.results_list)
        
        return layout
        
    def create_export_path_section(self) -> QHBoxLayout:
        """创建导出路径区域"""
        layout = QHBoxLayout()
        
        path_label = QLabel("导出路径:")
        path_label.setStyleSheet("font-weight: bold; color: #2c3e50;")
        layout.addWidget(path_label)
        
        self.path_display = QLabel("未设置")
        self.path_display.setStyleSheet("""
            QLabel {
                color: #3498db;
                font-size: 12px;
                background-color: #ebf3fd;
                padding: 5px 10px;
                border-radius: 4px;
                max-width: 400px;
            }
        """)
        self.path_display.setWordWrap(True)
        layout.addWidget(self.path_display)
        
        layout.addStretch()
        
        # 打开路径按钮
        self.open_path_btn = QPushButton("打开导出目录")
        self.open_path_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 4px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.open_path_btn.clicked.connect(self.open_export_path)
        layout.addWidget(self.open_path_btn)
        
        return layout
        
    def create_action_section(self) -> QHBoxLayout:
        """创建操作按钮区域"""
        layout = QHBoxLayout()
        layout.setSpacing(10)
        
        layout.addStretch()
        
        # 复制结果按钮
        self.copy_results_btn = QPushButton("复制结果摘要")
        self.copy_results_btn.setStyleSheet("""
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
        self.copy_results_btn.clicked.connect(self.copy_results_summary)
        layout.addWidget(self.copy_results_btn)
        
        # 保存报告按钮
        self.save_report_btn = QPushButton("保存报告")
        self.save_report_btn.setStyleSheet("""
            QPushButton {
                background-color: #e67e22;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #d35400;
            }
        """)
        self.save_report_btn.clicked.connect(self.save_report)
        layout.addWidget(self.save_report_btn)
        
        # 清空结果按钮
        self.clear_btn = QPushButton("清空结果")
        self.clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        self.clear_btn.clicked.connect(self.clear_results)
        layout.addWidget(self.clear_btn)
        
        return layout
        
    def add_result(self, result: dict):
        """添加转换结果"""
        self.results.append(result)
        
        # 创建列表项
        item = QListWidgetItem()
        item.setData(Qt.ItemDataRole.UserRole, result)
        
        # 根据结果状态设置样式
        if result.get('success', False):
            status_icon = "✅"
            status_color = "#27ae60"
            status_text = "成功"
        else:
            status_icon = "❌"
            status_color = "#e74c3c"
            status_text = "失败"
            
        component_id = result.get('componentId', '未知')
        message = result.get('message', '')
        files = result.get('files', [])
        
        # 构建显示文本
        display_text = f"{status_icon} <b>{component_id}</b> - <span style='color: {status_color};'>{status_text}</span>"
        if message:
            display_text += f"<br><span style='color: #7f8c8d; font-size: 11px;'>{message}</span>"
        if files:
            display_text += f"<br><span style='color: #3498db; font-size: 11px;'>生成 {len(files)} 个文件</span>"
            
        item.setText(display_text)
        self.results_list.addItem(item)
        
        # 更新统计信息
        self.update_stats()
        
        # 自动滚动到底部
        self.results_list.scrollToBottom()
        
    def update_stats(self):
        """更新统计信息"""
        total = len(self.results)
        success = sum(1 for r in self.results if r.get('success', False))
        failed = total - success
        
        # 计算生成的文件总数
        total_files = 0
        for result in self.results:
            files = result.get('files', [])
            if isinstance(files, list):
                total_files += len(files)
            elif isinstance(files, dict):
                total_files += len(files.get('files', []))
                
        # 更新显示
        self.total_label.setText(f"总元件数: {total}")
        self.success_label.setText(f"成功: {success}")
        self.failed_label.setText(f"失败: {failed}")
        self.files_label.setText(f"生成文件: {total_files}")
        
        # 更新导出路径
        if self.results and not self.export_path:
            last_result = self.results[-1]
            export_path = last_result.get('exportPath', '')
            if export_path:
                self.export_path = export_path
                self.path_display.setText(self.format_path(export_path))
                
    def format_path(self, path: str) -> str:
        """格式化路径显示"""
        path_obj = Path(path)
        if len(str(path_obj)) > 50:
            return f".../{path_obj.name}"
        return str(path_obj)
        
    def toggle_expand_all(self):
        """展开/收起所有结果详情"""
        # 这里可以实现展开收起功能
        # 由于QListWidget的限制，我们改为显示/隐藏详细信息
        if self.expand_btn.text() == "展开全部":
            self.expand_btn.setText("收起全部")
            # 显示详细信息逻辑
        else:
            self.expand_btn.setText("展开全部")
            # 隐藏详细信息逻辑
            
    def show_context_menu(self, position):
        """显示右键菜单"""
        if not self.results_list.selectedItems():
            return
            
        from PyQt6.QtWidgets import QMenu
        
        menu = QMenu()
        
        # 复制元件编号
        copy_id_action = menu.addAction("复制元件编号")
        copy_id_action.triggered.connect(self.copy_selected_component_id)
        
        # 复制结果详情
        copy_detail_action = menu.addAction("复制结果详情")
        copy_detail_action.triggered.connect(self.copy_selected_result_detail)
        
        # 打开导出目录
        open_path_action = menu.addAction("打开导出目录")
        open_path_action.triggered.connect(self.open_selected_export_path)
        
        menu.exec(self.results_list.mapToGlobal(position))
        
    def copy_selected_component_id(self):
        """复制选中的元件编号"""
        selected_items = self.results_list.selectedItems()
        if not selected_items:
            return
            
        component_ids = []
        for item in selected_items:
            result = item.data(Qt.ItemDataRole.UserRole)
            if result:
                component_ids.append(result.get('componentId', ''))
                
        if component_ids:
            from PyQt6.QtWidgets import QApplication
            clipboard = QApplication.clipboard()
            clipboard.setText("\n".join(component_ids))
            
    def copy_selected_result_detail(self):
        """复制选中的结果详情"""
        selected_items = self.results_list.selectedItems()
        if not selected_items:
            return
            
        details = []
        for item in selected_items:
            result = item.data(Qt.ItemDataRole.UserRole)
            if result:
                component_id = result.get('componentId', '')
                success = "成功" if result.get('success', False) else "失败"
                message = result.get('message', '')
                files = result.get('files', [])
                
                detail = f"{component_id}: {success}"
                if message:
                    detail += f" - {message}"
                if files:
                    detail += f" (生成 {len(files)} 个文件)"
                details.append(detail)
                
        if details:
            from PyQt6.QtWidgets import QApplication
            clipboard = QApplication.clipboard()
            clipboard.setText("\n".join(details))
            
    def open_selected_export_path(self):
        """打开选中的导出目录"""
        selected_items = self.results_list.selectedItems()
        if not selected_items:
            return
            
        # 使用第一个选中项的导出路径
        result = selected_items[0].data(Qt.ItemDataRole.UserRole)
        if result:
            export_path = result.get('exportPath', '')
            if export_path:
                self.open_export_path(export_path)
                
    def open_export_path(self, path: str = None):
        """打开导出目录"""
        if not path:
            path = self.export_path
            
        if path and os.path.exists(path):
            QDesktopServices.openUrl(QUrl.fromLocalFile(path))
        else:
            QMessageBox.warning(self, "警告", "导出目录不存在")
            
    def copy_results_summary(self):
        """复制结果摘要"""
        if not self.results:
            QMessageBox.information(self, "提示", "暂无转换结果")
            return
            
        total = len(self.results)
        success = sum(1 for r in self.results if r.get('success', False))
        failed = total - success
        
        # 计算文件总数
        total_files = 0
        for result in self.results:
            files = result.get('files', [])
            if isinstance(files, list):
                total_files += len(files)
            elif isinstance(files, dict):
                total_files += len(files.get('files', []))
                
        summary = f"""EasyKiConverter 转换结果摘要
========================
总元件数: {total}
成功: {success}
失败: {failed}
生成文件: {total_files}
导出路径: {self.export_path or '默认路径'}

详细结果:"""
        
        for result in self.results:
            component_id = result.get('componentId', '未知')
            success = "✅ 成功" if result.get('success', False) else "❌ 失败"
            message = result.get('message', '')
            files = result.get('files', [])
            file_count = len(files) if isinstance(files, list) else 0
            
            summary += f"\n{component_id}: {success}"
            if message:
                summary += f" - {message}"
            if file_count > 0:
                summary += f" (生成 {file_count} 个文件)"
                
        from PyQt6.QtWidgets import QApplication
        clipboard = QApplication.clipboard()
        clipboard.setText(summary)
        
        QMessageBox.information(self, "成功", "结果摘要已复制到剪贴板")
        
    def save_report(self):
        """保存详细报告"""
        if not self.results:
            QMessageBox.information(self, "提示", "暂无转换结果")
            return
            
        # 选择保存路径
        file_path, _ = QFileDialog.getSaveFileName(
            self, "保存转换报告", "conversion_report.txt",
            "文本文件 (*.txt);;所有文件 (*.*)"
        )
        
        if not file_path:
            return
            
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                # 写入报告头部
                f.write("EasyKiConverter 转换报告\n")
                f.write("=" * 50 + "\n")
                f.write(f"生成时间: {self.get_current_time()}\n")
                f.write(f"总元件数: {len(self.results)}\n")
                
                success_count = sum(1 for r in self.results if r.get('success', False))
                failed_count = len(self.results) - success_count
                f.write(f"成功: {success_count}\n")
                f.write(f"失败: {failed_count}\n")
                f.write(f"导出路径: {self.export_path or '默认路径'}\n")
                f.write("\n" + "=" * 50 + "\n\n")
                
                # 写入详细结果
                for i, result in enumerate(self.results, 1):
                    component_id = result.get('componentId', '未知')
                    success = result.get('success', False)
                    message = result.get('message', '')
                    files = result.get('files', [])
                    export_path = result.get('exportPath', '')
                    
                    f.write(f"[{i}] 元件: {component_id}\n")
                    f.write(f"状态: {'成功' if success else '失败'}\n")
                    if message:
                        f.write(f"消息: {message}\n")
                    if files:
                        f.write(f"生成文件数: {len(files)}\n")
                        if isinstance(files, list):
                            for file_path in files:
                                f.write(f"  - {os.path.basename(file_path)}\n")
                        elif isinstance(files, dict):
                            for file_info in files.get('files', []):
                                f.write(f"  - {file_info.get('name', '未知文件')}\n")
                    if export_path:
                        f.write(f"导出路径: {export_path}\n")
                    f.write("\n" + "-" * 30 + "\n\n")
                    
            QMessageBox.information(self, "成功", f"报告已保存到:\n{file_path}")
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"保存报告失败:\n{str(e)}")
            
    def clear_results(self):
        """清空结果"""
        if not self.results:
            return
            
        reply = QMessageBox.question(
            self, "确认清空",
            "确定要清空所有转换结果吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.results.clear()
            self.results_list.clear()
            self.export_path = ""
            self.update_stats()
            self.path_display.setText("未设置")
            self.hide_results()
            
    def show_results(self):
        """显示结果组件"""
        self.setVisible(True)
        
    def hide_results(self):
        """隐藏结果组件"""
        self.setVisible(False)
        
    def get_current_time(self) -> str:
        """获取当前时间字符串"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")