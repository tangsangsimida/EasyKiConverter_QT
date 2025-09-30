# -*- coding: utf-8 -*-
"""
资源工具模块
用于处理PyInstaller打包环境下的资源文件路径
"""

import sys
import os


def resource_path(relative_path: str) -> str:
    """获取资源文件的绝对路径，兼容 PyInstaller 打包环境"""
    try:
        # PyInstaller 创建的临时目录
        base_path = sys._MEIPASS
    except AttributeError:
        # 开发环境
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)