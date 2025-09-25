#!/usr/bin/env python3
# 检查正确的KiCad v6符号库格式

# 这是KiCad v6生成的标准符号库格式示例
standard_format = """(kicad_symbol_lib
  (version 20211014)
  (generator "kicad_symbol_editor")
  (generator_version "6.0.0")
  (symbol "Device:R"
    (pin_numbers hide)
    (pin_names (offset 0))
    (exclude_from_sim no)
    (in_bom yes)
    (on_board yes)
    (property "Reference" "R"
      (at 2.032 0 90)
      (effects (font (size 1.27 1.27)))
    )
    (property "Value" "R"
      (at 0 0 90)
      (effects (font (size 1.27 1.27)))
    )
    (property "Footprint" ""
      (at -1.778 0 90)
      (effects (font (size 1.27 1.27)) hide)
    )
    (symbol "R_0_1"
      (rectangle (start -1.016 -2.54) (end 1.016 2.54)
        (stroke (width 0.254) (type default))
        (fill (type none))
      )
    )
  )
)"""

print("=== 标准KiCad v6格式 ===")
print(standard_format)

# 对比我们的格式
our_format = """(kicad_symbol_lib
  (version 20211014)
  (generator "kicad_symbol_editor")
  (generator_version "6.0.0")

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
  )
)"""

print("\n=== 我们的格式 ===")
print(our_format)

print("\n=== 差异分析 ===")
print("1. 标准格式中，property的所有参数都在同一行:")
print("   (property \"Reference\" \"R\" (at 2.032 0 90) (effects (font (size 1.27 1.27))))")
print("2. 我们的格式中，property参数分散在多行:")
print("   (property\n     \"Reference\"\n     \"U\"\n     (id 0)")
print("3. 这可能是导致解析错误的原因！")

# 让我们修复格式
fixed_format = """(kicad_symbol_lib
  (version 20211014)
  (generator "kicad_symbol_editor")
  (generator_version "6.0.0")
  (symbol "TEST_COMPONENT"
    (in_bom yes)
    (on_board yes)
    (property "Reference" "U" (id 0) (at 0 5.08 0) (effects (font (size 1.27 1.27))))
    (property "Value" "TEST_COMPONENT" (id 1) (at 0 -5.08 0) (effects (font (size 1.27 1.27))))
    (property "Footprint" "TEST_PACKAGE" (id 2) (at 0 -7.62 0) (effects (font (size 1.27 1.27)) hide))
    (property "Datasheet" "https://example.com/datasheet.pdf" (id 3) (at 0 -10.16 0) (effects (font (size 1.27 1.27)) hide))
    (property "Manufacturer" "Test Manufacturer" (id 4) (at 0 -12.70 0) (effects (font (size 1.27 1.27)) hide))
    (property "LCSC Part" "C12345" (id 5) (at 0 -15.24 0) (effects (font (size 1.27 1.27)) hide))
    (property "JLC Part" "J12345" (id 6) (at 0 -17.78 0) (effects (font (size 1.27 1.27)) hide))
    (symbol "TEST_COMPONENT_0_1"
    )
  )
)"""

print("\n=== 修复后的格式 ===")
print(fixed_format)