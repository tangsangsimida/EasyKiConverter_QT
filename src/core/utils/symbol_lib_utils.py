"""
符号库工具模块
包含所有符号库操作相关函数
"""
import logging
import re

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
        # 读取现有文件内容
        with open(file=lib_path, encoding="utf-8") as lib_file:
            lib_data = lib_file.read()
        
        # 移除末尾的闭合括号
        if lib_data.strip().endswith(')'):
            lib_data = lib_data.strip()[:-1]
        
        # 添加新组件内容
        formatted_content = str(component_content)
        # 移除组件内容中的空行
        formatted_content = '\n'.join(line for line in formatted_content.split('\n') if line.strip())
        if not formatted_content.startswith('\n'):
            formatted_content = '\n' + formatted_content
        if not formatted_content.endswith('\n'):
            formatted_content = formatted_content + '\n'
        
        # 重新组合文件内容
        new_lib_data = lib_data + formatted_content + ')'
        
        # 更新生成器字段并移除generator_version行
        # 替换生成器字段
        new_lib_data = new_lib_data.replace(
            "(generator kicad_symbol_editor)",
            "(generator \"https://github.com/tangsangsimida/EasyKiConverter\")",
        )
        
        # 移除generator_version行
        new_lib_data = re.sub(r'\s*\(generator_version\s+\"[^\"]*\"\)\s*\n?', '', new_lib_data)
        
        # 处理空行：移除多余的空行，但保持必要的结构
        lines = new_lib_data.split('\n')
        cleaned_lines = []
        for i, line in enumerate(lines):
            # 保留非空行和必要的空行
            if line.strip() or (i > 0 and i < len(lines) - 1):
                cleaned_lines.append(line)
        
        # 移除连续的空行，只保留单个空行
        result_lines = []
        prev_line_empty = False
        for line in cleaned_lines:
            is_empty = not line.strip()
            if not is_empty or not prev_line_empty:
                result_lines.append(line)
            prev_line_empty = is_empty
        
        new_lib_data = '\n'.join(result_lines) + '\n'

        with open(file=lib_path, mode="w", encoding="utf-8") as lib_file:
            lib_file.write(new_lib_data)


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