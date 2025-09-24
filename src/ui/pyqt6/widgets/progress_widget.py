# -*- coding: utf-8 -*-
"""
进度显示组件
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QProgressBar, QLabel,
    QGroupBox, QTextEdit, QFrame, QScrollArea
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QPalette, QColor


class ProgressWidget(QWidget):
    """进度显示组件"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_progress = 0
        self.total_count = 0
        self.is_active = False
        self.start_time = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_elapsed_time)
        
        self.init_ui()
        self.hide_progress()  # 初始状态隐藏
        
    def init_ui(self):
        """初始化用户界面"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        
        # 创建进度组
        progress_group = QGroupBox("转换进度")
        progress_group.setStyleSheet("""
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
        
        group_layout = QVBoxLayout(progress_group)
        group_layout.setSpacing(15)
        
        # 进度条区域
        progress_layout = QVBoxLayout()
        
        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #ddd;
                border-radius: 6px;
                text-align: center;
                height: 25px;
                font-size: 12px;
            }
            QProgressBar::chunk {
                background-color: #3498db;
                border-radius: 4px;
            }
        """)
        progress_layout.addWidget(self.progress_bar)
        
        # 进度信息标签
        self.progress_info_label = QLabel("准备开始转换...")
        self.progress_info_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #2c3e50;
                font-weight: bold;
            }
        """)
        progress_layout.addWidget(self.progress_info_label)
        
        # 统计信息
        stats_layout = QHBoxLayout()
        
        self.processed_label = QLabel("已处理: 0")
        self.processed_label.setStyleSheet("color: #7f8c8d; font-size: 12px;")
        stats_layout.addWidget(self.processed_label)
        
        self.success_label = QLabel("成功: 0")
        self.success_label.setStyleSheet("color: #27ae60; font-size: 12px;")
        stats_layout.addWidget(self.success_label)
        
        self.failed_label = QLabel("失败: 0")
        self.failed_label.setStyleSheet("color: #e74c3c; font-size: 12px;")
        stats_layout.addWidget(self.failed_label)
        
        self.elapsed_time_label = QLabel("用时: 00:00")
        self.elapsed_time_label.setStyleSheet("color: #95a5a6; font-size: 12px;")
        stats_layout.addWidget(self.elapsed_time_label)
        
        stats_layout.addStretch()
        progress_layout.addLayout(stats_layout)
        
        group_layout.addLayout(progress_layout)
        
        # 详细日志区域
        log_layout = QVBoxLayout()
        
        log_label = QLabel("详细日志:")
        log_label.setStyleSheet("font-weight: bold; color: #2c3e50;")
        log_layout.addWidget(log_label)
        
        # 日志文本区域
        self.log_text = QTextEdit()
        self.log_text.setStyleSheet("""
            QTextEdit {
                border: 1px solid #ddd;
                border-radius: 6px;
                background-color: #f8f9fa;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 11px;
                color: #2c3e50;
            }
        """)
        self.log_text.setMaximumHeight(150)
        self.log_text.setReadOnly(True)
        log_layout.addWidget(self.log_text)
        
        group_layout.addLayout(log_layout)
        
        layout.addWidget(progress_group)
        
        # 初始化统计
        self.reset_stats()
        
    def show_progress(self):
        """显示进度组件"""
        self.setVisible(True)
        self.is_active = True
        self.start_time = self.get_current_time()
        self.timer.start(1000)  # 每秒更新一次
        self.reset_stats()
        
    def hide_progress(self):
        """隐藏进度组件"""
        self.setVisible(False)
        self.is_active = False
        self.timer.stop()
        
    def update_progress(self, current: int, total: int, current_component: str):
        """更新进度"""
        self.current_progress = current
        self.total_count = total
        
        # 更新进度条
        if total > 0:
            percentage = int((current / total) * 100)
            self.progress_bar.setValue(percentage)
            self.progress_bar.setFormat(f"{percentage}% ({current}/{total})")
        else:
            self.progress_bar.setValue(0)
            self.progress_bar.setFormat("准备中...")
            
        # 更新进度信息
        self.progress_info_label.setText(f"正在处理: {current_component}")
        
        # 更新统计信息
        self.update_stats(current, total)
        
        # 添加日志
        self.add_log(f"[{current}/{total}] 处理: {current_component}")
        
    def update_stats(self, current: int, total: int):
        """更新统计信息"""
        self.processed_label.setText(f"已处理: {current}")
        
        # 计算成功和失败数量（这里需要外部提供准确数据）
        # 暂时显示处理进度
        if current > 0:
            success_rate = int((current / total) * 100) if total > 0 else 0
            self.success_label.setText(f"进度: {success_rate}%")
            self.failed_label.setText(f"剩余: {total - current}")
        
    def reset_stats(self):
        """重置统计信息"""
        self.progress_bar.setValue(0)
        self.progress_bar.setFormat("准备中...")
        self.progress_info_label.setText("准备开始转换...")
        self.processed_label.setText("已处理: 0")
        self.success_label.setText("成功: 0")
        self.failed_label.setText("失败: 0")
        self.elapsed_time_label.setText("用时: 00:00")
        self.log_text.clear()
        
    def add_log(self, message: str, log_type: str = "info"):
        """添加日志消息"""
        if not self.is_active:
            return
            
        timestamp = self.get_formatted_time()
        color_map = {
            "info": "#2c3e50",
            "success": "#27ae60",
            "warning": "#f39c12",
            "error": "#e74c3c"
        }
        
        color = color_map.get(log_type, "#2c3e50")
        log_message = f'<span style="color: {color};">[{timestamp}] {message}</span>'
        
        # 限制日志数量，避免内存溢出
        if self.log_text.document().lineCount() > 100:
            cursor = self.log_text.textCursor()
            cursor.movePosition(cursor.MoveOperation.Start)
            cursor.movePosition(cursor.MoveOperation.Down, cursor.MoveMode.MoveAnchor, 20)
            cursor.select(cursor.SelectionType.Document)
            cursor.removeSelectedText()
            
        self.log_text.append(log_message)
        
        # 自动滚动到底部
        scrollbar = self.log_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
        
    def add_success_log(self, component_id: str, file_count: int):
        """添加成功日志"""
        self.add_log(f"✅ {component_id} 转换成功，生成 {file_count} 个文件", "success")
        
    def add_error_log(self, component_id: str, error: str):
        """添加错误日志"""
        self.add_log(f"❌ {component_id} 转换失败: {error}", "error")
        
    def add_warning_log(self, message: str):
        """添加警告日志"""
        self.add_log(f"⚠️ {message}", "warning")
        
    def update_elapsed_time(self):
        """更新用时显示"""
        if self.start_time and self.is_active:
            elapsed = self.get_current_time() - self.start_time
            minutes, seconds = divmod(int(elapsed), 60)
            self.elapsed_time_label.setText(f"用时: {minutes:02d}:{seconds:02d}")
            
    def get_current_time(self):
        """获取当前时间（秒）"""
        import time
        return time.time()
        
    def get_formatted_time(self):
        """获取格式化的时间字符串"""
        from datetime import datetime
        return datetime.now().strftime("%H:%M:%S")
        
    def set_indeterminate_progress(self, active: bool = True):
        """设置不确定进度模式"""
        if active:
            self.progress_bar.setRange(0, 0)  # 不确定模式
            self.progress_bar.setFormat("处理中...")
        else:
            self.progress_bar.setRange(0, 100)  # 确定模式
            
    def complete_progress(self, success_count: int, total_count: int):
        """完成进度显示"""
        self.is_active = False
        self.timer.stop()
        
        # 更新最终状态
        self.progress_bar.setValue(100)
        self.progress_bar.setFormat(f"完成: {success_count}/{total_count}")
        
        if success_count == total_count:
            self.progress_info_label.setText("✅ 所有元件转换完成！")
            self.add_log("🎉 所有元件转换任务完成！", "success")
        else:
            self.progress_info_label.setText(f"⚠️ 转换完成，成功: {success_count}/{total_count}")
            self.add_log(f"转换任务完成，成功: {success_count}/{total_count}，失败: {total_count - success_count}", "warning")
            
        # 更新最终统计
        self.processed_label.setText(f"已处理: {total_count}")
        self.success_label.setText(f"成功: {success_count}")
        self.failed_label.setText(f"失败: {total_count - success_count}")
        
    def clear_progress(self):
        """清除进度信息"""
        self.hide_progress()
        self.reset_stats()