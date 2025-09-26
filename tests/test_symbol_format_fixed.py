#!/usr/bin/env python3
"""
测试修复后的符号库导出格式
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.kicad.parameters_kicad_symbol import KicadVersion, KiSymbol, KiSymbolInfo

# 创建一个测试符号
test_symbol = KiSymbol(
    info=KiSymbolInfo(
        name="RP2040",
        prefix="U",
        package="LQFN-56_L7.0-W7.0-P0.4-EP",
        manufacturer="",
        datasheet="",
        lcsc_id="C2040",
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
test_file_path = "/tmp/test_symbol_format_fixed.kicad_sym"

with open(test_file_path, 'w', encoding='utf-8') as f:
    f.write(lib_header)
    f.write(exported_symbol)
    f.write(lib_footer)

print("\n=== 完整的符号库文件 ===")
with open(test_file_path, 'r', encoding='utf-8') as f:
    content = f.read()
    print(content)

# 语法检查
print("\n=== 语法检查 ===")
lines = content.split('\n')
for i, line in enumerate(lines, 1):
    if line.strip() and not line.startswith('  ') and not line.startswith('(') and not line.startswith(')') and not line.startswith('(kicad_symbol_lib') and not line.startswith('(symbol'):
        print(f"第{i}行可能有格式问题: {line}")

# 检查括号匹配
open_brackets = content.count('(')
close_brackets = content.count(')')
print(f"\n括号匹配: 左={open_brackets}, 右={close_brackets}, {'✅' if open_brackets == close_brackets else '❌'}")