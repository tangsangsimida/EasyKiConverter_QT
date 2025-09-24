#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试元件验证器修复效果
"""

import sys
sys.path.insert(0, '/home/dennis/Desktop/workspace/github_projects/EasyKiConverter/EasyKiConverter')

from PyQt6_UI.utils.component_validator import ComponentValidator

def test_validator():
    """测试验证器"""
    validator = ComponentValidator()
    
    # 测试用例
    test_cases = [
        "C2040",      # 用户提到的案例
        "C123456",    # 标准LCSC格式
        "C1",         # 最短的LCSC格式
        "ESP32",      # 普通元件型号
        "STM32F103",  # 复杂元件型号
        "123ABC",     # 非标准格式
        "",           # 空字符串
    ]
    
    print("=== 元件验证器测试结果 ===")
    for test_case in test_cases:
        print(f"\n测试: {test_case}")
        
        # 提取LCSC ID
        lcsc_id = validator.extract_lcsc_id(test_case)
        print(f"  提取LCSC ID: {lcsc_id}")
        
        # 验证格式
        is_valid = validator.validate_component_format(test_case)
        print(f"  格式验证: {'通过' if is_valid else '失败'}")
        
        # 标准化
        normalized = validator.normalize_component_id(test_case)
        print(f"  标准化结果: {normalized}")
        
        # 获取详细信息
        info = validator.get_component_info(test_case)
        print(f"  是否有效: {info['is_valid']}")
        print(f"  是否LCSC格式: {info['is_lcsc_format']}")

if __name__ == "__main__":
    test_validator()