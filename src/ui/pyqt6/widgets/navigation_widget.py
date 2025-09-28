# -*- coding: utf-8 -*-
"""
导航组件
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QFrame
from PyQt6.QtCore import Qt, pyqtSignal

class NavigationWidget(QWidget):
    """导航组件"""
    
    page_changed = pyqtSignal(str)  # 页面切换信号
    
    def __init__(self, config_manager, parent=None):
        super().__init__(parent)
        self.config_manager = config_manager
        self.current_page = "component"
        
        self.init_ui()
        
    def init_ui(self):
        """初始化用户界面"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 20, 10, 20)
        layout.setSpacing(10)
        
        # 创建导航标题
        title_label = QLabel("导航菜单")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #2c3e50;
                padding: 10px;
                background-color: #ecf0f1;
                border-radius: 6px;
                text-align: center;
            }
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # 创建导航按钮
        self.create_navigation_buttons(layout)
        
        # 添加弹簧
        layout.addStretch()
        
        # 创建底部信息
        self.create_bottom_info(layout)
        
    def create_navigation_buttons(self, layout):
        """创建导航按钮"""
        # 元件转换按钮
        self.component_btn = QPushButton("🔧 元件转换")
        self.component_btn.setCheckable(True)
        self.component_btn.setChecked(True)
        self.component_btn.setStyleSheet(self.get_button_style(True))
        self.component_btn.clicked.connect(lambda: self.switch_page("component"))
        layout.addWidget(self.component_btn)
        
        # 设置按钮
        self.settings_btn = QPushButton("⚙️ 设置")
        self.settings_btn.setCheckable(True)
        self.settings_btn.setStyleSheet(self.get_button_style(False))
        self.settings_btn.clicked.connect(lambda: self.switch_page("settings"))
        layout.addWidget(self.settings_btn)
        
        # 关于按钮
        self.about_btn = QPushButton("ℹ️ 关于")
        self.about_btn.setCheckable(True)
        self.about_btn.setStyleSheet(self.get_button_style(False))
        self.about_btn.clicked.connect(lambda: self.switch_page("about"))
        layout.addWidget(self.about_btn)
        
    def create_bottom_info(self, layout):
        """创建底部信息"""
        # 分隔线
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet("background-color: #bdc3c7;")
        layout.addWidget(separator)
        
        # 版本信息
        version_label = QLabel("EasyKiConverter v1.0.0")
        version_label.setStyleSheet("""
            QLabel {
                font-size: 11px;
                color: #7f8c8d;
                text-align: center;
                padding: 5px;
            }
        """)
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(version_label)
        
    def get_button_style(self, is_active: bool) -> str:
        """获取按钮样式"""
        if is_active:
            return """
                QPushButton {
                    background-color: #3498db;
                    color: white;
                    border: none;
                    padding: 12px 15px;
                    border-radius: 6px;
                    font-weight: bold;
                    text-align: left;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #2980b9;
                }
            """
        else:
            return """
                QPushButton {
                    background-color: #ecf0f1;
                    color: #2c3e50;
                    border: 1px solid #bdc3c7;
                    padding: 12px 15px;
                    border-radius: 6px;
                    font-weight: bold;
                    text-align: left;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #d5dbdb;
                }
            """
            
    def switch_page(self, page_name: str):
        """切换页面"""
        if self.current_page == page_name:
            return
            
        # 更新当前页面
        self.current_page = page_name
        
        # 更新按钮状态
        self.update_button_states(page_name)
        
        # 发送页面切换信号
        self.page_changed.emit(page_name)
        
    def update_button_states(self, active_page: str):
        """更新按钮状态"""
        # 重置所有按钮
        self.component_btn.setChecked(False)
        self.component_btn.setStyleSheet(self.get_button_style(False))
        
        self.settings_btn.setChecked(False)
        self.settings_btn.setStyleSheet(self.get_button_style(False))
        
        self.about_btn.setChecked(False)
        self.about_btn.setStyleSheet(self.get_button_style(False))
        
        # 激活当前页面按钮
        if active_page == "component":
            self.component_btn.setChecked(True)
            self.component_btn.setStyleSheet(self.get_button_style(True))
        elif active_page == "settings":
            self.settings_btn.setChecked(True)
            self.settings_btn.setStyleSheet(self.get_button_style(True))
        elif active_page == "about":
            self.about_btn.setChecked(True)
            self.about_btn.setStyleSheet(self.get_button_style(True))
            
    def get_current_page(self) -> str:
        """获取当前页面"""
        return self.current_page