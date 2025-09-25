#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EasyKiConverter PyQt6 UI - 主程序入口
基于PyQt6的桌面应用程序，用于将嘉立创EDA元器件转换为KiCad格式
"""
import sys
from pathlib import Path
# 确保可以导入同级模块
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import traceback
from PyQt6.QtWidgets import QApplication, QMessageBox, QListWidgetItem
from PyQt6.QtCore import QThread, pyqtSignal

from modern_main_window import ModernMainWindow
from utils.config_manager import ConfigManager
from utils.bom_parser import BOMParser
from utils.component_validator import ComponentValidator
from core.easyeda import EasyEDAImporter, EasyedaSymbolImporter, EasyedaFootprintImporter, Easyeda3dModelImporter
from core.kicad import KiCadSymbolExporter, KiCadFootprintExporter, KiCad3DModelExporter


class ExportWorker(QThread):
    """导出工作线程"""
    
    progress_updated = pyqtSignal(int)
    status_updated = pyqtSignal(str)
    export_completed = pyqtSignal(int, int, int, str)
    export_failed = pyqtSignal(str)
    
    def __init__(self, components, export_options, output_path, lib_name):
        super().__init__()
        self.components = components
        self.export_options = export_options
        self.output_path = output_path
        self.lib_name = lib_name
        
    def run(self):
        """执行导出任务"""
        try:
            total = len(self.components)
            success_count = 0
            failed_count = 0
            
            self.status_updated.emit(f"开始转换 {total} 个元器件...")
            
            # 创建输出目录
            if not self.output_path:
                self.output_path = Path.cwd() / "output"
            else:
                self.output_path = Path(self.output_path)
                
            self.output_path.mkdir(parents=True, exist_ok=True)
            
            # 创建导出器
            importer = EasyEDAImporter()
            
            # 固定使用KiCad 6版本，高版本兼容6版本
            from core.kicad.parameters_kicad_symbol import KicadVersion
            
            # 逐个处理元件
            for i, component_id in enumerate(self.components):
                try:
                    progress = int((i + 1) / total * 100)
                    self.progress_updated.emit(progress)
                    self.status_updated.emit(f"正在转换: {component_id} ({i+1}/{total})")
                    
                    # 从EasyEDA获取数据
                    component_data = importer.import_component(component_id)
                    if not component_data:
                        failed_count += 1
                        continue
                    
                    # 导出符号
                    if self.export_options.get('symbol', True):
                        try:
                            # 检查是否有符号数据
                            if 'dataStr' in component_data:
                                symbol_data = component_data['dataStr']
                                symbol_importer = EasyedaSymbolImporter(component_data)
                                symbol = symbol_importer.get_symbol()
                                if symbol:
                                    symbol_exporter = KiCadSymbolExporter(symbol, KicadVersion.v6)
                                    # 实际导出符号到文件
                                    symbol_content = symbol_exporter.export(footprint_lib_name=self.lib_name or "easyeda_convertlib")
                                    if symbol_content:
                                        # 保存符号文件
                                        symbol_file = self.output_path / f"{self.lib_name or 'easyeda_convertlib'}.kicad_sym"
                                        with open(symbol_file, 'w', encoding='utf-8') as f:
                                            f.write(symbol_content)
                                        print(f"符号文件保存成功: {symbol_file}")
                                    else:
                                        print(f"符号导出内容为空: {component_id}")
                                else:
                                    print(f"符号数据为空: {component_id}")
                            else:
                                print(f"没有符号数据: {component_id}")
                        except Exception as e:
                            print(f"符号导出失败 {component_id}: {e}")
                    
                    # 导出封装
                    if self.export_options.get('footprint', True):
                        try:
                            # 检查是否有封装数据
                            if 'packageDetail' in component_data:
                                footprint_data = component_data['packageDetail']
                                footprint_importer = EasyedaFootprintImporter(component_data)
                                footprint = footprint_importer.get_footprint()
                                if footprint:
                                    footprint_exporter = KiCadFootprintExporter(footprint)
                                    # 实际导出封装到文件
                                    footprint_file = self.output_path / f"{component_id}.kicad_mod"
                                    model_3d_path = self.output_path / "3d_models" if self.export_options.get('model3d') else ""
                                    footprint_exporter.export(str(footprint_file), str(model_3d_path))
                                    print(f"封装文件保存成功: {footprint_file}")
                                else:
                                    print(f"封装数据为空: {component_id}")
                            else:
                                print(f"没有封装数据: {component_id}")
                        except Exception as e:
                            print(f"封装导出失败 {component_id}: {e}")
                    
                    # 导出3D模型
                    if self.export_options.get('model3d', True):
                        try:
                            # 检查是否有3D模型数据
                            if 'packageDetail' in component_data:
                                model3d_data = component_data['packageDetail']
                                # 不下载原始3D模型文件，只转换元数据
                                model3d_importer = Easyeda3dModelImporter(component_data, download_raw_3d_model=False)
                                model3d = model3d_importer.output  # 使用output属性而不是get_3d_model方法
                                if model3d:
                                    model3d_exporter = KiCad3DModelExporter(model3d)
                                    # 实际导出3D模型到文件
                                    model3d_file = self.output_path / "3d_models" / f"{component_id}.step"
                                    self.output_path.mkdir(parents=True, exist_ok=True)  # 确保目录存在
                                    (self.output_path / "3d_models").mkdir(parents=True, exist_ok=True)
                                    model3d_exporter.export(str(model3d_file))
                                    print(f"3D模型文件保存成功: {model3d_file}")
                                else:
                                    print(f"3D模型数据为空: {component_id}")
                            else:
                                print(f"没有3D模型数据: {component_id}")
                        except Exception as e:
                            print(f"3D模型导出失败 {component_id}: {e}")
                    
                    success_count += 1
                    
                except Exception as e:
                    failed_count += 1
                    print(f"转换 {component_id} 失败: {e}")
            
            # 完成导出
            avg_time = "0s"
            self.export_completed.emit(total, success_count, failed_count, avg_time)
            
        except Exception as e:
            self.export_failed.emit(str(e))


class EasyKiConverterApp(ModernMainWindow):
    """EasyKiConverter应用主窗口"""
    
    def __init__(self, config_manager: ConfigManager, parent=None):
        super().__init__(config_manager, parent)
        
        # 初始化业务逻辑组件
        self.component_validator = ComponentValidator()
        self.bom_parser = BOMParser()
        self.export_worker = None
        
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
        
        # 禁用导出按钮，显示进度条
        self.export_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.status_label.setText("正在准备转换...")
        
        # 创建工作线程
        self.export_worker = ExportWorker(components, export_options, export_path, lib_name)
        self.export_worker.progress_updated.connect(self.update_progress)
        self.export_worker.status_updated.connect(self.update_status)
        self.export_worker.export_completed.connect(self.on_export_completed)
        self.export_worker.export_failed.connect(self.on_export_failed)
        
        # 开始导出
        self.export_worker.start()
        
    def update_progress(self, value):
        """更新进度"""
        self.progress_bar.set_progress(value)
        
    def update_status(self, status):
        """更新状态"""
        self.status_label.setText(status)
        
    def on_export_completed(self, total, success, failed, avg_time):
        """导出完成"""
        self.export_btn.setEnabled(True)
        self.status_label.setText(f"转换完成！成功: {success}, 失败: {failed}")
        
        # 显示结果
        if failed > 0:
            QMessageBox.information(self, "转换完成", 
                f"转换完成！\n总数: {total}\n成功: {success}\n失败: {failed}")
        else:
            QMessageBox.information(self, "转换完成", 
                f"所有 {success} 个元器件转换成功！")
                
    def on_export_failed(self, error):
        """导出失败"""
        self.export_btn.setEnabled(True)
        self.status_label.setText("转换失败")
        QMessageBox.critical(self, "转换失败", f"转换过程中发生错误：\n{error}")


def main():
    """主函数"""
    print("🚀 正在启动 EasyKiConverter PyQt6 UI...")
    
    # 创建QApplication实例
    app = QApplication(sys.argv)
    print("✅ QApplication 创建成功")
    
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