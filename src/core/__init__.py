# Core module initialization
import sys
from pathlib import Path

# 统一包管理 - 确保src目录在Python路径中
SRC_DIR = Path(__file__).parent.parent
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

# 现在可以安全地导入子模块
from . import easyeda, kicad, utils

__all__ = ['easyeda', 'kicad', 'utils']