# -*- coding: utf-8 -*-
"""
EasyKiConverter PyQt6 UI - 主程序入口
基于PyQt6的桌面应用程序，用于将嘉立创EDA元器件转换为KiCad格式
"""
import sys
import os

import traceback
from PyQt6.QtWidgets import QApplication, QMessageBox, QListWidgetItem, QFileDialog
from PyQt6.QtGui import QIcon

from src.ui.pyqt6.modern_main_window import ModernMainWindow
from src.ui.pyqt6.utils.config_manager import ConfigManager
from src.ui.pyqt6.utils.bom_parser import BOMParser
from src.ui.pyqt6.utils.component_validator import ComponentValidator
from src.ui.pyqt6.utils.resource_utils import resource_path

# 从workers目录导入新的ExportWorker类
from src.ui.pyqt6.workers.export_worker import ExportWorker
# 导入转换结果详情组件
from src.ui.pyqt6.widgets.conversion_results_widget import ConversionResultsWidget

class EasyKiConverterApp(ModernMainWindow):
    """EasyKiConverter应用主窗口"""
    
    def __init__(self, config_manager: ConfigManager, parent=None):
        super().__init__(config_manager, parent)
        
        # 初始化业务逻辑组件
        self.component_validator = ComponentValidator()
        self.bom_parser = BOMParser()
        self.export_worker = None
        
        # 转换结果存储
        self.conversion_results = {
            "success": [],
            "failed": [],
            "partial": []
        }
        
        # 转换结果详情组件
        self.conversion_results_widget = None
        
        # 连接信号
        self.setup_business_connections()
        
    def setup_business_connections(self):
        """设置业务逻辑连接"""
        # 连接导出按钮
        self.export_btn.clicked.connect(self.start_export)
        
        # 确保导出按钮初始状态为启用（只在用户点击时进行验证）
        self.export_btn.setEnabled(True)
        
    def add_component(self):
        """添加元件（重写父类方法）"""
        input_text = self.component_input.text().strip()
        if not input_text:
            return
            
        # 严格验证元件ID格式 - 只接受以C开头的LCSC编号
        if not input_text.startswith('C'):
            QMessageBox.warning(self, "警告", 
                f"仅支持LCSC元件编号格式：{input_text}\n\n正确格式：C + 数字（例如：C2040、C123456）")
            return
            
        # 验证是否为有效的LCSC编号（C + 数字）
        if not input_text[1:].isdigit():
            QMessageBox.warning(self, "警告", 
                f"无效的LCSC编号格式：{input_text}\n\n正确格式：C + 数字（例如：C2040、C123456）")
            return
            
        # 检查是否已存在
        existing_items = []
        for i in range(self.component_list.count()):
            existing_items.append(self.component_list.item(i).text())
            
        if input_text in existing_items:
            QMessageBox.information(self, "提示", f"元件 {input_text} 已在列表中")
            self.component_input.clear()
            return
            
        # 添加到列表
        item = QListWidgetItem(input_text)
        self.component_list.addItem(item)
        self.component_input.clear()
        
        # 更新计数
        self.component_count_label.setText(f"共 {self.component_list.count()} 个元器件")
        
        # 确保导出按钮保持启用状态（只在用户点击时进行验证）
        self.export_btn.setEnabled(True)
        
    def select_bom_file(self):
        """选择BOM文件（重写父类方法）"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择BOM文件", "",
            "Excel文件 (*.xlsx *.xls);;CSV文件 (*.csv);;所有文件 (*.*)"
        )
        
        if file_path:
            self.import_bom_file(file_path)
            
    def import_bom_file(self, file_path: str):
        """导入BOM文件（仅支持元件ID）"""
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
                
            # 过滤非元件ID格式的项目（只保留C+数字格式）
            valid_component_ids = []
            invalid_items = []
            
            for component_id in component_ids:
                if component_id.startswith('C') and component_id[1:].isdigit():
                    valid_component_ids.append(component_id)
                else:
                    invalid_items.append(component_id)
            
            if not valid_component_ids:
                QMessageBox.warning(self, "BOM导入失败", 
                    "BOM文件中没有找到有效的LCSC元件编号\n\n仅支持C+数字格式（例如：C2040）")
                return
                
            # 添加到列表
            added_count = 0
            duplicate_count = 0
            
            existing_items = []
            for i in range(self.component_list.count()):
                existing_items.append(self.component_list.item(i).text())
            
            for component_id in valid_component_ids:
                if component_id not in existing_items:
                    item = QListWidgetItem(component_id)
                    self.component_list.addItem(item)
                    added_count += 1
                else:
                    duplicate_count += 1
                    
            # 更新计数
            self.component_count_label.setText(f"共 {self.component_list.count()} 个元器件")
            
            # 更新BOM结果显示
            message = f"从BOM文件解析出 {len(valid_component_ids)} 个有效元件编号"
            if len(invalid_items) > 0:
                message += f"，跳过 {len(invalid_items)} 个无效格式"
            if added_count > 0:
                message += f"，新增 {added_count} 个"
            if duplicate_count > 0:
                message += f"，跳过 {duplicate_count} 个重复项"
                
            self.bom_file_label.setText(file_path.split('/')[-1])
            self.bom_result_label.setText(message)
            
            QMessageBox.information(self, "BOM导入成功", message)
            
            # 确保导出按钮保持启用状态（只在用户点击时进行验证）
            self.export_btn.setEnabled(True)
            
        except Exception as e:
            QMessageBox.critical(self, "BOM导入错误", f"导入BOM文件时发生错误：\n{str(e)}")
            
            # 确保导出按钮保持启用状态（只在用户点击时进行验证）
            self.export_btn.setEnabled(True)
            
    def start_export(self):
        """开始导出"""
        if self.component_list.count() == 0:
            QMessageBox.warning(self, "警告", "请先添加要转换的元器件编号")
            return
            
        # 获取导出设置
        export_path = self.output_path_input.text().strip()
        lib_name = self.lib_name_input.text().strip()
        
        # 获取所有元件
        components = []
        for i in range(self.component_list.count()):
            components.append(self.component_list.item(i).text())
        
        # 获取导出选项
        export_options = {
            'symbol': self.symbol_checkbox.isChecked(),
            'footprint': self.footprint_checkbox.isChecked(),
            'model3d': self.model3d_checkbox.isChecked()
        }
        
        # 确保至少选择一个选项
        if not any(export_options.values()):
            QMessageBox.warning(self, "警告", "请至少选择一种导出类型")
            return
        
        # 禁用导出按钮，显示进度条，并重置进度
        self.export_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.set_progress(0)  # 显式设置进度为0%
        self.status_label.setText("正在准备转换...")
        
        # 创建工作线程
        self.export_worker = ExportWorker(components, export_options, export_path, lib_name)
        # 连接新的信号
        self.export_worker.progress_updated.connect(self.on_progress_updated)
        self.export_worker.component_completed.connect(self.on_component_completed)
        self.export_worker.export_finished.connect(self.on_export_finished)
        self.export_worker.error_occurred.connect(self.on_export_error)
        
        # 开始导出
        self.export_worker.start()
        
    def on_progress_updated(self, current, total, component_id):
        """更新进度"""
        # 对于并行处理，我们显示已完成的元件比例
        # 这样用户可以知道整体进度
        progress = int(current / total * 100)
        self.progress_bar.set_progress(progress)
        self.status_label.setText(f"正在转换: {component_id} ({current}/{total})")
        
    def on_component_completed(self, result):
        """单个元件转换完成"""
        # 存储转换结果
        component_id = result.get('componentId', result.get('message', 'Unknown'))
        if result['success']:
            self.conversion_results["success"].append(component_id)
        else:
            # 提取错误信息中的元件ID
            error_msg = result.get('error', 'Unknown error')
            if component_id == 'Unknown' and 'Unknown' in error_msg:
                # 尝试从错误信息中提取元件ID
                import re
                match = re.search(r'[C]\d+', error_msg)
                if match:
                    component_id = match.group(0)
            self.conversion_results["failed"].append({
                "id": component_id,
                "error": error_msg
            })
        
    def on_export_finished(self, total, success_count):
        """导出完成"""
        self.export_btn.setEnabled(True)
        
        # 计算详细统计信息
        failed_count = total - success_count
        success_rate = f"{(success_count / total * 100):.1f}%" if total > 0 else "0%"
        
        # 更新状态标签显示详细统计
        self.status_label.setText(f"转换完成！总数: {total}, 成功: {success_count}, 失败: {failed_count}, 成功率: {success_rate}")
        
        # 显示详细结果列表
        self.show_detailed_results()
        
    def show_detailed_results(self):
        """显示详细转换结果"""
        # 创建转换结果详情组件（如果尚未创建）
        if self.conversion_results_widget is None:
            self.conversion_results_widget = ConversionResultsWidget()
            # 将结果详情组件添加到滚动内容布局的底部
            from PyQt6.QtWidgets import QWidget, QScrollArea
            central_widget = self.centralWidget()
            if central_widget:
                # 找到滚动区域
                scroll_areas = central_widget.findChildren(QScrollArea)
                if scroll_areas:
                    scroll_area = scroll_areas[0]
                    scroll_content = scroll_area.widget()
                    if scroll_content and scroll_content.layout():
                        # 先移除之前的stretch
                        for i in reversed(range(scroll_content.layout().count())):
                            item = scroll_content.layout().itemAt(i)
                            if item and item.spacerItem():
                                scroll_content.layout().removeItem(item)
                        
                        # 添加转换结果详情组件
                        scroll_content.layout().addWidget(self.conversion_results_widget)
                        
                        # 添加stretch以确保详情组件位于底部
                        scroll_content.layout().addStretch()
        else:
            # 如果组件已创建，确保它可见
            if not self.conversion_results_widget.isVisible():
                self.conversion_results_widget.setVisible(True)
        
        # 更新结果显示
        self.conversion_results_widget.update_results(self.conversion_results)
        
        # 清空结果存储，为下次转换做准备
        self.conversion_results = {
            "success": [],
            "failed": [],
            "partial": []
        }
                
    def on_export_error(self, error_msg):
        """导出失败"""
        self.export_btn.setEnabled(True)
        self.status_label.setText("转换失败")
        QMessageBox.critical(self, "转换失败", f"转换过程中发生错误：\n{error_msg}")

def main():
    """主函数"""
    print("🚀 正在启动 EasyKiConverter PyQt6 UI...")
    
    # 创建QApplication实例
    app = QApplication(sys.argv)
    print("✅ QApplication 创建成功")
    
    # 设置应用程序图标
    try:
        icon_path = resource_path("resources/app_icon.ico")
        if os.path.exists(icon_path):
            app.setWindowIcon(QIcon(icon_path))
            print(f"✅ 应用程序图标设置成功: {icon_path}")
        else:
            print(f"⚠️  未找到应用程序图标文件: {icon_path}")
    except Exception as e:
        print(f"⚠️  设置应用程序图标时出错: {e}")
    
    # 设置应用程序属性（必须在创建QApplication后）
    app.setApplicationName("EasyKiConverter")
    app.setApplicationVersion("3.0.0")
    app.setOrganizationName("EasyKiConverter")
    app.setOrganizationDomain("easykiconverter.com")
    
    # 设置应用程序样式
    app.setStyle("Fusion")
    print("✅ 应用程序属性设置完成")
    
    try:
        # 初始化配置管理器
        print("📋 正在初始化配置管理器...")
        config_manager = ConfigManager()
        print("✅ 配置管理器初始化成功")
        
        # 创建并显示主窗口（使用现代化界面）
        print("🏗️ 正在创建主窗口...")
        main_window = EasyKiConverterApp(config_manager)
        
        # 为窗口设置图标
        try:
            icon_path = resource_path("resources/app_icon.ico")
            if os.path.exists(icon_path):
                main_window.setWindowIcon(QIcon(icon_path))
                print(f"✅ 窗口图标设置成功: {icon_path}")
            else:
                print(f"⚠️  未找到窗口图标文件: {icon_path}")
        except Exception as e:
            print(f"⚠️  设置窗口图标时出错: {e}")
        
        print("✅ 主窗口创建成功")
        
        main_window.show()
        print("🎉 应用程序启动成功！")
        
        # 运行应用程序事件循环
        return app.exec()
        
    except Exception as e:
        print(f"❌ 应用程序启动失败: {e}")
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())