#!/usr/bin/env python3
"""
测试使用四个空格缩进的符号库导出
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.kicad.parameters_kicad_symbol import KicadVersion, KiSymbol, KiSymbolInfo
from core.utils.symbol_lib_utils import add_component_in_symbol_lib_file

# 创建一个测试符号
test_symbol = KiSymbol(
    info=KiSymbolInfo(
        name="RP2040",
        prefix="U",
        package="",
        manufacturer="",
        datasheet="",
        lcsc_id="",
        jlc_id="",
    )
)

# 导出为KiCad v6格式
exported_symbol = test_symbol.export(KicadVersion.v6)
print("=== 导出的符号内容 ===")
print(exported_symbol)

# 创建基础符号库文件内容
lib_header = """(kicad_symbol_lib
  (version 20211014)
  (generator "https://github.com/tangsangsimida/EasyKiConverter")
)"""

# 创建测试文件
test_file_path = "/tmp/test_indentation.kicad_sym"

# 写入基础库文件
with open(test_file_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(lib_header)

print("\n=== 基础符号库文件 ===")
with open(test_file_path, 'r', encoding='utf-8') as f:
    content = f.read()
    print(content)

# 添加组件到符号库
add_component_in_symbol_lib_file(test_file_path, exported_symbol, KicadVersion.v6)

# 读取结果
with open(test_file_path, 'r', encoding='utf-8') as f:
    result = f.read()

print("\n=== 添加组件后的符号库文件 ===")
print(result)

# 检查缩进
lines = result.split('\n')
print("\n=== 缩进检查 ===")
for i, line in enumerate(lines[:20], 1):
    if line.strip():
        # 计算行首空格数
        leading_spaces = len(line) - len(line.lstrip(' '))
        print(f"第{i}行: {leading_spaces}个空格 - {line.strip()}")