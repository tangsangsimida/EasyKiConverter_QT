#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EasyKiConverter Web UI - 集成真实EasyKiConverter工具链
"""

import sys
import os

# 添加父目录到 Python 路径
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import json
import tempfile
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
import concurrent.futures
import threading
import time

from flask import Flask, request, jsonify, send_file, render_template_string, send_from_directory
from flask_cors import CORS
import logging
import pandas as pd
from werkzeug.utils import secure_filename
from werkzeug.serving import WSGIRequestHandler
import warnings

# 导入EasyKiConverter的核心模块
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
    print(f"导入错误: {e}")
    print(f"当前工作目录: {os.getcwd()}")
    print(f"Python 路径: {sys.path}")
    raise

# 导入配置管理器
from config_manager import ConfigManager

# 创建Flask应用
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# 初始化配置管理器
config_manager = ConfigManager()

# 设置日志
logging.basicConfig(level=logging.INFO)

# 配置 werkzeug 日志 - 保留请求信息，但禁用开发服务器警告
werkzeug_logger = logging.getLogger('werkzeug')
werkzeug_logger.setLevel(logging.INFO)

# 创建更安全的自定义过滤器
class StrictNoWarningFilter(logging.Filter):
    def filter(self, record):
        try:
            # 尝试获取消息内容
            message = ""
            if hasattr(record, 'getMessage'):
                try:
                    message = record.getMessage()
                except:
                    pass
            
            # 检查各种可能包含警告的字段
            msg = getattr(record, 'msg', '')
            if isinstance(msg, str) and ("development server" in msg or "production deployment" in msg):
                return False
                
            if isinstance(message, str) and ("development server" in message or "production deployment" in message):
                return False
                
            return True
        except:
            # 如果过滤过程中出现任何错误，默认允许消息通过
            return True

# 应用过滤器到所有相关的日志记录器
werkzeug_logger.addFilter(StrictNoWarningFilter())
# 也应用到根日志记录器，以防警告通过其他渠道
root_logger = logging.getLogger()
root_logger.addFilter(StrictNoWarningFilter())

logger = logging.getLogger(__name__)

# 多线程配置
MAX_WORKERS = 15  # 最大并发线程数
file_lock = threading.Lock()  # 文件操作锁
symbol_lib_locks = {}  # 符号库文件锁字典
symbol_lib_locks_lock = threading.Lock()  # 符号库锁字典的锁

def get_symbol_lib_lock(symbol_lib_path: str) -> threading.Lock:
    """获取符号库文件的专用锁"""
    with symbol_lib_locks_lock:
        if symbol_lib_path not in symbol_lib_locks:
            symbol_lib_locks[symbol_lib_path] = threading.Lock()
        return symbol_lib_locks[symbol_lib_path]

def process_component_threaded(component_input: str, export_dir: str, options: Dict[str, bool], file_prefix: str) -> Dict[str, Any]:
    """多线程处理单个元器件的包装函数"""
    try:
        # 从URL中提取LCSC ID
        lcsc_id = extract_lcsc_id_from_url(component_input)
        if not lcsc_id:
            return {
                'componentId': component_input,
                'success': False,
                'error': '无法从输入中提取有效的LCSC ID',
                'files': [],
                'message': '无法从输入中提取有效的LCSC ID',
                'exportPath': None
            }
            
        # 调用线程安全的导出函数
        result = export_component_real_threadsafe(lcsc_id, export_dir, options, file_prefix)
        
        # 为每个文件添加类型和完整路径信息
        file_details = []
        for file_path in result['files']:
            file_type = 'unknown'
            if file_path.endswith('.kicad_sym') or file_path.endswith('.lib'):
                file_type = 'symbol'
            elif file_path.endswith('.kicad_mod'):
                file_type = 'footprint'
            elif file_path.endswith('.step') or file_path.endswith('.wrl'):
                file_type = 'model3d'
            
            file_details.append({
                'path': file_path,
                'type': file_type,
                'name': os.path.basename(file_path)
            })
        
        return {
            'componentId': lcsc_id,
            'success': result['success'],
            'files': file_details,
            'message': result['message'],
            'exportPath': result['export_path']
        }
        
    except Exception as e:
        logger.error(f"Thread processing error for {component_input}: {str(e)}", exc_info=True)
        return {
            'componentId': component_input,
            'success': False,
            'error': str(e),
            'files': [],
            'message': f'处理失败: {str(e)}',
            'exportPath': None
        }

def extract_lcsc_id_from_url(url_or_id: str) -> str:
    """从输入中提取LCSC ID"""
    import re
    
    # 如果已经是LCSC ID格式，直接返回
    if re.match(r'^C\d+$', url_or_id.strip()):
        return url_or_id.strip()
    
    # 从URL中提取LCSC ID
    # 支持格式：https://item.szlcsc.com/12345.html 或 https://item.szlcsc.com/C12345.html
    patterns = [
        r'item\.szlcsc\.com/(C?\d+)\.html',  # 标准URL格式
        r'item\.szlcsc\.com/(C\d+)',         # 不带.html的格式
        r'/(C\d+)(?:\.html)?$',              # 任何以/C数字结尾的URL
        r'\b(C\d+)\b'                        # 任何包含C+数字的文本
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url_or_id)
        if match:
            lcsc_id = match.group(1)
            # 确保以C开头
            if not lcsc_id.startswith('C'):
                lcsc_id = 'C' + lcsc_id
            return lcsc_id
    
    return None

# 主页路由
@app.route('/')
def index():
    """提供主页"""
    return send_from_directory('.', 'index.html')

# 静态文件路由
@app.route('/css/<path:filename>')
def css_files(filename):
    """提供CSS文件"""
    return send_from_directory('css', filename)

@app.route('/js/<path:filename>')
def js_files(filename):
    """提供JS文件"""
    return send_from_directory('js', filename)

@app.route('/imgs/<path:filename>')
def img_files(filename):
    """提供图片文件"""
    return send_from_directory('imgs', filename)

@app.route('/api/export', methods=['POST'])
def export_components():
    """处理元器件导出请求"""
    try:
        data = request.get_json()
        
        # 验证输入
        if not data or 'componentIds' not in data:
            return jsonify({
                'success': False,
                'error': '缺少componentIds参数'
            }), 400

        component_ids = data.get('componentIds', [])
        export_path = data.get('exportPath', './exports')
        options = data.get('options', {
            'symbol': True,
            'footprint': True,
            'model3d': True
        })
        file_prefix = data.get('filePrefix', '')

        if not component_ids:
            return jsonify({
                'success': False,
                'error': '请输入至少一个元器件编号或上传BOM文件',
                'error_type': 'empty_input'
            }), 400

        # 处理导出路径：如果为空则使用工作区根目录的output文件夹
        if not export_path or export_path.strip() == '':
            export_dir = Path.cwd().parent.parent / 'output'
        else:
            export_dir = Path(export_path)
            if not export_dir.is_absolute():
                export_dir = Path.cwd() / export_dir
        
        # 确保导出目录存在
        export_dir.mkdir(parents=True, exist_ok=True)

        # 根据元器件数量动态分配线程数，最多MAX_WORKERS个线程
        num_components = len(component_ids)
        num_workers = min(num_components, MAX_WORKERS)  # 线程数不超过元件数和最大线程数
        
        logger.info(f"开始并行处理 {num_components} 个元器件，使用 {num_workers} 个线程")
        start_time = time.time()
        
        all_results = []
        
        # 根据元器件数量决定是否使用多线程
        if num_components == 1:
            # 单个元器件直接处理，避免线程开销
            result = process_component_threaded(component_ids[0], str(export_dir), options, file_prefix)
            all_results.append(result)
        else:
            # 多个元器件使用线程池并行处理，线程数根据元件数量动态分配
            with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
                # 提交所有任务
                future_to_component = {
                    executor.submit(process_component_threaded, component_input, str(export_dir), options, file_prefix): component_input
                    for component_input in component_ids
                }
                
                # 收集结果
                for future in concurrent.futures.as_completed(future_to_component):
                    component_input = future_to_component[future]
                    try:
                        result = future.result()
                        all_results.append(result)
                        logger.info(f"完成处理: {component_input}")
                    except Exception as e:
                        logger.error(f"线程执行异常 {component_input}: {str(e)}", exc_info=True)
                        all_results.append({
                            'componentId': component_input,
                            'success': False,
                            'error': str(e),
                            'files': [],
                            'message': f'线程执行失败: {str(e)}',
                            'exportPath': None
                        })
        
        end_time = time.time()
        processing_time = end_time - start_time
        logger.info(f"所有元器件处理完成，耗时: {processing_time:.2f} 秒")
        
        # 保存用户设置到配置文件
        try:
            config_manager.update_last_settings(
                export_path=export_path,
                file_prefix=file_prefix,
                export_options=options,
                component_ids=component_ids
            )
            logger.info("用户设置已保存")
        except Exception as e:
            logger.warning(f"保存用户设置失败: {str(e)}")
        
        return jsonify({
            'success': True,
            'results': all_results,
            'exportPath': str(export_dir.absolute())
        })

    except Exception as e:
        logger.error(f"API error: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def export_component_real_threadsafe(lcsc_id: str, export_path: str, export_options: Dict[str, bool], file_prefix: str = None) -> Dict[str, Any]:
    """线程安全版本的元器件导出函数"""
    try:
        files_created = []
        kicad_version = KicadVersion.v6
        
        # 初始化EasyEDA API
        easyeda_api = EasyedaApi()
        
        # 获取元器件数据
        logger.info(f"Fetching component data for LCSC ID: {lcsc_id}")
        component_data = easyeda_api.get_cad_data_of_component(lcsc_id=lcsc_id)
        
        if not component_data:
            return {
                "success": False,
                "message": f"Failed to retrieve component data for LCSC ID: {lcsc_id}",
                "files": [],
                "export_path": None
            }
        
        # 使用与main.py完全一致的路径处理逻辑
        output_path = export_path
        if not os.path.isabs(output_path):
            output_path = os.path.abspath(output_path)

        # 处理导出路径：如果为空则使用项目根目录上级目录的output文件夹
        if not export_path or export_path.strip() == '':
            base_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'output')
        else:
            base_folder = output_path
            if not os.path.isabs(base_folder):
                base_folder = os.path.abspath(base_folder)

        # 使用用户提供的文件名前缀，如果没有则使用默认名称
        lib_name = file_prefix if file_prefix else "easyeda_convertlib"

        # 线程安全的目录创建
        with file_lock:
            if not os.path.isdir(base_folder):
                os.makedirs(base_folder, exist_ok=True)
                logger.info(f"Created export directory: {base_folder}")

        # 使用os.path.join确保正确的路径分隔符
        output_base = os.path.join(base_folder, lib_name)

        # 创建目录结构 - 线程安全
        footprint_dir = f"{output_base}.pretty"
        model_dir = f"{output_base}.3dshapes"
        
        with file_lock:
            if not os.path.isdir(footprint_dir):
                os.mkdir(footprint_dir)
                logger.info(f"Create {lib_name}.pretty footprint folder in {base_folder}")

            if not os.path.isdir(model_dir):
                os.mkdir(model_dir)
                logger.info(f"Create {lib_name}.3dshapes 3D model folder in {base_folder}")

        lib_extension = "kicad_sym" if kicad_version == KicadVersion.v6 else "lib"
        symbol_lib_path = f"{output_base}.{lib_extension}"
        
        # 线程安全的符号库文件创建
        symbol_lib_lock = get_symbol_lib_lock(symbol_lib_path)
        with symbol_lib_lock:
            if not os.path.isfile(symbol_lib_path):
                with open(symbol_lib_path, "w+", encoding="utf-8") as my_lib:
                    my_lib.write(
                        '''(kicad_symbol_lib
  (version 20211014)
  (generator https://github.com/tangsangsimida/EasyKiConverter)
)'''
                        if kicad_version == KicadVersion.v6
                        else "EESchema-LIBRARY Version 2.4\n#encoding utf-8\n"
                    )
                logger.info(f"Create {lib_name}.{lib_extension} symbol lib in {base_folder}")
        
        # 导出符号 - 线程安全
        if export_options.get('symbol', True):
            logger.info(f"Symbol conversion for {lcsc_id} ...")
            symbol_importer = EasyedaSymbolImporter(easyeda_cp_cad_data=component_data)
            symbol_data = symbol_importer.get_symbol()
            
            if not symbol_data:
                logger.error(f"No symbol found for component {lcsc_id}")
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
                        lib_path=symbol_lib_path,
                        component_name=symbol_data.info.name,
                        kicad_version=kicad_version,
                    ):
                        add_component_in_symbol_lib_file(
                            lib_path=symbol_lib_path,
                            component_content=kicad_symbol_str,
                            kicad_version=kicad_version,
                        )
                        logger.info(f"Symbol for {symbol_data.info.name} added to {symbol_lib_path}")
                    else:
                        logger.info(f"Symbol for {symbol_data.info.name} already exists in {symbol_lib_path}. Skipping.")
                
                files_created.append(os.path.abspath(symbol_lib_path))
                logger.info(f"Symbol saved to {symbol_lib_path}")
        
        # 导出封装 - 无需特殊锁定，每个文件独立
        if export_options.get('footprint', True):
            logger.info(f"Footprint conversion for {lcsc_id} ...")
            footprint_importer = EasyedaFootprintImporter(easyeda_cp_cad_data=component_data)
            footprint_data = footprint_importer.get_footprint()
            
            if not footprint_data:
                logger.error(f"No footprint found for component {lcsc_id}")
            else:
                footprint_exporter = ExporterFootprintKicad(footprint=footprint_data)
                footprint_filename = os.path.join(
                    footprint_dir, 
                    f"{footprint_data.info.name}.kicad_mod"
                )
                
                model_3d_path = output_base  # 使用完整的用户导出路径 + lib_name
                footprint_exporter.export(
                    footprint_full_path=footprint_filename,
                    model_3d_path=model_3d_path
                )
                
                files_created.append(os.path.abspath(footprint_filename))
                logger.info(f"Footprint saved to {footprint_filename}")
        
        # 导出3D模型 - 无需特殊锁定，每个文件独立
        if export_options.get('model3d', True):
            logger.info(f"3D model conversion for {lcsc_id} ...")
            model_3d_importer = Easyeda3dModelImporter(
                easyeda_cp_cad_data=component_data, 
                download_raw_3d_model=True
            )
            model_3d = model_3d_importer.create_3d_model()
            
            if not model_3d:
                logger.error(f"No 3D model found for component {lcsc_id}")
            else:
                model_3d_exporter = Exporter3dModelKicad(model_3d=model_3d)
                model_3d_exporter.export(lib_path=output_base)
                
                # 查找导出的3D模型文件
                model_name = getattr(model_3d, 'name', f"{lcsc_id}_3dmodel")
                for ext in ['.step', '.wrl']:
                    model_file = os.path.join(model_dir, f"{model_name}{ext}")
                    if os.path.exists(model_file):
                        files_created.append(os.path.abspath(model_file))
                        logger.info(f"3D model saved to {model_file}")
        
        return {
            "success": True,
            "message": f"Component {lcsc_id} exported successfully",
            "files": files_created,
            "export_path": str(Path(base_folder).absolute())
        }
        
    except Exception as e:
        logger.error(f"Export failed for {lcsc_id}: {str(e)}", exc_info=True)
        return {
            "success": False,
            "message": f"Export failed: {str(e)}",
            "files": [],
            "export_path": None
        }

def export_component_real(lcsc_id: str, export_path: str, export_options: Dict[str, bool], file_prefix: str = None) -> Dict[str, Any]:
    """使用真实的EasyKiConverter工具链导出元器件 - 完全对齐main.py逻辑"""
    try:
        files_created = []
        kicad_version = KicadVersion.v6
        
        # 初始化EasyEDA API
        easyeda_api = EasyedaApi()
        
        # 获取元器件数据
        logger.info(f"Fetching component data for LCSC ID: {lcsc_id}")
        component_data = easyeda_api.get_cad_data_of_component(lcsc_id=lcsc_id)
        
        if not component_data:
            return {
                "success": False,
                "message": f"Failed to retrieve component data for LCSC ID: {lcsc_id}",
                "files": [],
                "export_path": None
            }
        
        # 使用与main.py完全一致的路径处理逻辑
        output_path = export_path
        if not os.path.isabs(output_path):
            output_path = os.path.abspath(output_path)

        # 处理导出路径：如果为空则使用项目根目录上级目录的output文件夹
        if not export_path or export_path.strip() == '':
            base_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'output')
        else:
            base_folder = output_path
            if not os.path.isabs(base_folder):
                base_folder = os.path.abspath(base_folder)

        # 使用用户提供的文件名前缀，如果没有则使用默认名称
        lib_name = file_prefix if file_prefix else "easyeda_convertlib"

        # 确保目录存在
        if not os.path.isdir(base_folder):
            os.makedirs(base_folder, exist_ok=True)
            logger.info(f"Created export directory: {base_folder}")

        # 使用os.path.join确保正确的路径分隔符
        output_base = os.path.join(base_folder, lib_name)

        # 创建目录结构 - 与main.py完全一致
        footprint_dir = f"{output_base}.pretty"
        model_dir = f"{output_base}.3dshapes"
        
        if not os.path.isdir(footprint_dir):
            os.mkdir(footprint_dir)
            logger.info(f"Create {lib_name}.pretty footprint folder in {base_folder}")

        if not os.path.isdir(model_dir):
            os.mkdir(model_dir)
            logger.info(f"Create {lib_name}.3dshapes 3D model folder in {base_folder}")

        lib_extension = "kicad_sym" if kicad_version == KicadVersion.v6 else "lib"
        symbol_lib_path = f"{output_base}.{lib_extension}"
        
        if not os.path.isfile(symbol_lib_path):
            with open(symbol_lib_path, "w+", encoding="utf-8") as my_lib:
                my_lib.write(
                    '''(kicad_symbol_lib
  (version 20211014)
  (generator https://github.com/tangsangsimida/EasyKiConverter)
)'''
                    if kicad_version == KicadVersion.v6
                    else "EESchema-LIBRARY Version 2.4\n#encoding utf-8\n"
                )
            logger.info(f"Create {lib_name}.{lib_extension} symbol lib in {base_folder}")
        
        # 导出符号 - 与main.py完全一致
        if export_options.get('symbol', True):
            logger.info("Symbol conversion ...")
            symbol_importer = EasyedaSymbolImporter(easyeda_cp_cad_data=component_data)
            symbol_data = symbol_importer.get_symbol()
            
            if not symbol_data:
                logger.error("No symbol found for this component")
            else:
                symbol_exporter = ExporterSymbolKicad(
                    symbol=symbol_data, 
                    kicad_version=kicad_version
                )
                kicad_symbol_str = symbol_exporter.export(
                    footprint_lib_name=lib_name
                )
                
                # 使用与main.py相同的逻辑添加符号
                if not id_already_in_symbol_lib(
                    lib_path=symbol_lib_path,
                    component_name=symbol_data.info.name,
                    kicad_version=kicad_version,
                ):
                    add_component_in_symbol_lib_file(
                        lib_path=symbol_lib_path,
                        component_content=kicad_symbol_str,
                        kicad_version=kicad_version,
                    )
                    logger.info(f"Symbol for {symbol_data.info.name} added to {symbol_lib_path}")
                else:
                    logger.info(f"Symbol for {symbol_data.info.name} already exists in {symbol_lib_path}. Skipping.")
                
                files_created.append(os.path.abspath(symbol_lib_path))
                logger.info(f"Symbol saved to {symbol_lib_path}")
        
        # 导出封装 - 与main.py完全一致
        if export_options.get('footprint', True):
            logger.info("Footprint conversion ...")
            footprint_importer = EasyedaFootprintImporter(easyeda_cp_cad_data=component_data)
            footprint_data = footprint_importer.get_footprint()
            
            if not footprint_data:
                logger.error("No footprint found for this component")
            else:
                footprint_exporter = ExporterFootprintKicad(footprint=footprint_data)
                footprint_filename = os.path.join(
                    footprint_dir, 
                    f"{footprint_data.info.name}.kicad_mod"
                )
                
                model_3d_path = lib_name  # 与main.py一致
                footprint_exporter.export(
                    footprint_full_path=footprint_filename,
                    model_3d_path=model_3d_path
                )
                
                files_created.append(os.path.abspath(footprint_filename))
                logger.info(f"Footprint saved to {footprint_filename}")
        
        # 导出3D模型 - 与main.py完全一致
        if export_options.get('model3d', True):
            logger.info("3D model conversion ...")
            model_3d_importer = Easyeda3dModelImporter(
                easyeda_cp_cad_data=component_data, 
                download_raw_3d_model=True
            )
            model_3d = model_3d_importer.create_3d_model()
            
            if not model_3d:
                logger.error("No 3D model found for this component")
            else:
                model_3d_exporter = Exporter3dModelKicad(model_3d=model_3d)
                model_3d_exporter.export(lib_path=output_base)
                
                # 查找导出的3D模型文件
                model_name = getattr(model_3d, 'name', f"{lcsc_id}_3dmodel")
                for ext in ['.step', '.wrl']:
                    model_file = os.path.join(model_dir, f"{model_name}{ext}")
                    if os.path.exists(model_file):
                        files_created.append(os.path.abspath(model_file))
                        logger.info(f"3D model saved to {model_file}")
        
        return {
            "success": True,
            "message": f"Component {lcsc_id} exported successfully",
            "files": files_created,
            "export_path": str(Path(base_folder).absolute())
        }
        
    except Exception as e:
        logger.error(f"Export failed: {str(e)}", exc_info=True)
        return {
            "success": False,
            "message": f"Export failed: {str(e)}",
            "files": [],
            "export_path": None
        }

@app.route('/api/config', methods=['GET'])
def get_config():
    """获取用户配置"""
    try:
        config = config_manager.get_last_settings()
        return jsonify({
            'success': True,
            'config': config
        })
    except Exception as e:
        logger.error(f"获取配置失败: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/config', methods=['POST'])
def save_config():
    """保存用户配置"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': '缺少配置数据'
            }), 400
        
        success = config_manager.save_config(data)
        if success:
            return jsonify({
                'success': True,
                'message': '配置保存成功'
            })
        else:
            return jsonify({
                'success': False,
                'error': '配置保存失败'
            }), 500
    except Exception as e:
        logger.error(f"保存配置失败: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/parse-bom', methods=['POST'])
def parse_bom():
    """解析BOM文件，提取Supplier Part列中的元件编号"""
    try:
        logger.info(f"收到BOM解析请求，文件列表: {list(request.files.keys())}")
        
        # 检查是否有文件上传
        if 'bom_file' not in request.files:
            logger.error("未找到上传的文件")
            return jsonify({
                'success': False,
                'error': '未找到上传的文件'
            }), 400
        
        file = request.files['bom_file']
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': '未选择文件'
            }), 400
        
        # 检查文件扩展名
        filename = secure_filename(file.filename)
        file_ext = filename.lower().split('.')[-1]
        
        if file_ext not in ['xlsx', 'xls', 'csv']:
            return jsonify({
                'success': False,
                'error': '不支持的文件格式，请上传 .xlsx, .xls 或 .csv 文件'
            }), 400
        
        # 读取文件内容
        try:
            if file_ext == 'csv':
                # 尝试不同的编码读取CSV文件
                try:
                    df = pd.read_csv(file, encoding='utf-8')
                except UnicodeDecodeError:
                    file.seek(0)  # 重置文件指针
                    try:
                        df = pd.read_csv(file, encoding='gbk')
                    except UnicodeDecodeError:
                        file.seek(0)  # 重置文件指针
                        df = pd.read_csv(file, encoding='latin-1')
            else:
                # Excel文件 - 首先尝试自动检测表头位置（检查前10行）
                df_temp = pd.read_excel(file, header=None)
                header_row = None
                
                # 查找包含元器件编号相关列名的行（检查前10行）
                component_column_keywords = [
                    'supplier part', 'supplier_part', 'lcsc', 'lcsc part', 'lcsc_part',
                    'part number', 'part_number', 'component id', 'component_id',
                    'mpn', 'manufacturer part', 'manufacturer_part', 'manufacturer part',
                    'no.', 'quantity', 'comment', 'designator', 'footprint', 'value'
                ]
                
                for i in range(min(10, len(df_temp))):
                    row = df_temp.iloc[i]
                    row_str = ' '.join([str(x) for x in row if pd.notna(x)]).lower()
                    
                    # 检查是否包含任何元器件编号相关的关键词
                    for keyword in component_column_keywords:
                        if keyword in row_str:
                            header_row = i
                            break
                    
                    if header_row is not None:
                        break
                
                if header_row is not None:
                    # 重新读取文件，使用找到的表头行
                    file.seek(0)  # 重置文件指针
                    df = pd.read_excel(file, header=header_row)
                else:
                    # 如果没找到，尝试默认方式读取
                    file.seek(0)  # 重置文件指针
                    df = pd.read_excel(file)
        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'文件读取失败: {str(e)}'
            }), 400
        
        # 查找元器件编号列（支持多种可能的列名）
        component_column = None
        component_column_keywords = [
            'supplier part', 'supplier_part', 'lcsc', 'lcsc part', 'lcsc_part',
            'part number', 'part_number', 'component id', 'component_id',
            'mpn', 'manufacturer part', 'manufacturer_part'
        ]
        
        # 优先查找 Supplier Part 列（嘉立创BOM标准格式）
        for col in df.columns:
            col_lower = str(col).lower().strip()
            if 'supplier part' in col_lower:
                component_column = col
                break
        
        # 如果没找到 Supplier Part，再查找其他可能的列名
        if component_column is None:
            for col in df.columns:
                col_lower = str(col).lower()
                for keyword in component_column_keywords:
                    if keyword in col_lower:
                        component_column = col
                        break
                if component_column is not None:
                    break
        
        if component_column is None:
            return jsonify({
                'success': False,
                'error': f'未找到元器件编号列，请检查BOM表格式。\n支持的列名包括: Supplier Part, LCSC, Part Number, Component ID, MPN等\n可用列名: {", ".join([str(col) for col in df.columns])}'
            }), 400
        
        # 提取元件编号
        component_ids = []
        for value in df[component_column].dropna():
            # 转换为字符串并清理
            component_id = str(value).strip()
            if component_id and component_id.lower() != 'nan':
                # 检查是否是有效的元件编号（通常以字母开头）
                if component_id and len(component_id) > 1:
                    component_ids.append(component_id)
        
        # 去重并保持顺序
        unique_component_ids = []
        seen = set()
        for cid in component_ids:
            if cid not in seen:
                unique_component_ids.append(cid)
                seen.add(cid)
        
        return jsonify({
            'success': True,
            'component_ids': unique_component_ids,
            'total_count': len(unique_component_ids),
            'column_name': component_column,
            'message': f'从"{component_column}"列成功解析 {len(unique_component_ids)} 个唯一元件编号'
        })
        
    except Exception as e:
        logger.error(f"BOM解析错误: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'BOM解析失败: {str(e)}'
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/@vite/client')
def vite_client():
    """处理 Vite 客户端请求，静默返回 404"""
    return '', 404

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': '接口不存在'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': '服务器内部错误'}), 500



if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    # 完全禁用开发服务器警告
    warnings.filterwarnings('ignore', '.*This is a development server.*')
    warnings.filterwarnings('ignore', '.*Do not use it in a production deployment.*')
    warnings.filterwarnings('ignore', '.*Use a production WSGI server instead.*')
    
    # 自定义请求处理器，只显示请求日志，不显示警告
    class CustomRequestHandler(WSGIRequestHandler):
        def log(self, type, message, *args):
            # 跳过包含开发服务器警告的日志
            if "development server" not in message and "production deployment" not in message:
                return WSGIRequestHandler.log(self, type, message, *args)
    
    print("=" * 50)
    print("  EasyKiConverter Web UI")
    print("=" * 50)
    print(f"访问地址: http://localhost:{port}")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=port, debug=debug, request_handler=CustomRequestHandler)