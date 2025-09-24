# -*- coding: utf-8 -*-
"""
主窗口类 - EasyKiConverter PyQt6 UI
"""

import sys
import os
from pathlib import Path
from typing import Dict, List, Any, Optional

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QTabWidget, QMenuBar, QStatusBar, QToolBar, QMessageBox,
    QFileDialog, QApplication, QProgressBar, QLabel, QFrame
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer, QSize
from PyQt6.QtGui import QAction, QIcon, QFont, QPalette, QColor

# 导入自定义组件
from widgets.component_input_widget import ComponentInputWidget
from widgets.progress_widget import ProgressWidget
from widgets.results_widget import ResultsWidget
from widgets.navigation_widget import NavigationWidget
from workers.export_worker import ExportWorker
from utils.config_manager import ConfigManager
from utils.style_manager import StyleManager


class MainWindow(QMainWindow):
    """主窗口类"""
    
    def __init__(self, config_manager: ConfigManager, parent=None):
        super().__init__(parent)
        self.config_manager = config_manager
        self.style_manager = StyleManager()
        self.export_worker = None
        self.current_theme = "light"
        
        self.init_ui()
        self.init_status_bar()
        self.init_menu()
        self.init_connections()
        self.load_settings()
        
    def init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle("EasyKiConverter - 嘉立创EDA转KiCad工具")
        self.setMinimumSize(1200, 800)
        self.resize(1400, 900)
        
        # 设置窗口图标
        # self.setWindowIcon(QIcon(":/icons/app_icon.png"))
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 创建导航栏
        self.navigation_widget = NavigationWidget(self.config_manager)
        self.navigation_widget.setFixedWidth(200)
        
        # 创建主工作区
        self.main_workspace = QWidget()
        workspace_layout = QVBoxLayout(self.main_workspace)
        workspace_layout.setContentsMargins(20, 20, 20, 20)
        workspace_layout.setSpacing(15)
        
        # 创建标题区域
        title_frame = self.create_title_frame()
        workspace_layout.addWidget(title_frame)
        
        # 创建标签页
        self.tab_widget = QTabWidget()
        self.tab_widget.setDocumentMode(True)
        self.tab_widget.setTabsClosable(False)
        
        # 创建各个功能页面
        self.component_page = self.create_component_page()
        self.tab_widget.addTab(self.component_page, "元件转换")
        
        workspace_layout.addWidget(self.tab_widget)
        
        # 添加到主布局
        main_layout.addWidget(self.navigation_widget)
        main_layout.addWidget(self.main_workspace)
        
        # 应用初始样式
        self.apply_theme(self.current_theme)
        
    def create_title_frame(self) -> QFrame:
        """创建标题区域"""
        title_frame = QFrame()
        title_frame.setObjectName("titleFrame")
        title_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        title_frame.setStyleSheet("""
            QFrame#titleFrame {
                background-color: #f8f9fa;
                border-radius: 8px;
                padding: 15px;
                margin-bottom: 10px;
            }
        """)
        
        title_layout = QVBoxLayout(title_frame)
        title_layout.setContentsMargins(20, 15, 20, 15)
        
        # 主标题
        title_label = QLabel("EasyKiConverter")
        title_label.setObjectName("mainTitle")
        title_label.setStyleSheet("""
            QLabel#mainTitle {
                font-size: 24px;
                font-weight: bold;
                color: #2c3e50;
                margin-bottom: 5px;
            }
        """)
        title_layout.addWidget(title_label)
        
        # 副标题
        subtitle_label = QLabel("将嘉立创EDA元器件转换为KiCad格式的便捷工具")
        subtitle_label.setObjectName("subtitle")
        subtitle_label.setStyleSheet("""
            QLabel#subtitle {
                font-size: 14px;
                color: #7f8c8d;
                margin-bottom: 10px;
            }
        """)
        title_layout.addWidget(subtitle_label)
        
        # 功能描述
        desc_label = QLabel(
            "支持符号、封装、3D模型的完整转换 | 批量处理多个元器件 | "
            "多线程并行处理 | 支持KiCad 5.x和6.x+版本"
        )
        desc_label.setObjectName("description")
        desc_label.setStyleSheet("""
            QLabel#description {
                font-size: 12px;
                color: #95a5a6;
            }
        """)
        title_layout.addWidget(desc_label)
        
        return title_frame
        
    def create_component_page(self) -> QWidget:
        """创建元件转换页面"""
        page = QWidget()
        page_layout = QVBoxLayout(page)
        page_layout.setContentsMargins(0, 0, 0, 0)
        page_layout.setSpacing(15)
        
        # 创建分割器
        splitter = QSplitter(Qt.Orientation.Vertical)
        
        # 元件输入组件
        self.component_input_widget = ComponentInputWidget(self.config_manager)
        splitter.addWidget(self.component_input_widget)
        
        # 进度显示组件
        self.progress_widget = ProgressWidget()
        splitter.addWidget(self.progress_widget)
        
        # 结果显示组件
        self.results_widget = ResultsWidget()
        splitter.addWidget(self.results_widget)
        
        # 设置分割器比例
        splitter.setStretchFactor(0, 3)  # 输入区域占3份
        splitter.setStretchFactor(1, 1)  # 进度区域占1份
        splitter.setStretchFactor(2, 2)  # 结果区域占2份
        
        page_layout.addWidget(splitter)
        
        return page
        
    def init_menu(self):
        """初始化菜单栏"""
        menubar = self.menuBar()
        
        # 文件菜单
        file_menu = menubar.addMenu("文件(&F)")
        
        # 导入BOM文件
        import_bom_action = QAction("导入BOM文件...", self)
        import_bom_action.setShortcut("Ctrl+O")
        import_bom_action.triggered.connect(self.import_bom_file)
        file_menu.addAction(import_bom_action)
        
        file_menu.addSeparator()
        
        # 退出
        exit_action = QAction("退出", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # 工具菜单
        tools_menu = menubar.addMenu("工具(&T)")
        
        # 设置
        settings_action = QAction("设置...", self)
        settings_action.setShortcut("Ctrl+,")
        settings_action.triggered.connect(self.show_settings)
        tools_menu.addAction(settings_action)
        
        # 帮助菜单
        help_menu = menubar.addMenu("帮助(&H)")
        
        # 关于
        about_action = QAction("关于", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
    def init_status_bar(self):
        """初始化状态栏"""
        self.status_bar = self.statusBar()
        
        # 状态标签
        self.status_label = QLabel("就绪")
        self.status_bar.addWidget(self.status_label)
        
        # 进度条
        self.status_progress = QProgressBar()
        self.status_progress.setVisible(False)
        self.status_progress.setFixedWidth(200)
        self.status_bar.addPermanentWidget(self.status_progress)
        
        # 主题切换按钮
        self.theme_button = QAction("🌙" if self.current_theme == "light" else "☀️", self)
        self.theme_button.triggered.connect(self.toggle_theme)
        self.status_bar.addPermanentWidget(self.create_theme_button())
        
    def create_theme_button(self) -> QWidget:
        """创建主题切换按钮"""
        button = QLabel("🌙" if self.current_theme == "light" else "☀️")
        button.setObjectName("themeButton")
        button.setStyleSheet("""
            QLabel#themeButton {
                font-size: 16px;
                padding: 5px;
                margin: 2px;
                border-radius: 4px;
            }
            QLabel#themeButton:hover {
                background-color: rgba(0, 0, 0, 0.1);
            }
        """)
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.mousePressEvent = lambda event: self.toggle_theme()
        return button
        
    def init_connections(self):
        """初始化信号连接"""
        # 连接元件输入组件的信号
        self.component_input_widget.export_requested.connect(self.start_export)
        self.component_input_widget.import_bom_requested.connect(self.import_bom_file)
        
        # 连接导航组件的信号
        if hasattr(self.navigation_widget, 'page_changed'):
            self.navigation_widget.page_changed.connect(self.switch_page)
            
    def load_settings(self):
        """加载用户设置"""
        try:
            settings = self.config_manager.get_last_settings()
            
            # 加载主题设置
            theme = settings.get("theme", "light")
            self.apply_theme(theme)
            
            # 加载窗口状态
            geometry = settings.get("window_geometry")
            if geometry:
                self.restoreGeometry(geometry)
                
            window_state = settings.get("window_state")
            if window_state:
                self.restoreState(window_state)
                
        except Exception as e:
            print(f"加载设置失败: {e}")
            
    def save_settings(self):
        """保存用户设置"""
        try:
            settings = {
                "theme": self.current_theme,
                "window_geometry": self.saveGeometry(),
                "window_state": self.saveState(),
            }
            
            # 保存到配置文件
            current_config = self.config_manager.get_last_settings()
            current_config.update(settings)
            self.config_manager.save_config(current_config)
            
        except Exception as e:
            print(f"保存设置失败: {e}")
            
    def start_export(self, component_ids: List[str], options: Dict[str, bool], 
                    export_path: str = "", file_prefix: str = ""):
        """开始导出处理"""
        if not component_ids:
            QMessageBox.warning(self, "警告", "请先添加要转换的元器件编号")
            return
            
        # 禁用导出按钮
        self.component_input_widget.set_export_enabled(False)
        
        # 清空之前的结果
        self.results_widget.clear_results()
        
        # 显示进度组件
        self.progress_widget.show_progress()
        
        # 更新状态栏
        self.status_label.setText(f"正在处理 {len(component_ids)} 个元器件...")
        self.status_progress.setVisible(True)
        self.status_progress.setRange(0, 0)  # 不确定进度
        
        # 创建并启动导出工作线程
        self.export_worker = ExportWorker(
            component_ids, options, export_path, file_prefix
        )
        
        # 连接工作线程的信号
        self.export_worker.progress_updated.connect(self.progress_widget.update_progress)
        self.export_worker.component_completed.connect(self.results_widget.add_result)
        self.export_worker.export_finished.connect(self.on_export_finished)
        self.export_worker.error_occurred.connect(self.on_export_error)
        
        # 启动工作线程
        self.export_worker.start()
        
    def on_export_finished(self, total_components: int, success_count: int):
        """导出完成处理"""
        # 重新启用导出按钮
        self.component_input_widget.set_export_enabled(True)
        
        # 隐藏进度条
        self.status_progress.setVisible(False)
        
        # 更新状态栏
        if success_count == total_components:
            self.status_label.setText(f"转换完成：成功处理 {success_count}/{total_components} 个元器件")
            QMessageBox.information(self, "成功", f"所有元器件转换完成！\n成功：{success_count}/{total_components}")
        else:
            self.status_label.setText(f"转换完成：成功 {success_count}/{total_components} 个元器件，失败 {total_components - success_count} 个")
            QMessageBox.warning(self, "完成", f"转换完成，但有部分失败\n成功：{success_count}/{total_components}\n失败：{total_components - success_count}")
            
    def on_export_error(self, error_msg: str):
        """导出错误处理"""
        self.status_label.setText("转换失败")
        QMessageBox.critical(self, "错误", f"转换过程中发生错误：\n{error_msg}")
        
    def import_bom_file(self):
        """导入BOM文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择BOM文件", "", 
            "Excel文件 (*.xlsx *.xls);;CSV文件 (*.csv);;所有文件 (*.*)"
        )
        
        if file_path:
            self.component_input_widget.import_bom_file(file_path)
            
    def show_settings(self):
        """显示设置对话框"""
        from widgets.settings_dialog import SettingsDialog
        dialog = SettingsDialog(self.config_manager, self)
        dialog.exec()
        
    def show_about(self):
        """显示关于对话框"""
        QMessageBox.about(
            self, "关于 EasyKiConverter",
            "<h3>EasyKiConverter</h3>"
            "<p>版本：1.0.0</p>"
            "<p>一个用于将嘉立创EDA元器件转换为KiCad格式的便捷工具</p>"
            "<p>支持符号、封装、3D模型的完整转换</p>"
            "<p><a href='https://github.com/tangsangsimida/EasyKiConverter'>GitHub项目</a></p>"
        )
        
    def toggle_theme(self):
        """切换主题"""
        new_theme = "dark" if self.current_theme == "light" else "light"
        self.apply_theme(new_theme)
        
    def apply_theme(self, theme: str):
        """应用主题"""
        self.current_theme = theme
        self.style_manager.apply_theme(self, theme)
        
        # 更新主题按钮图标（如果status_bar已初始化）
        if hasattr(self, 'status_bar'):
            theme_button = self.status_bar.findChild(QLabel, "themeButton")
            if theme_button:
                theme_button.setText("🌙" if theme == "light" else "☀️")
            
    def switch_page(self, page_name: str):
        """切换页面"""
        page_map = {
            "component": 0,
            "settings": 1,
            "about": 2
        }
        
        if page_name in page_map:
            self.tab_widget.setCurrentIndex(page_map[page_name])
            
    def closeEvent(self, event):
        """窗口关闭事件"""
        # 检查是否有正在进行的导出任务
        if self.export_worker and self.export_worker.isRunning():
            reply = QMessageBox.question(
                self, "确认退出",
                "有正在进行的转换任务，确定要退出吗？",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                # 停止工作线程
                self.export_worker.requestInterruption()
                self.export_worker.wait()
            else:
                event.ignore()
                return
                
        # 保存设置
        self.save_settings()
        
        # 接受关闭事件
        event.accept()