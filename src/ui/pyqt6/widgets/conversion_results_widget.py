# -*- coding: utf-8 -*-
"""
转换结果详情组件
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt6.QtCore import Qt
from utils.modern_ui_components import ModernCard


class ConversionResultsWidget(ModernCard):
    """转换结果详情组件"""
    
    def __init__(self, parent=None):
        super().__init__("📋 转换详情", "查看每个元件的转换结果", parent)
        # 确保setup_ui只被调用一次
        if not hasattr(self, 'success_table'):
            self.setup_ui()
        
    def setup_ui(self):
        """设置UI"""
        # 避免重复调用
        if hasattr(self, 'success_table'):
            return
        
        # 确保content_layout已正确初始化
        if not hasattr(self, "content_layout") or self.content_layout is None:
            # 调用父类的setup_ui方法确保content_layout已创建
            super().setup_ui()
            
        # 创建成功结果表格
        self.success_table = self._create_results_table("✅ 成功的转换")
        
        # 创建失败结果表格
        self.failed_table = self._create_results_table("❌ 失败的转换")
        
        # 创建部分成功结果表格
        self.partial_table = self._create_results_table("⚠️ 部分成功的转换")
        
        # 添加表格到内容布局
        if hasattr(self, "content_layout") and self.content_layout is not None:
            self.content_layout.addWidget(self.success_table)
            self.content_layout.addWidget(self.failed_table)
            self.content_layout.addWidget(self.partial_table)
        else:
            print("Warning: Could not find appropriate layout for results table")
        
    def update_results(self, results):
        """
        更新结果显示
        :param results: 转换结果字典
        """
        # 清空现有数据
        self.success_table.table.setRowCount(0)
        self.failed_table.table.setRowCount(0)
        self.partial_table.table.setRowCount(0)
        
        # 添加成功结果
        for component_id in results.get("success", []):
            self._add_result_row(self.success_table.table, component_id, "✅ 成功", "")
            
        # 添加失败结果
        for item in results.get("failed", []):
            component_id = item.get("id", "Unknown")
            error_msg = item.get("error", "")
            self._add_result_row(self.failed_table.table, component_id, "❌ 失败", error_msg)
            
        # 添加部分成功结果
        for item in results.get("partial", []):
            component_id = item.get("id", "Unknown")
            message = item.get("message", "")
            self._add_result_row(self.partial_table.table, component_id, "⚠️ 部分成功", message)
            
        # 调整行高
        self.success_table.table.resizeRowsToContents()
        self.failed_table.table.resizeRowsToContents()
        self.partial_table.table.resizeRowsToContents()
        
    def _create_results_table(self, title):
        """创建结果表格"""
        # 创建标签
        label = QLabel(title)
        label.setStyleSheet("""
            font-size: 16px;
            font-weight: 600;
            color: #1e293b;
            margin-top: 15px;
            margin-bottom: 10px;
        """)
        
        # 创建表格
        table = QTableWidget()
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["元件编号", "状态", "详情"])
        table.setAlternatingRowColors(True)
        
        # 设置表格样式
        table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #e2e8f0;
                border-radius: 10px;
                background-color: white;
                gridline-color: #f1f5f9;
                font-size: 14px;
            }
            QTableWidget::item {
                padding: 10px;
                border-bottom: 1px solid #f1f5f9;
            }
            QTableWidget::item:selected {
                background-color: #dbeafe;
                color: #1e40af;
            }
            QHeaderView::section {
                background-color: #f8fafc;
                color: #475569;
                padding: 12px;
                border: none;
                font-weight: 600;
                font-size: 14px;
            }
        """)
        
        # 设置列宽
        table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        table.setColumnWidth(1, 100)
        
        # 隐藏垂直表头
        table.verticalHeader().setVisible(False)
        
        # 设置选择行为
        table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        
        # 创建一个容器部件来包含标签和表格
        container = QWidget()
        
        # 将标签和表格添加到布局中
        layout = QVBoxLayout(container)
        layout.addWidget(label)
        layout.addWidget(table)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        
        # 保存表格引用以便后续使用
        container.table = table
        
        return container
        
    def _add_result_row(self, table, component_id, status, details):
        """
        添加结果行
        :param table: 表格控件
        :param component_id: 元件编号
        :param status: 状态
        :param details: 详情
        """
        row = table.rowCount()
        table.insertRow(row)
        
        # 元件编号
        id_item = QTableWidgetItem(component_id)
        id_item.setFlags(id_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        table.setItem(row, 0, id_item)
        
        # 状态
        status_item = QTableWidgetItem(status)
        status_item.setFlags(status_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        table.setItem(row, 1, status_item)
        
        # 详情
        details_item = QTableWidgetItem(details)
        details_item.setFlags(details_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        table.setItem(row, 2, details_item)