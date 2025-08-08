#!/usr/bin/env python3
"""
EasyKiConverter Web UI - 集成真实EasyKiConverter工具链
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import tempfile
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

from flask import Flask, request, jsonify, send_file, render_template_string, send_from_directory
from flask_cors import CORS
import logging

# 导入EasyKiConverter的核心模块
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
from helpers import add_component_in_symbol_lib_file, id_already_in_symbol_lib

# 创建Flask应用
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 主页路由
@app.route('/')
def index():
    """提供主页"""
    return send_from_directory('.', 'index.html')

# 静态文件路由
@app.route('/styles.css')
def styles():
    """提供CSS文件"""
    return send_from_directory('.', 'styles.css')

@app.route('/script.js')
def script():
    """提供JS文件"""
    return send_from_directory('.', 'script.js')

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
                'error': 'componentIds不能为空'
            }), 400

        # 处理导出路径：如果为空则使用项目根目录上级目录的output文件夹
        if not export_path or export_path.strip() == '':
            export_dir = Path.cwd().parent / 'output'
        else:
            export_dir = Path(export_path)
            if not export_dir.is_absolute():
                export_dir = Path.cwd() / export_dir
        
        # 确保导出目录存在
        export_dir.mkdir(parents=True, exist_ok=True)

        # 使用真实导出逻辑
        all_results = []
        for lcsc_id in component_ids:
            if not lcsc_id.startswith('C'):
                all_results.append({
                    'componentId': lcsc_id,
                    'success': False,
                    'error': 'LCSC ID应以C开头'
                })
                continue
                
            result = export_component_real(lcsc_id, str(export_dir), options, file_prefix)
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
            
            all_results.append({
                'componentId': lcsc_id,
                'success': result['success'],
                'files': file_details,
                'message': result['message'],
                'exportPath': result['export_path']
            })
        
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
        lib_name = file_prefix if file_prefix else "EasyKi_Library"

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
  (generator https://github.com/uPesy/easyeda2kicad.py)
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

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': '接口不存在'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': '服务器内部错误'}), 500



if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    print("=" * 50)
    print("  EasyKiConverter Web UI")
    print("=" * 50)
    print(f"访问: http://localhost:{port}")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=port, debug=debug)