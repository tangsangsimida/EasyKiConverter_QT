#!/usr/bin/env python3
# 测试符号库格式生成

import sys
sys.path.insert(0, '/home/dennis/Desktop/workspace/github_projects/EasyKiConverter/src')

from core.kicad.parameters_kicad_symbol import KiSymbol, KiSymbolInfo, KicadVersion
from core.easyeda.parameters_easyeda import EeSymbol, EeSymbolInfo

# 创建一个简单的测试符号
ki_info = KiSymbolInfo(
    name="TEST_COMPONENT",
    prefix="U",
    package="TEST_PACKAGE",
    manufacturer="Test Manufacturer",
    datasheet="https://example.com/datasheet.pdf",
    lcsc_id="C12345",
    jlc_id="J12345"
)

# 创建符号对象
ki_symbol = KiSymbol(info=ki_info, pins=[], rectangles=[], circles=[], arcs=[], polygons=[], beziers=[])

# 直接查看v6格式的符号内容
symbol_content_v6 = ki_symbol.export(kicad_version=KicadVersion.v6)

print("=== 生成的KiCad v6符号内容 ===")
print(repr(symbol_content_v6))
print("\n=== 格式化的符号内容 ===")
print(symbol_content_v6)

print("\n=== 符号库头部格式 ===")
lib_header = """(kicad_symbol_lib
  (version 20211014)
  (generator "kicad_symbol_editor")
  (generator_version "6.0.0")
"""
print(lib_header)

print("=== 完整符号库格式 ===")
full_lib = lib_header + symbol_content_v6 + "\n)"
print(full_lib)

# 检查括号匹配
print("\n=== 括号匹配检查 ===")
open_brackets = full_lib.count('(')
close_brackets = full_lib.count(')')
print(f"左括号数量: {open_brackets}")
print(f"右括号数量: {close_brackets}")
print(f"括号匹配: {'✅' if open_brackets == close_brackets else '❌'}")