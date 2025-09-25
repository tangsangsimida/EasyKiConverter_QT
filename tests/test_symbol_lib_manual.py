#!/usr/bin/env python3
# 手动测试符号库文件格式

# 创建一个测试符号库文件
test_lib_content = """(kicad_symbol_lib
  (version 20211014)
  (generator "kicad_symbol_editor")
  (generator_version "6.0.0")
)"""

# 测试符号内容
test_symbol = """
  (symbol "TEST_COMPONENT"
    (in_bom yes)
    (on_board yes)
    (property
      "Reference"
      "U"
      (id 0)
      (at 0 5.08 0)
      (effects (font (size 1.27 1.27) ) )
    )
    (property
      "Value"
      "TEST_COMPONENT"
      (id 1)
      (at 0 -5.08 0)
      (effects (font (size 1.27 1.27) ) )
    )
    (symbol "TEST_COMPONENT_0_1"
    )
  )"""

# 写入初始文件
with open('/tmp/test.kicad_sym', 'w', encoding='utf-8') as f:
    f.write(test_lib_content)

print("=== 初始符号库文件 ===")
print(test_lib_content)

# 手动添加组件（模拟add_component_in_symbol_lib_file函数）
with open('/tmp/test.kicad_sym', 'r', encoding='utf-8') as f:
    content = f.read()

# 移除结尾的括号并添加组件
if content.endswith(")"):
    new_content = content[:-1] + test_symbol + "\n)"
else:
    new_content = content + test_symbol + "\n)"

# 写回文件
with open('/tmp/test.kicad_sym', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("\n=== 添加组件后的符号库文件 ===")
print(new_content)

# 检查语法
print("\n=== 语法检查 ===")
lines = new_content.split('\n')
for i, line in enumerate(lines, 1):
    stripped = line.strip()
    if stripped and not stripped.startswith('(') and not stripped.startswith(')') and not stripped.startswith('(property') and not stripped.startswith('(symbol') and not stripped.startswith('(in_bom') and not stripped.startswith('(on_board') and not stripped.startswith('(id') and not stripped.startswith('(at') and not stripped.startswith('(effects'):
        print(f"第{i}行可能有格式问题: '{line}'")

# 检查括号匹配
open_brackets = new_content.count('(')
close_brackets = new_content.count(')')
print(f"\n括号匹配: 左={open_brackets}, 右={close_brackets}, {'✅' if open_brackets == close_brackets else '❌'}")

# 检查是否有空行或格式问题
print("\n=== 详细格式分析 ===")
import re

# 检查是否符合KiCad v6格式要求
property_pattern = r'^\s*\(property\s+"[^"]*"\s+"[^"]*"\s+\(id\s+\d+\)\s+\(at\s+[-\d.]+\s+[-\d.]+\s+\d+\)\s+\(effects\s+\(font\s+\(size\s+\d+\.\d+\s+\d+\.\d+\)\s*\)\s*(hide)?\)\s*\)$'
symbol_pattern = r'^\s*\(symbol\s+"[^"]*"\s*$'
symbol_end_pattern = r'^\s*\)\s*$'

lines = new_content.split('\n')
for i, line in enumerate(lines, 1):
    stripped = line.strip()
    if stripped:
        if re.match(property_pattern, stripped):
            continue
        elif re.match(symbol_pattern, stripped):
            continue
        elif re.match(symbol_end_pattern, stripped):
            continue
        elif stripped in ['(in_bom yes)', '(on_board yes)', '(kicad_symbol_lib', '(version 20211014)', '(generator "kicad_symbol_editor")', '(generator_version "6.0.0")']:
            continue
        elif stripped.startswith('(property') or stripped.startswith('(symbol') or stripped.startswith('(id') or stripped.startswith('(at') or stripped.startswith('(effects'):
            continue
        else:
            print(f"第{i}行格式未知: '{stripped}'")