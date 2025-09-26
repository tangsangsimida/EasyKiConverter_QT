#!/usr/bin/env python3
"""
测试修复生成器字段格式后的符号库导出
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.kicad.parameters_kicad_symbol import KicadVersion, KiSymbol, KiSymbolInfo
from core.utils.symbol_lib_utils import add_component_in_symbol_lib_file

# 创建一个测试符号
test_symbol = KiSymbol(
    info=KiSymbolInfo(
        name="CL05B103KB5NNNC",
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
test_file_path = "/tmp/test_generator_format.kicad_sym"

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

# 检查特定行
lines = result.split('\n')
print(f"\n第1行: {repr(lines[0])}")
print(f"第2行: {repr(lines[1])}")
print(f"第3行: {repr(lines[2])}")
print(f"第4行: {repr(lines[3])}")