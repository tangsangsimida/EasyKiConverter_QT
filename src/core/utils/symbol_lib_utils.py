"""
符号库工具模块
包含所有符号库操作相关函数
"""
import logging
import re
from typing import Optional

from ..kicad.parameters_kicad_symbol import KicadVersion


def add_component_in_symbol_lib_file(
    lib_path: str, component_content: str, kicad_version: KicadVersion
) -> None:
    """
    将新组件添加到符号库文件中
    Add new component to symbol library file
    
    参数:
    Args:
        lib_path (str): 符号库文件路径 / Symbol library file path
        component_content (str): 组件内容字符串 / Component content string
        kicad_version (KicadVersion): KiCad版本枚举 / KiCad version enum
    """

    if kicad_version == KicadVersion.v5:
        with open(file=lib_path, mode="a+", encoding="utf-8") as lib_file:
            lib_file.write(str(component_content))
    elif kicad_version == KicadVersion.v6:
        with open(file=lib_path, mode="rb+") as lib_file:
            lib_file.seek(-2, 2)  # 移动到文件末尾倒数第二个字符 / Move to second last character of file
            lib_file.truncate()  # 删除最后的括号 / Remove the closing bracket
            lib_file.write(str(component_content).encode(encoding="utf-8"))
            lib_file.write("\n)".encode(encoding="utf-8"))  # 重新添加括号 / Re-add the closing bracket

        with open(file=lib_path, encoding="utf-8") as lib_file:
            new_lib_data = lib_file.read()

        with open(file=lib_path, mode="w", encoding="utf-8") as lib_file:
            lib_file.write(
                new_lib_data.replace(
                    "(generator kicad_symbol_editor)",
                    "(generator https://github.com/tangsangsimida/EasyKiConverter)",
                )
            )

        # 保持标准的generator字段，确保KiCad兼容性
        # with open(file=lib_path, encoding="utf-8") as lib_file:
        #     new_lib_data = lib_file.read()

        # with open(file=lib_path, mode="w", encoding="utf-8") as lib_file:
        #     lib_file.write(
        #         new_lib_data.replace(
        #             "(generator kicad_symbol_editor)",
        #             "(generator https://github.com/tangsangsimida/EasyKiConverter)",
        #         )
        #     )


def update_component_in_symbol_lib_file(
    lib_path: str,
    component_name: str,
    component_content: str,
    kicad_version: KicadVersion,
) -> None:
    """
    更新符号库中已存在的组件
    Update existing component in symbol library
    """
    with open(file=lib_path, encoding="utf-8") as lib_file:
        current_lib = lib_file.read()
        new_lib = re.sub(
            sym_lib_regex_pattern[kicad_version.name].format(
                component_name=sanitize_for_regex(component_name)
            ),
            str(component_content),
            current_lib,
            flags=re.DOTALL,
        )

        # 保持标准的generator字段，确保KiCad兼容性
        # new_lib = new_lib.replace(
        #     "(generator kicad_symbol_editor)",
        #     "(generator https://github.com/tangsangsimida/EasyKiConverter)",
        # )

    with open(file=lib_path, mode="w", encoding="utf-8") as lib_file:
        lib_file.write(new_lib)


def id_already_in_symbol_lib(
    lib_path: str, component_name: str, kicad_version: KicadVersion
) -> bool:
    """
    检查符号库中是否已存在指定名称的组件
    Check if component exists in symbol library
    """
    with open(lib_path, encoding="utf-8") as lib_file:
        current_lib = lib_file.read()
        component = re.findall(
            sym_lib_regex_pattern[kicad_version.name].format(
                component_name=sanitize_for_regex(component_name)
            ),
            current_lib,
            flags=re.DOTALL,
        )
        if component != []:
            logging.warning(f"This id is already in {lib_path}")
            return True
    return False

# 共享的正则表达式模式
sym_lib_regex_pattern = {
    "v5": r"(#\n# {component_name}\n#\n.*?ENDDEF\n)",
    "v6": r'\n  \(symbol "{component_name}".*?\n  \)',
    "v6_99": r"",
}

def sanitize_for_regex(field: str):
    """字符串转义用于正则表达式匹配"""
    return re.escape(field)