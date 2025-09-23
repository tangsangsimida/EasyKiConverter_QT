# -*- coding: utf-8 -*-
"""
导出工作线程 - 集成EasyKiConverter核心转换逻辑
"""

import os
import sys
import time
import threading
from pathlib import Path
from typing import List, Dict, Any, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

from PyQt6.QtCore import QThread, pyqtSignal

# 添加父目录到Python路径
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.insert(0, str(parent_dir))

# 导入EasyKiConverter核心模块
try:
    from easyeda.easyeda_api import EasyedaApi
    from easyeda.easyeda_importer import (
        Easyeda3dModelImporter,
        EasyedaFootprintImporter,
        EasyedaSymbolImporter,
    )
    from kicad.export_kicad_3d_model import Exporter3dModelKicad
    from kicad.export_kicad_footprint import ExporterFootprintKicad
    from kicad.export_kicad_symbol import ExporterSymbolKicad
    from kicad.parameters_kicad_symbol import KicadVersion
    from symbol_lib_utils import add_component_in_symbol_lib_file, id_already_in_symbol_lib
except ImportError as e:
    print(f"导入EasyKiConverter模块失败: {e}")
    print(f"Python路径: {sys.path}")
    raise


class ExportWorker(QThread):
    """导出工作线程"""
    
    # 信号定义
    progress_updated = pyqtSignal(int, int, str)  # 当前进度, 总数, 状态消息
    component_completed = pyqtSignal(dict)  # 单个元件转换结果
    export_finished = pyqtSignal(int, int)  # 总数, 成功数
    error_occurred = pyqtSignal(str)  # 错误消息
    
    def __init__(self, component_ids: List[str], options: Dict[str, bool], 
                 export_path: str = "", file_prefix: str = "", parent=None):
        super().__init__(parent)
        self.component_ids = component_ids
        self.options = options
        self.export_path = export_path
        self.file_prefix = file_prefix
        
        # 多线程配置
        self.max_workers = min(len(component_ids), 15)  # 最大并发线程数
        self.file_lock = threading.Lock()  # 文件操作锁
        self.symbol_lib_locks = {}  # 符号库文件锁字典
        self.symbol_lib_locks_lock = threading.Lock()  # 符号库锁字典的锁
        
        self.success_count = 0
        self.total_count = len(component_ids)
        
    def run(self):
        """工作线程主函数"""
        try:
            self.success_count = 0
            
            # 根据元件数量决定是否使用多线程
            if self.total_count == 1:
                # 单个元件直接处理
                self.process_single_component(self.component_ids[0], 1, 1)
            else:
                # 多个元件使用线程池并行处理
                self.process_multiple_components()
                
            # 发送完成信号
            self.export_finished.emit(self.total_count, self.success_count)
            
        except Exception as e:
            self.error_occurred.emit(f"导出过程发生错误: {str(e)}")
            
    def process_single_component(self, component_id: str, current: int, total: int):
        """处理单个元件"""
        try:
            # 更新进度
            self.progress_updated.emit(current, total, f"正在处理: {component_id}")
            
            # 执行转换
            result = self.export_component_real_threadsafe(
                component_id, self.export_path, self.options, self.file_prefix
            )
            
            # 发送结果
            self.component_completed.emit(result)
            
            # 更新成功计数
            if result.get('success', False):
                self.success_count += 1
                
        except Exception as e:
            # 发送错误结果
            error_result = {
                'componentId': component_id,
                'success': False,
                'error': str(e),
                'files': [],
                'message': f'处理失败: {str(e)}',
                'exportPath': None
            }
            self.component_completed.emit(error_result)
            
    def process_multiple_components(self):
        """使用线程池处理多个元件"""
        self.progress_updated.emit(0, self.total_count, f"开始并行处理 {self.total_count} 个元器件")
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # 提交所有任务
            future_to_component = {
                executor.submit(
                    self.export_component_real_threadsafe, 
                    component_id, self.export_path, self.options, self.file_prefix
                ): (component_id, index + 1)
                for index, component_id in enumerate(self.component_ids)
            }
            
            # 收集结果
            completed_count = 0
            for future in as_completed(future_to_component):
                component_id, sequence_num = future_to_component[future]
                completed_count += 1
                
                try:
                    # 获取结果
                    result = future.result()
                    
                    # 更新进度
                    self.progress_updated.emit(
                        completed_count, self.total_count, 
                        f"完成: {component_id} ({completed_count}/{self.total_count})"
                    )
                    
                    # 发送结果
                    self.component_completed.emit(result)
                    
                    # 更新成功计数
                    if result.get('success', False):
                        self.success_count += 1
                        
                except Exception as e:
                    # 发送错误结果
                    error_result = {
                        'componentId': component_id,
                        'success': False,
                        'error': str(e),
                        'files': [],
                        'message': f'线程执行失败: {str(e)}',
                        'exportPath': None
                    }
                    self.component_completed.emit(error_result)
                    
                    # 更新进度
                    self.progress_updated.emit(
                        completed_count, self.total_count,
                        f"失败: {component_id} ({completed_count}/{self.total_count})"
                    )
                    
    def get_symbol_lib_lock(self, symbol_lib_path: str) -> threading.Lock:
        """获取符号库文件的专用锁"""
        with self.symbol_lib_locks_lock:
            if symbol_lib_path not in self.symbol_lib_locks:
                self.symbol_lib_locks[symbol_lib_path] = threading.Lock()
            return self.symbol_lib_locks[symbol_lib_path]
            
    def export_component_real_threadsafe(self, lcsc_id: str, export_path: str, 
                                       export_options: Dict[str, bool], file_prefix: str = None) -> Dict[str, Any]:
        """线程安全版本的元器件导出函数 - 复用Web UI的核心逻辑"""
        try:
            files_created = []
            kicad_version = KicadVersion.v6
            
            # 初始化EasyEDA API
            easyeda_api = EasyedaApi()
            
            # 获取元器件数据
            print(f"正在获取元件数据: {lcsc_id}")
            component_data = easyeda_api.get_cad_data_of_component(lcsc_id=lcsc_id)
            
            if not component_data:
                return {
                    "success": False,
                    "message": f"无法获取元件数据: {lcsc_id}",
                    "files": [],
                    "export_path": None
                }
            
            # 处理导出路径
            if not export_path or export_path.strip() == '':
                # 使用项目根目录上级目录的output文件夹
                base_folder = Path(__file__).parent.parent.parent / 'output'
            else:
                base_folder = Path(export_path)
                if not base_folder.is_absolute():
                    base_folder = Path.cwd() / base_folder

            # 使用用户提供的文件名前缀，如果没有则使用默认名称
            lib_name = file_prefix if file_prefix else "easyeda_convertlib"

            # 线程安全的目录创建
            with self.file_lock:
                base_folder.mkdir(parents=True, exist_ok=True)
                print(f"创建导出目录: {base_folder}")

            # 创建目录结构
            output_base = base_folder / lib_name
            footprint_dir = output_base.with_suffix('.pretty')
            model_dir = output_base.with_suffix('.3dshapes')
            
            with self.file_lock:
                footprint_dir.mkdir(exist_ok=True)
                model_dir.mkdir(exist_ok=True)
                print(f"创建封装目录: {footprint_dir}")
                print(f"创建3D模型目录: {model_dir}")

            lib_extension = "kicad_sym" if kicad_version == KicadVersion.v6 else "lib"
            symbol_lib_path = output_base.with_suffix(f'.{lib_extension}')
            
            # 线程安全的符号库文件创建
            symbol_lib_lock = self.get_symbol_lib_lock(str(symbol_lib_path))
            with symbol_lib_lock:
                if not symbol_lib_path.exists():
                    with open(symbol_lib_path, "w+", encoding="utf-8") as my_lib:
                        my_lib.write(
                            '''(kicad_symbol_lib
  (version 20211014)
  (generator https://github.com/tangsangsimida/EasyKiConverter)
)'''
                            if kicad_version == KicadVersion.v6
                            else "EESchema-LIBRARY Version 2.4\n#encoding utf-8\n"
                        )
                    print(f"创建符号库文件: {symbol_lib_path}")
            
            # 导出符号
            if export_options.get('symbol', True):
                print(f"开始符号转换: {lcsc_id}")
                symbol_importer = EasyedaSymbolImporter(easyeda_cp_cad_data=component_data)
                symbol_data = symbol_importer.get_symbol()
                
                if not symbol_data:
                    print(f"未找到符号数据: {lcsc_id}")
                else:
                    symbol_exporter = ExporterSymbolKicad(
                        symbol=symbol_data, 
                        kicad_version=kicad_version
                    )
                    kicad_symbol_str = symbol_exporter.export(
                        footprint_lib_name=lib_name
                    )
                    
                    # 线程安全的符号库文件操作
                    with symbol_lib_lock:
                        if not id_already_in_symbol_lib(
                            lib_path=str(symbol_lib_path),
                            component_name=symbol_data.info.name,
                            kicad_version=kicad_version,
                        ):
                            add_component_in_symbol_lib_file(
                                lib_path=str(symbol_lib_path),
                                component_content=kicad_symbol_str,
                                kicad_version=kicad_version,
                            )
                            print(f"符号已添加到库: {symbol_data.info.name}")
                        else:
                            print(f"符号已存在，跳过: {symbol_data.info.name}")
                    
                    files_created.append(str(symbol_lib_path.absolute()))
            
            # 导出封装
            if export_options.get('footprint', True):
                print(f"开始封装转换: {lcsc_id}")
                footprint_importer = EasyedaFootprintImporter(easyeda_cp_cad_data=component_data)
                footprint_data = footprint_importer.get_footprint()
                
                if not footprint_data:
                    print(f"未找到封装数据: {lcsc_id}")
                else:
                    footprint_exporter = ExporterFootprintKicad(footprint=footprint_data)
                    footprint_filename = footprint_dir / f"{footprint_data.info.name}.kicad_mod"
                    
                    model_3d_path = str(output_base)  # 使用完整的用户导出路径 + lib_name
                    footprint_exporter.export(
                        footprint_full_path=str(footprint_filename),
                        model_3d_path=model_3d_path
                    )
                    
                    files_created.append(str(footprint_filename.absolute()))
                    print(f"封装已保存: {footprint_filename}")
            
            # 导出3D模型
            if export_options.get('model3d', True):
                print(f"开始3D模型转换: {lcsc_id}")
                model_3d_importer = Easyeda3dModelImporter(
                    easyeda_cp_cad_data=component_data, 
                    download_raw_3d_model=True
                )
                model_3d = model_3d_importer.create_3d_model()
                
                if not model_3d:
                    print(f"未找到3D模型数据: {lcsc_id}")
                else:
                    model_3d_exporter = Exporter3dModelKicad(model_3d=model_3d)
                    model_3d_exporter.export(lib_path=str(output_base))
                    
                    # 查找导出的3D模型文件
                    model_name = getattr(model_3d, 'name', f"{lcsc_id}_3dmodel")
                    for ext in ['.step', '.wrl']:
                        model_file = model_dir / f"{model_name}{ext}"
                        if model_file.exists():
                            files_created.append(str(model_file.absolute()))
                            print(f"3D模型已保存: {model_file}")
            
            return {
                "success": True,
                "message": f"元件 {lcsc_id} 转换成功",
                "files": files_created,
                "export_path": str(base_folder.absolute())
            }
            
        except Exception as e:
            print(f"转换失败 {lcsc_id}: {str(e)}")
            return {
                "success": False,
                "message": f"转换失败: {str(e)}",
                "files": [],
                "export_path": None
            }