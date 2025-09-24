"""
EasyKiConverter 统一包管理
确保所有模块都能正确导入核心功能
"""

import sys
from pathlib import Path

# 获取项目根目录
PROJECT_ROOT = Path(__file__).parent.parent.parent
SRC_DIR = PROJECT_ROOT / "src"

# 将src目录添加到Python路径
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

# 核心模块导入
try:
    from core import easyeda, kicad, utils
    from core.easyeda import easyeda_api, easyeda_importer, svg_path_parser
    from core.kicad import (
        export_kicad_3d_model,
        export_kicad_footprint,
        export_kicad_symbol,
        parameters_kicad_footprint,
        parameters_kicad_symbol
    )
    from core.utils import symbol_lib_utils, geometry_utils
    
    CORE_AVAILABLE = True
except ImportError as e:
    print(f"警告: 核心模块导入失败 - {e}")
    CORE_AVAILABLE = False

__all__ = [
    'PROJECT_ROOT',
    'SRC_DIR', 
    'CORE_AVAILABLE',
    'easyeda',
    'kicad',
    'utils'
]