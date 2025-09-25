#!/usr/bin/env python3
# 测试实际的符号导出流程

import sys
import os
sys.path.insert(0, '/home/dennis/Desktop/workspace/github_projects/EasyKiConverter/src')

# 设置环境变量以避免Qt导入问题
os.environ['QT_QPA_PLATFORM'] = 'offscreen'

from core.easyeda.parameters_easyeda import EeSymbol, EeSymbolInfo
from core.kicad.export_kicad_symbol import ExporterSymbolKicad
from core.kicad.parameters_kicad_symbol import KicadVersion

# 创建一个更真实的测试符号
symbol_info = EeSymbolInfo(
    name="C12345",
    prefix="C",
    package="C0402",
    manufacturer="Yageo",
    datasheet="https://datasheet.lcsc.com/lcsc/1811151516_Yageo-CC0402KRX5R6BB104_C15850.pdf",
    lcsc_id="C15850",
    jlc_id="C15850"
)

# 创建符号对象
symbol = EeSymbol(
    info=symbol_info,
    pins=[],
    rectangles=[],
    circles=[],
    arcs=[],
    paths=[],
    polygons=[],
    polylines=[],
    ellipses=[],
    bbox=None
)

print("=== 测试真实符号导出 ===")
print(f"符号名称: {symbol.info.name}")
print(f"封装: {symbol.info.package}")

# 导出为KiCad v6格式
exporter = ExporterSymbolKicad(symbol=symbol, kicad_version=KicadVersion.v6)
symbol_content = exporter.export(footprint_lib_name="test_lib")

print("\n=== 生成的符号内容 ===")
print(repr(symbol_content))

print("\n=== 格式化的符号内容 ===")
print(symbol_content)

# 创建完整的符号库文件
lib_header = """(kicad_symbol_lib
  (version 20211014)
  (generator "kicad_symbol_editor")
  (generator_version "6.0.0")
"""

full_lib = lib_header + symbol_content + "\n)"

print("\n=== 完整符号库文件 ===")
print(full_lib)

# 保存到文件进行测试
with open('/tmp/test_real.kicad_sym', 'w', encoding='utf-8') as f:
    f.write(full_lib)

print(f"\n=== 文件已保存到 /tmp/test_real.kicad_sym ===")

# 检查括号匹配
open_brackets = full_lib.count('(')
close_brackets = full_lib.count(')')
print(f"括号匹配: 左={open_brackets}, 右={close_brackets}, {'✅' if open_brackets == close_brackets else '❌'}")

# 检查是否有空行问题
lines = full_lib.split('\n')
empty_lines = [i+1 for i, line in enumerate(lines) if not line.strip()]
if empty_lines:
    print(f"空行位置: {empty_lines}")

# 尝试用Python的解析器检查基本语法
try:
    # 简单的括号匹配检查
    stack = []
    for i, char in enumerate(full_lib):
        if char == '(':
            stack.append(i)
        elif char == ')':
            if not stack:
                print(f"❌ 第{i+1}字符: 多余的右括号")
                break
            stack.pop()
    else:
        if stack:
            print(f"❌ 第{stack[-1]+1}字符: 未闭合的左括号")
        else:
            print("✅ 括号语法检查通过")
except Exception as e:
    print(f"语法检查错误: {e}")

# 检查行尾格式
print(f"\n行尾格式检查:")
print(f"Unix格式 (LF): {'✅' if '\n' in full_lib and not '\r\n' in full_lib else '❌'}")
print(f"Windows格式 (CRLF): {'✅' if '\r\n' in full_lib else '❌'}")

# 让我们也测试KiCad是否能解析这个文件
print(f"\n文件大小: {len(full_lib)} 字符")
print(f"行数: {len(lines)}")