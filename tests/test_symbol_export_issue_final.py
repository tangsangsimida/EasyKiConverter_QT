#!/usr/bin/env python3
"""
测试符号库导出问题最终修复
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.kicad.parameters_kicad_symbol import KicadVersion
from core.utils.symbol_lib_utils import add_component_in_symbol_lib_file

# 创建一个简单的测试符号 - 修复格式问题
test_symbol = """  (symbol "TEST"
    (in_bom yes)
    (on_board yes)
    (property "Reference" "U" (id 0) (at 0 5.08 0) (effects (font (size 1.27 1.27))))
    (property "Value" "TEST" (id 1) (at 0 -5.08 0) (effects (font (size 1.27 1.27))))
    (symbol "TEST_0_1"
      (pin input line (at -2.54 0 180) (length 2.54) (name "IN" (effects (font (size 1.27 1.27))))
        (number "1" (effects (font (size 1.27 1.27)))))
    )
  )"""

# 创建基础符号库文件内容 - 修复格式问题
lib_header = """(kicad_symbol_lib
  (version 20211014)
  (generator "https://github.com/tangsangsimida/EasyKiConverter")
)"""

# 创建测试文件
test_file_path = "/tmp/test_export_issue_final.kicad_sym"

# 写入基础库文件
with open(test_file_path, 'w', encoding='utf-8') as f:
    f.write(lib_header)

print("=== 基础符号库文件 ===")
print(lib_header)

# 添加组件到符号库
add_component_in_symbol_lib_file(test_file_path, test_symbol, KicadVersion.v6)

# 读取结果
with open(test_file_path, 'r', encoding='utf-8') as f:
    result = f.read()

print("\n=== 添加组件后的符号库文件 ===")
print(result)

# 语法检查
print("\n=== 语法检查 ===")
lines = result.split('\n')
for i, line in enumerate(lines, 1):
    if line.strip() and not line.startswith('  ') and not line.startswith('(') and not line.startswith(')'):
        print(f"第{i}行可能有格式问题: {line}")

# 检查括号匹配
open_brackets = result.count('(')
close_brackets = result.count(')')
print(f"\n括号匹配: 左={open_brackets}, 右={close_brackets}, {'✅' if open_brackets == close_brackets else '❌'}")

# 检查特定行的内容
lines = result.split('\n')
if len(lines) >= 4:
    print(f"\n第4行内容: '{lines[3]}'")
    print(f"第4行前4个字符: '{lines[3][:4]}'")