#!/usr/bin/env python3
# 测试符号库文件格式

import sys
sys.path.insert(0, '/home/dennis/Desktop/workspace/github_projects/EasyKiConverter/src')

import sys
sys.path.insert(0, '/home/dennis/Desktop/workspace/github_projects/EasyKiConverter/src')

from core.utils.symbol_lib_utils import add_component_in_symbol_lib_file
from core.kicad.parameters_kicad_symbol import KicadVersion

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

# 写入测试文件
with open('/tmp/test.kicad_sym', 'w', encoding='utf-8') as f:
    f.write(test_lib_content)

print("=== 初始符号库文件 ===")
print(test_lib_content)

# 使用工具函数添加组件
add_component_in_symbol_lib_file('/tmp/test.kicad_sym', test_symbol, KicadVersion.v6)

# 读取结果
with open('/tmp/test.kicad_sym', 'r', encoding='utf-8') as f:
    result = f.read()

print("\n=== 添加组件后的符号库文件 ===")
print(result)

# 检查语法
print("\n=== 语法检查 ===")
lines = result.split('\n')
for i, line in enumerate(lines, 1):
    if line.strip() and not line.startswith('  ') and not line.startswith('(') and not line.startswith(')'):
        print(f"第{i}行可能有格式问题: {line}")

# 检查括号匹配
open_brackets = result.count('(')
close_brackets = result.count(')')
print(f"\n括号匹配: 左={open_brackets}, 右={close_brackets}, {'✅' if open_brackets == close_brackets else '❌'}")