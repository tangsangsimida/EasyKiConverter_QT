#!/usr/bin/env python3
"""
测试符号库文件结构和格式
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.kicad.parameters_kicad_symbol import KicadVersion, KiSymbol, KiSymbolInfo
from core.utils.symbol_lib_utils import add_component_in_symbol_lib_file

# 创建一个测试符号
test_symbol = KiSymbol(
    info=KiSymbolInfo(
        name="CL05B104KO5NNNC",
        prefix="C",
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
print(repr(exported_symbol))

# 创建基础符号库文件内容
lib_header = """(kicad_symbol_lib
  (version 20211014)
  (generator "https://github.com/tangsangsimida/EasyKiConverter")
)"""

# 创建测试文件
test_file_path = "/tmp/test_symbol_structure.kicad_sym"

# 写入基础库文件
with open(test_file_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(lib_header)

print("\n=== 基础符号库文件 ===")
with open(test_file_path, 'r', encoding='utf-8') as f:
    content = f.read()
    print(repr(content))

# 添加组件到符号库
add_component_in_symbol_lib_file(test_file_path, exported_symbol, KicadVersion.v6)

# 读取结果
with open(test_file_path, 'r', encoding='utf-8') as f:
    result = f.read()

print("\n=== 添加组件后的符号库文件 ===")
print(repr(result))

# 显示文件内容
print("\n=== 文件内容 ===")
print(result)

# 检查行尾字符
print("\n=== 行尾字符检查 ===")
lines = result.split('\n')
for i, line in enumerate(lines[:20], 1):
    if line:
        print(f"第{i}行: {repr(line)}")