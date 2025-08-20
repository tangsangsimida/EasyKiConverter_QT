#!/usr/bin/env python3
"""
EasyKiConverter Web UI 后端服务器
提供REST API供前端调用，处理元器件库导出
"""

import os
import sys
import json
import asyncio
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

try:
    from flask import Flask, request, jsonify, send_file
    from flask_cors import CORS
except ImportError:
    print("请安装依赖: pip install flask flask-cors")
    sys.exit(1)

# 简化版本 - 不依赖EasyKiConverter模块，直接提供模拟功能
# 实际使用时需要集成真正的转换功能

app = Flask(__name__)
CORS(app)

# 全局变量存储导出任务状态
export_tasks = {}

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
        file_prefix = data.get('filePrefix', 'exported_components')
        export_path = data.get('exportPath', './exports')
        options = data.get('options', {
            'symbol': True,
            'footprint': True,
            'model3d': True
        })

        if not component_ids:
            return jsonify({
                'success': False,
                'error': 'componentIds不能为空'
            }), 400

        # 创建导出任务
        task_id = f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # 确保导出目录存在
        export_dir = Path(export_path)
        export_dir.mkdir(parents=True, exist_ok=True)

        # 执行导出
        results = process_export_task(
            component_ids, 
            file_prefix, 
            export_dir, 
            options
        )

        return jsonify({
            'success': True,
            'taskId': task_id,
            'results': results,
            'exportPath': str(export_dir)
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })

def process_export_task(
    component_ids: List[str], 
    file_prefix: str, 
    export_dir: Path, 
    options: Dict[str, bool]
) -> List[Dict[str, Any]]:
    """处理实际的导出任务"""
    results = []
    
    for component_id in component_ids:
        component_results = process_single_component(
            component_id, file_prefix, export_dir, options
        )
        results.extend(component_results)
    
    return results

def process_single_component(
    component_id: str, 
    file_prefix: str, 
    export_dir: Path, 
    options: Dict[str, bool]
) -> List[Dict[str, Any]]:
    """处理单个元器件的导出"""
    results = []
    
    # 符号库导出
    if options.get('symbol', True):
        try:
            symbol_file = export_dir / f"{file_prefix}_{component_id}_symbol.kicad_sym"
            
            # 这里应该调用实际的EasyKiConverter功能
            # 暂时创建占位文件
            symbol_file.touch()
            
            results.append({
                'componentId': component_id,
                'type': 'symbol',
                'fileName': symbol_file.name,
                'filePath': str(symbol_file),
                'success': True
            })
        except Exception as e:
            results.append({
                'componentId': component_id,
                'type': 'symbol',
                'fileName': f"{file_prefix}_{component_id}_symbol.kicad_sym",
                'filePath': str(export_dir),
                'success': False,
                'error': str(e)
            })
    
    # 封装库导出
    if options.get('footprint', True):
        try:
            footprint_dir = export_dir / f"{file_prefix}_{component_id}_footprints.pretty"
            footprint_dir.mkdir(exist_ok=True)
            footprint_file = footprint_dir / f"{component_id}.kicad_mod"
            footprint_file.touch()
            
            results.append({
                'componentId': component_id,
                'type': 'footprint',
                'fileName': footprint_dir.name,
                'filePath': str(footprint_dir),
                'success': True
            })
        except Exception as e:
            results.append({
                'componentId': component_id,
                'type': 'footprint',
                'fileName': f"{file_prefix}_{component_id}_footprints.pretty",
                'filePath': str(export_dir),
                'success': False,
                'error': str(e)
            })
    
    # 3D模型导出
    if options.get('model3d', True):
        try:
            model3d_dir = export_dir / f"{file_prefix}_{component_id}_3dmodels"
            model3d_dir.mkdir(exist_ok=True)
            model3d_file = model3d_dir / f"{component_id}.step"
            model3d_file.touch()
            
            results.append({
                'componentId': component_id,
                'type': '3dmodel',
                'fileName': model3d_file.name,
                'filePath': str(model3d_file),
                'success': True
            })
        except Exception as e:
            results.append({
                'componentId': component_id,
                'type': '3dmodel',
                'fileName': f"{component_id}.step",
                'filePath': str(export_dir),
                'success': False,
                'error': str(e)
            })
    
    return results

@app.route('/api/download/<path:filename>')
def download_file(filename):
    """下载导出的文件"""
    try:
        file_path = Path(filename)
        if file_path.exists():
            return send_file(str(file_path), as_attachment=True)
        else:
            return jsonify({'error': '文件不存在'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': '接口不存在'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': '服务器内部错误'}), 500

def main():
    """启动服务器"""
    port = int(os.environ.get('PORT', 8000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    print(f"启动 EasyKiConverter Web UI 服务器...")
    print(f"访问地址: http://localhost:{port} 使用Web界面")
    print(f"API文档: http://localhost:{port}/api/health")
    
    app.run(host='0.0.0.0', port=port, debug=debug)

if __name__ == '__main__':
    main()