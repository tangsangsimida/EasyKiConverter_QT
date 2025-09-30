# -*- coding: utf-8 -*-
"""
导出工作线程 - 集成EasyKiConverter核心转换逻辑
"""

import os
import sys
import time
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

from PyQt6.QtCore import QThread, pyqtSignal

# 添加src目录到Python路径，确保可以导入EasyKiConverter模块
current_dir = Path(__file__).parent
src_dir = current_dir.parent.parent
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

try:
    # 导入EasyKiConverter核心模块
    from src.core.easyeda.easyeda_api import EasyedaApi
    from src.core.easyeda.easyeda_importer import (
        Easyeda3dModelImporter,
        EasyedaFootprintImporter,
        EasyedaSymbolImporter,
    )
    from src.core.kicad.export_kicad_3d_model import Exporter3dModelKicad
    from src.core.kicad.export_kicad_footprint import ExporterFootprintKicad
    from src.core.kicad.export_kicad_symbol import ExporterSymbolKicad
    from src.core.kicad.parameters_kicad_symbol import KicadVersion
    from src.core.utils.symbol_lib_utils import add_component_in_symbol_lib_file, id_already_in_symbol_lib
    
except ImportError as e:
    print(f"导入EasyKiConverter模块失败: {e}")
    print(f"Python路径: {sys.path}")
    # 创建一个模拟的导出器用于测试
    class MockEasyKiConverter:
        def export_component(self, lcsc_id: str, export_path: str, options: Dict[str, bool], file_prefix: str) -> Dict[str, Any]:
            return {
                "success": True,
                "message": f"模拟导出成功: {lcsc_id}",
                "files": [f"{lcsc_id}_symbol.kicad_sym", f"{lcsc_id}_footprint.kicad_mod"],
                "export_path": export_path
            }


