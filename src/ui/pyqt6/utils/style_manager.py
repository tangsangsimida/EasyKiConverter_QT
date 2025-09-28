# -*- coding: utf-8 -*-
"""
样式管理器 - 管理应用程序的主题样式
"""

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPalette, QColor


class StyleManager:
    """样式管理器"""
    
    def __init__(self):
        self.current_theme = "light"
        
    def apply_theme(self, widget, theme: str):
        """应用主题到部件"""
        self.current_theme = theme
        
        if theme == "dark":
            self.apply_dark_theme(widget)
        else:
            self.apply_light_theme(widget)
            
    def apply_light_theme(self, widget):
        """应用浅色主题"""
        style_sheet = """
            /* 主窗口样式 */
            QMainWindow {
                background-color: #f8f9fa;
            }
            
            /* 组框样式 */
            QGroupBox {
                font-weight: bold;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
                color: #2c3e50;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                background-color: #f8f9fa;
            }
            
            /* 按钮样式 */
            QPushButton {
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 13px;
            }
            
            QPushButton:hover {
                opacity: 0.8;
            }
            
            QPushButton:pressed {
                padding: 9px 15px 7px 17px;
            }
            
            /* 输入框样式 */
            QLineEdit {
                padding: 8px 12px;
                border: 2px solid #ddd;
                border-radius: 6px;
                font-size: 14px;
                background-color: white;
                color: #2c3e50;
            }
            
            QLineEdit:focus {
                border-color: #3498db;
                outline: none;
            }
            
            /* 列表样式 */
            QListWidget {
                border: 1px solid #ddd;
                border-radius: 6px;
                background-color: white;
                font-size: 13px;
                color: #2c3e50;
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
            
            /* 复选框样式 */
            QCheckBox {
                font-size: 13px;
                color: #2c3e50;
                spacing: 8px;
            }
            
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 2px solid #ddd;
                border-radius: 4px;
                background-color: white;
            }
            
            QCheckBox::indicator:checked {
                background-color: #3498db;
                border-color: #3498db;
            }
            
            /* 文本编辑框样式 */
            QTextEdit {
                border: 1px solid #ddd;
                border-radius: 6px;
                background-color: #f8f9fa;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 11px;
                color: #2c3e50;
            }
            
            /* 状态栏样式 */
            QStatusBar {
                background-color: #ecf0f1;
                color: #7f8c8d;
                font-size: 12px;
            }
            
            /* 菜单栏样式 */
            QMenuBar {
                background-color: white;
                border-bottom: 1px solid #ddd;
            }
            
            QMenuBar::item {
                padding: 6px 12px;
                color: #2c3e50;
            }
            
            QMenuBar::item:selected {
                background-color: #3498db;
                color: white;
            }
            
            /* 菜单样式 */
            QMenu {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
            
            QMenu::item {
                padding: 8px 20px;
                color: #2c3e50;
            }
            
            QMenu::item:selected {
                background-color: #3498db;
                color: white;
            }
            
            /* 工具栏样式 */
            QToolBar {
                background-color: white;
                border: none;
                padding: 4px;
            }
            
            QToolBar::separator {
                width: 1px;
                background-color: #ddd;
                margin: 4px;
            }
        """
        
        widget.setStyleSheet(style_sheet)
        
        # 设置应用程序调色板
        app = QApplication.instance()
        if app:
            palette = QPalette()
            palette.setColor(QPalette.ColorRole.Window, QColor(248, 249, 250))
            palette.setColor(QPalette.ColorRole.WindowText, QColor(44, 62, 80))
            palette.setColor(QPalette.ColorRole.Base, QColor(255, 255, 255))
            palette.setColor(QPalette.ColorRole.AlternateBase, QColor(248, 249, 250))
            palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 255))
            palette.setColor(QPalette.ColorRole.ToolTipText, QColor(44, 62, 80))
            palette.setColor(QPalette.ColorRole.Text, QColor(44, 62, 80))
            palette.setColor(QPalette.ColorRole.Button, QColor(236, 240, 241))
            palette.setColor(QPalette.ColorRole.ButtonText, QColor(44, 62, 80))
            palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 255, 255))
            palette.setColor(QPalette.ColorRole.Link, QColor(52, 152, 219))
            palette.setColor(QPalette.ColorRole.Highlight, QColor(52, 152, 219))
            palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
            app.setPalette(palette)
            
    def apply_dark_theme(self, widget):
        """应用深色主题"""
        style_sheet = """
            /* 主窗口样式 */
            QMainWindow {
                background-color: #2c3e50;
            }
            
            /* 组框样式 */
            QGroupBox {
                font-weight: bold;
                border: 2px solid #34495e;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
                color: #ecf0f1;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                background-color: #2c3e50;
            }
            
            /* 按钮样式 */
            QPushButton {
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 13px;
                background-color: #34495e;
                color: #ecf0f1;
            }
            
            QPushButton:hover {
                background-color: #4a5f7a;
            }
            
            QPushButton:pressed {
                background-color: #2c3e50;
                padding: 9px 15px 7px 17px;
            }
            
            /* 输入框样式 */
            QLineEdit {
                padding: 8px 12px;
                border: 2px solid #34495e;
                border-radius: 6px;
                font-size: 14px;
                background-color: #34495e;
                color: #ecf0f1;
            }
            
            QLineEdit:focus {
                border-color: #3498db;
                outline: none;
            }
            
            /* 列表样式 */
            QListWidget {
                border: 1px solid #34495e;
                border-radius: 6px;
                background-color: #34495e;
                font-size: 13px;
                color: #ecf0f1;
            }
            
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #2c3e50;
            }
            
            QListWidget::item:hover {
                background-color: #4a5f7a;
            }
            
            QListWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
            
            /* 复选框样式 */
            QCheckBox {
                font-size: 13px;
                color: #ecf0f1;
                spacing: 8px;
            }
            
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 2px solid #34495e;
                border-radius: 4px;
                background-color: #34495e;
            }
            
            QCheckBox::indicator:checked {
                background-color: #3498db;
                border-color: #3498db;
            }
            
            /* 文本编辑框样式 */
            QTextEdit {
                border: 1px solid #34495e;
                border-radius: 6px;
                background-color: #34495e;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 11px;
                color: #ecf0f1;
            }
            
            /* 状态栏样式 */
            QStatusBar {
                background-color: #2c3e50;
                color: #bdc3c7;
                font-size: 12px;
            }
            
            /* 菜单栏样式 */
            QMenuBar {
                background-color: #34495e;
                border-bottom: 1px solid #2c3e50;
            }
            
            QMenuBar::item {
                padding: 6px 12px;
                color: #ecf0f1;
            }
            
            QMenuBar::item:selected {
                background-color: #3498db;
                color: white;
            }
            
            /* 菜单样式 */
            QMenu {
                background-color: #34495e;
                border: 1px solid #2c3e50;
                border-radius: 4px;
            }
            
            QMenu::item {
                padding: 8px 20px;
                color: #ecf0f1;
            }
            
            QMenu::item:selected {
                background-color: #3498db;
                color: white;
            }
            
            /* 工具栏样式 */
            QToolBar {
                background-color: #34495e;
                border: none;
                padding: 4px;
            }
            
            QToolBar::separator {
                width: 1px;
                background-color: #2c3e50;
                margin: 4px;
            }
        """
        
        widget.setStyleSheet(style_sheet)
        
        # 设置应用程序调色板
        app = QApplication.instance()
        if app:
            palette = QPalette()
            palette.setColor(QPalette.ColorRole.Window, QColor(44, 62, 80))
            palette.setColor(QPalette.ColorRole.WindowText, QColor(236, 240, 241))
            palette.setColor(QPalette.ColorRole.Base, QColor(52, 73, 94))
            palette.setColor(QPalette.ColorRole.AlternateBase, QColor(44, 62, 80))
            palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(52, 73, 94))
            palette.setColor(QPalette.ColorRole.ToolTipText, QColor(236, 240, 241))
            palette.setColor(QPalette.ColorRole.Text, QColor(236, 240, 241))
            palette.setColor(QPalette.ColorRole.Button, QColor(52, 73, 94))
            palette.setColor(QPalette.ColorRole.ButtonText, QColor(236, 240, 241))
            palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 255, 255))
            palette.setColor(QPalette.ColorRole.Link, QColor(52, 152, 219))
            palette.setColor(QPalette.ColorRole.Highlight, QColor(52, 152, 219))
            palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
            app.setPalette(palette)
            
    def get_current_theme(self) -> str:
        """获取当前主题"""
        return self.current_theme
        
    def get_theme_colors(self, theme: str = None) -> dict:
        """获取主题颜色"""
        if theme is None:
            theme = self.current_theme
            
        if theme == "dark":
            return {
                "primary": "#3498db",
                "secondary": "#2c3e50",
                "success": "#27ae60",
                "warning": "#f39c12",
                "error": "#e74c3c",
                "background": "#2c3e50",
                "surface": "#34495e",
                "text": "#ecf0f1",
                "text_secondary": "#bdc3c7",
                "border": "#34495e"
            }
        else:
            return {
                "primary": "#3498db",
                "secondary": "#95a5a6",
                "success": "#27ae60",
                "warning": "#f39c12",
                "error": "#e74c3c",
                "background": "#f8f9fa",
                "surface": "#ffffff",
                "text": "#2c3e50",
                "text_secondary": "#7f8c8d",
                "border": "#e0e0e0"
            }