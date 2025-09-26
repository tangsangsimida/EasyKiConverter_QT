#!/usr/bin/env python3
"""
测试修复空行和generator_version行问题后的符号库导出
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
print(repr(exported_symbol))

# 创建基础符号库文件内容 - 包含generator_version行用于测试移除功能
lib_header = """(kicad_symbol_lib
  (version 20211014)
  (generator kicad_symbol_editor)
  (generator_version "6.0.0")
)"""

# 创建测试文件
test_file_path = "/tmp/test_no_empty_lines.kicad_sym"

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

# 检查空行
lines = result.split('\n')
print(f"\n总行数: {len(lines)}")
empty_lines = [i for i, line in enumerate(lines) if not line.strip()]
if empty_lines:
    print(f"空行位置: {empty_lines}")
else:
    print("没有空行")

# 检查generator_version行
if 'generator_version' in result:
    print("文件中仍包含generator_version行")
else:
    print("文件中已移除generator_version行")