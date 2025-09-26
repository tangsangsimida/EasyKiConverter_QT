#!/usr/bin/env python3
"""
测试修复行尾字符问题后的符号库导出
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.kicad.parameters_kicad_symbol import KicadVersion, KiSymbol, KiSymbolInfo

# 创建一个测试符号
test_symbol = KiSymbol(
    info=KiSymbolInfo(
        name="CL05A225MQ5NSNC",
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
print(exported_symbol)

# 创建完整的符号库文件
lib_header = """(kicad_symbol_lib
  (version 20211014)
  (generator "https://github.com/tangsangsimida/EasyKiConverter")
"""

lib_footer = "\n)"

# 创建测试文件
test_file_path = "/tmp/test_line_endings.kicad_sym"

with open(test_file_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(lib_header)
    f.write(exported_symbol)
    f.write(lib_footer)

print("\n=== 完整的符号库文件 ===")
with open(test_file_path, 'r', encoding='utf-8') as f:
    content = f.read()
    print(content)

# 检查行尾字符
print("\n=== 行尾字符检查 ===")
lines = content.split('\n')
for i, line in enumerate(lines[:10], 1):
    if line:
        print(f"第{i}行: {repr(line)}")

# 检查括号匹配
open_brackets = content.count('(')
close_brackets = content.count(')')
print(f"\n括号匹配: 左={open_brackets}, 右={close_brackets}, {'✅' if open_brackets == close_brackets else '❌'}")