class ExportWorker(QThread):
    """导出工作线程"""
    
    # 信号定义
    progress_updated = pyqtSignal(int, int, str)  # 当前进度, 总数, 当前元件
    component_completed = pyqtSignal(dict)  # 元件转换结果
    export_finished = pyqtSignal(int, int)  # 总数, 成功数
    error_occurred = pyqtSignal(str)  # 错误信息
    
    def __init__(self, component_ids: List[str], options: Dict[str, bool], 
                 export_path: str = "", file_prefix: str = "", parent=None):
        super().__init__(parent)
        self.component_ids = component_ids
        self.options = options
        self.export_path = export_path
        self.file_prefix = file_prefix
        self.current_component = None
        self.current_position = 0
        self.total_components = 0
        self.completed_count = 0  # 已完成的元件数量
        self.completed_count_lock = threading.Lock()  # 已完成计数器锁
        
        # 多线程配置
        self.max_workers = min(len(component_ids), 16)  # 最大并发线程数
        self.file_lock = threading.Lock()  # 文件操作锁
        self.symbol_lib_locks = {}  # 符号库文件锁字典
        self.symbol_lib_locks_lock = threading.Lock()  # 符号库锁字典的锁
        
        # 日志配置
        self.logger = logging.getLogger(__name__)
        
    def get_symbol_lib_lock(self, symbol_lib_path: str) -> threading.Lock:
        """获取符号库文件的专用锁"""
        with self.symbol_lib_locks_lock:
            if symbol_lib_path not in self.symbol_lib_locks:
                self.symbol_lib_locks[symbol_lib_path] = threading.Lock()
            return self.symbol_lib_locks[symbol_lib_path]
    
    def update_progress(self, component_input: str):
        """更新进度"""
        if self.total_components > 0:
            # 确保线程安全地获取当前信息
            current_pos = self.current_position
            total_comps = self.total_components
            self.progress_updated.emit(current_pos, total_comps, component_input)
    
    def update_completed_progress(self, component_input: str):
        """更新已完成进度"""
        with self.completed_count_lock:
            self.completed_count += 1
            completed = self.completed_count
            total = self.total_components
            if total > 0:
                self.progress_updated.emit(completed, total, f"{component_input} - 完成")
    
    def extract_lcsc_id_from_url(self, url_or_id: str) -> str:
        """从输入中提取LCSC ID"""
        import re
        
        # 如果已经是LCSC ID格式，直接返回
        if re.match(r'^C\d+$', url_or_id.strip()):
            return url_or_id.strip()
        
        # 从URL中提取LCSC ID - 更全面的模式
        patterns = [
            r'item\.szlcsc\.com/(\d+)(?:\.html)?',     # 标准URL格式，带或不带.html
            r'item\.szlcsc\.com/(C\d+)(?:\.html)?',    # 带C的URL格式
            r'/(\d+)(?:\.html)?$',                     # 任何以/数字结尾的URL
            r'/(C\d+)(?:\.html)?$',                    # 任何以/C数字结尾的URL
            r'\b(C\d+)\b',                             # 任何包含C+数字的文本
            r'LCSC[:\s]*(C\d+)',                       # LCSC: C数字格式
            r'编号[:\s]*(C\d+)',                        # 编号: C数字格式
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url_or_id, re.IGNORECASE)
            if match:
                lcsc_id = match.group(1)
                # 确保以C开头
                if not lcsc_id.startswith('C'):
                    lcsc_id = 'C' + lcsc_id
                return lcsc_id
        
        return None
    
    def run(self):
        """工作线程主函数"""
        try:
            total_components = len(self.component_ids)
            success_count = 0
            
            self.logger.info(f"开始处理 {total_components} 个元器件，使用 {self.max_workers} 个线程")
            start_time = time.time()
            
            # 设置总组件数和重置完成计数
            self.total_components = total_components
            self.completed_count = 0
            
            # 根据元件数量决定是否使用多线程
            if total_components == 1:
                # 单个元件直接处理，避免线程开销
                self.current_position = 1
                self.current_component = self.component_ids[0]
                result = self.process_single_component(self.component_ids[0], 1, total_components)
                if result['success']:
                    success_count += 1
                self.component_completed.emit(result)
            else:
                # 多个元件使用线程池并行处理，线程数根据元件数量动态分配，最多16个线程
                with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                    # 提交所有任务
                    future_to_component = {
                        executor.submit(self.process_single_component, component_input, idx + 1, total_components): 
                        (component_input, idx + 1) 
                        for idx, component_input in enumerate(self.component_ids)
                    }
                    
                    # 收集结果
                    for future in as_completed(future_to_component):
                        component_input, position = future_to_component[future]
                        
                        # 更新当前处理的组件信息
                        self.current_position = position
                        self.current_component = component_input
                        
                        if self.isInterruptionRequested():
                            break
                            
                        try:
                            result = future.result()
                            if result['success']:
                                success_count += 1
                            self.component_completed.emit(result)
                            
                        except Exception as e:
                            error_result = {
                                'componentId': component_input,
                                'success': False,
                                'error': str(e),
                                'files': [],
                                'message': f'处理失败: {str(e)}',
                                'exportPath': None
                            }
                            self.component_completed.emit(error_result)
                            self.logger.error(f"处理元件 {component_input} 失败: {str(e)}")
            
            end_time = time.time()
            processing_time = end_time - start_time
            self.logger.info(f"所有元器件处理完成，耗时: {processing_time:.2f} 秒，成功: {success_count}/{total_components}")
            
            # 发送完成信号
            self.export_finished.emit(total_components, success_count)
            
        except Exception as e:
            error_msg = f"导出过程发生严重错误: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            self.error_occurred.emit(error_msg)
    
    def process_single_component(self, component_input: str, current: int, total: int) -> Dict[str, Any]:
        """处理单个元件"""
        # 设置当前组件信息
        self.current_position = current
        self.current_component = component_input
        self.total_components = total
        
        try:
            # 提取LCSC ID
            lcsc_id = self.extract_lcsc_id_from_url(component_input)
            if not lcsc_id:
                return {
                    'componentId': component_input,
                    'success': False,
                    'error': '无法从输入中提取有效的LCSC ID',
                    'files': [],
                    'message': '无法从输入中提取有效的LCSC ID',
                    'exportPath': None
                }
            
            # 调用真实的转换函数
            result = self.export_component_real(lcsc_id, self.export_path, self.options, self.file_prefix)
            
            self.logger.info(f"处理元件 {current}/{total}: {component_input}")
            
            return result
            
        except Exception as e:
            error_result = {
                'componentId': component_input,
                'success': False,
                'error': str(e),
                'files': [],
                'message': f'处理失败: {str(e)}',
                'exportPath': None
            }
            self.logger.error(f"处理元件 {component_input} 时发生异常: {str(e)}", exc_info=True)
            return error_result
    
    def export_component_real(self, lcsc_id: str, export_path: str, export_options: Dict[str, bool], file_prefix: str = None) -> Dict[str, Any]:
        """使用EasyKiConverter工具链导出元器件 - 线程安全版本"""
        try:
            files_created = []
            kicad_version = KicadVersion.v6
            
            # 初始化EasyEDA API
            easyeda_api = EasyedaApi()
            
            # 获取元器件数据
            self.logger.info(f"获取元件数据: {lcsc_id}")
            component_data = easyeda_api.get_cad_data_of_component(lcsc_id=lcsc_id)
            
            if not component_data:
                return {
                    "success": False,
                    "message": f"无法获取元件数据: {lcsc_id}",
                    "files": [],
                    "export_path": None
                }
            
            # 处理导出路径
            if not export_path or export_path.strip() == "":
                # 使用项目根目录上级目录的output文件夹
                base_folder = Path(__file__).parent.parent.parent.parent / "output"
            else:
                base_folder = Path(export_path)
                if not base_folder.is_absolute():
                    base_folder = Path.cwd() / base_folder
            
            # 使用用户提供的文件名前缀，如果没有则使用默认名称
            lib_name = file_prefix if file_prefix else "easyeda_convertlib"
            
            # 线程安全的目录创建
            with self.file_lock:
                base_folder.mkdir(parents=True, exist_ok=True)
                self.logger.info(f"创建导出目录: {base_folder}")
            
            # 创建目录结构
            footprint_dir = base_folder / f"{lib_name}.pretty"
            model_dir = base_folder / f"{lib_name}.3dshapes"
            
            with self.file_lock:
                footprint_dir.mkdir(exist_ok=True)
                model_dir.mkdir(exist_ok=True)
                self.logger.info(f"创建封装和3D模型目录")
            
            # 符号库文件路径
            lib_extension = "kicad_sym" if kicad_version == KicadVersion.v6 else "lib"
            symbol_lib_path = base_folder / f"{lib_name}.{lib_extension}"
            
            # 线程安全的符号库文件创建
            symbol_lib_lock = self.get_symbol_lib_lock(str(symbol_lib_path))
            with symbol_lib_lock:
                if not symbol_lib_path.exists():
                    with open(symbol_lib_path, "w+", encoding="utf-8") as my_lib:
                        if kicad_version == KicadVersion.v6:
                            my_lib.write(
                                """(kicad_symbol_lib
  (version 20211014)
  (generator https://github.com/tangsangsimida/EasyKiConverter)
  (generator_version \"6.0.0\")
)"""
                            )
                        else:
                            my_lib.write("EESchema-LIBRARY Version 2.4\n#encoding utf-8\n")
                    self.logger.info(f"创建符号库文件: {symbol_lib_path}")
            
            # First, process 3D models if enabled (needed for footprint 3D references)
            model_3d = None
            if export_options.get('model3d', True):
                self.logger.info(f"转换3D模型: {lcsc_id}")
                # 不在重试过程中更新进度，只在最终完成或失败时更新
                try:
                    # 尝试多次获取3D模型数据，以应对网络问题
                    model_3d_importer = None
                    success = False
                    for attempt in range(3):  # 最多尝试3次
                        model_3d_importer = Easyeda3dModelImporter(
                            easyeda_cp_cad_data=component_data, 
                            download_raw_3d_model=True
                        )
                        model_3d = model_3d_importer.output  # Use the output property directly
                        
                        if model_3d:
                            success = True
                            if attempt > 0:  # 如果不是第一次就成功，记录重试成功
                                self.logger.info(f"第{attempt + 1}次尝试成功获取3D模型数据: {lcsc_id}")
                            break  # 成功获取到3D模型，跳出循环
                        else:
                            self.logger.warning(f"第{attempt + 1}次尝试获取3D模型数据失败: {lcsc_id}")
                            if attempt < 2:  # 不是最后一次尝试，等待后重试
                                import time
                                # 限制最大等待时间为1秒，避免用户等待太久
                                wait_time = min(2 ** attempt, 1.0)
                                time.sleep(wait_time)
                    
                    if not success:
                        self.logger.warning(f"最终失败 - 未找到3D模型数据: {lcsc_id}")
                    elif model_3d:
                        self.logger.info(f"3D模型信息: name={model_3d.name}, uuid={model_3d.uuid}")
                        self.logger.info(f"3D模型数据: raw_obj={'有' if model_3d.raw_obj else '无'}, step={'有' if model_3d.step else '无'}")
                        
                        model_3d_exporter = Exporter3dModelKicad(model_3d=model_3d)
                        model_3d_exporter.export(lib_path=str(base_folder / lib_name))
                        
                        # 查找导出的3D模型文件
                        model_name = getattr(model_3d, 'name', f"{lcsc_id}_3dmodel")
                        # Sanitize model name for file system compatibility
                        import re
                        sanitized_model_name = re.sub(r'[<>:"/\|?*]', '_', model_name)
                        for ext in ['.step', '.wrl']:
                            model_file = model_dir / f"{sanitized_model_name}{ext}"
                            if model_file.exists():
                                files_created.append(str(model_file.absolute()))
                                self.logger.info(f"保存3D模型: {model_file}")
                            else:
                                self.logger.warning(f"3D模型文件未找到: {model_file}")
                        
                        # Update the model name in the 3D model object to match the sanitized name
                        # This ensures consistency between the exported file name and the reference in footprint
                        if model_3d:
                            model_3d.name = sanitized_model_name
                except Exception as e:
                    self.logger.error(f"3D模型导出失败 {lcsc_id}: {e}", exc_info=True)
            
            # 导出符号
            if export_options.get('symbol', True):
                self.logger.info(f"转换符号: {lcsc_id}")
                # 不在重试过程中更新进度，只在最终完成或失败时更新
                # 尝试多次获取符号数据，以应对网络问题
                symbol_data = None
                success = False
                for attempt in range(3):  # 最多尝试3次
                    symbol_importer = EasyedaSymbolImporter(easyeda_cp_cad_data=component_data)
                    symbol_data = symbol_importer.get_symbol()
                    
                    if symbol_data:
                        success = True
                        if attempt > 0:  # 如果不是第一次就成功，记录重试成功
                            self.logger.info(f"第{attempt + 1}次尝试成功获取符号数据: {lcsc_id}")
                        break  # 成功获取到符号数据，跳出循环
                    else:
                        self.logger.warning(f"第{attempt + 1}次尝试获取符号数据失败: {lcsc_id}")
                        if attempt < 2:  # 不是最后一次尝试，等待后重试
                            import time
                            # 限制最大等待时间为1秒，避免用户等待太久
                            wait_time = min(2 ** attempt, 1.0)
                            time.sleep(wait_time)
                
                if not success:
                    self.logger.warning(f"最终失败 - 未找到符号数据: {lcsc_id}")
                elif not symbol_data:
                    self.logger.warning(f"未找到符号数据: {lcsc_id}")
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
                            self.logger.info(f"添加符号到库文件: {symbol_data.info.name}")
                        else:
                            self.logger.info(f"符号已存在，跳过: {symbol_data.info.name}")
                    
                    files_created.append(str(symbol_lib_path.absolute()))
            
            # 导出封装 (with 3D model reference if available)
            if export_options.get('footprint', True):
                self.logger.info(f"转换封装: {lcsc_id}")
                # 不在开始时立即更新进度，而是在重试过程中更新
                # 尝试多次获取封装数据，以应对网络问题
                footprint_data = None
                success = False
                for attempt in range(3):  # 最多尝试3次
                    # 移除重试过程中的进度更新调用，避免进度条闪烁
                    # if attempt > 0:
                    #     self.update_progress(f"{lcsc_id} - 封装重试 {attempt}/3...")
                    
                    footprint_importer = EasyedaFootprintImporter(easyeda_cp_cad_data=component_data)
                    footprint_data = footprint_importer.get_footprint()
                    
                    if footprint_data:
                        success = True
                        if attempt > 0:  # 如果不是第一次就成功，记录重试成功
                            self.logger.info(f"第{attempt + 1}次尝试成功获取封装数据: {lcsc_id}")
                            # 移除重试成功时的进度更新调用
                            # self.update_progress(f"{lcsc_id} - 封装重试成功")
                        break  # 成功获取到封装数据，跳出循环
                    else:
                        self.logger.warning(f"第{attempt + 1}次尝试获取封装数据失败: {lcsc_id}")
                        if attempt < 2:  # 不是最后一次尝试，等待后重试
                            import time
                            # 限制最大等待时间为1秒，避免用户等待太久
                            wait_time = min(2 ** attempt, 1.0)
                            time.sleep(wait_time)
                
                if not success:
                    self.logger.warning(f"最终失败 - 未找到封装数据: {lcsc_id}")
                    # 移除获取失败时的进度更新调用
                    # self.update_progress(f"{lcsc_id} - 封装获取失败")
                elif not footprint_data:
                    self.logger.warning(f"未找到封装数据: {lcsc_id}")
                else:
                    footprint_exporter = ExporterFootprintKicad(footprint=footprint_data)
                    footprint_filename = footprint_dir / f"{footprint_data.info.name}.kicad_mod"
                    
                    # Set 3D model path for footprint reference
                    model_3d_path = base_folder / lib_name
                    footprint_exporter.export(
                        footprint_full_path=str(footprint_filename),
                        model_3d_path=str(model_3d_path)
                    )
                    
                    files_created.append(str(footprint_filename.absolute()))
                    self.logger.info(f"保存封装: {footprint_filename}")
            
            # 处理完成，更新最终进度
            self.update_completed_progress(f"{lcsc_id}")
            
            return {
                "success": True,
                "message": f"元件 {lcsc_id} 转换成功",
                "files": files_created,
                "export_path": str(base_folder.absolute())
            }
            
        except Exception as e:
            error_msg = f"转换失败: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            return {
                "success": False,
                "message": error_msg,
                "files": [],
                "export_path": None
            }