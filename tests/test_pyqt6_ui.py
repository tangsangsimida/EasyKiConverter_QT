#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EasyKiConverter PyQt6 UI 测试脚本
用于验证核心功能是否正常工作
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.insert(0, str(parent_dir))

def test_imports():
    """测试模块导入"""
    print("🧪 测试模块导入...")
    
    try:
        # 测试PyQt6导入
        from PyQt6.QtWidgets import QApplication, QWidget
        from PyQt6.QtCore import Qt, pyqtSignal
        print("✅ PyQt6 模块导入成功")
        
        # 测试EasyKiConverter核心模块
        from easyeda.easyeda_api import EasyedaApi
        from kicad.export_kicad_symbol import ExporterSymbolKicad
        print("✅ EasyKiConverter 核心模块导入成功")
        
        # 测试UI模块
        from utils.config_manager import ConfigManager
        from utils.style_manager import StyleManager
        from utils.bom_parser import BOMParser
        from utils.component_validator import ComponentValidator
        print("✅ UI工具模块导入成功")
        
        # 测试工作线程
        from workers.export_worker import ExportWorker
        print("✅ 工作线程模块导入成功")
        
        return True
        
    except ImportError as e:
        print(f"❌ 模块导入失败: {e}")
        return False

def test_config_manager():
    """测试配置管理器"""
    print("\n🧪 测试配置管理器...")
    
    try:
        from utils.config_manager import ConfigManager
        
        config_manager = ConfigManager("test_config.json")
        
        # 测试默认配置
        default_config = config_manager.get_config()
        print(f"✅ 默认配置加载成功，包含 {len(default_config)} 个配置项")
        
        # 测试配置更新
        test_config = {
            "export_path": "/test/path",
            "file_prefix": "test_prefix",
            "theme": "dark"
        }
        
        success = config_manager.save_config(test_config)
        if success:
            print("✅ 配置保存成功")
        else:
            print("❌ 配置保存失败")
            return False
            
        # 测试配置加载
        loaded_config = config_manager.get_config()
        if loaded_config.get("export_path") == "/test/path":
            print("✅ 配置加载正确")
        else:
            print("❌ 配置加载错误")
            return False
            
        # 清理测试文件
        config_file = Path("test_config.json")
        if config_file.exists():
            config_file.unlink()
            
        return True
        
    except Exception as e:
        print(f"❌ 配置管理器测试失败: {e}")
        return False

def test_component_validator():
    """测试元件编号验证器"""
    print("\n🧪 测试元件编号验证器...")
    
    try:
        from utils.component_validator import ComponentValidator
        
        validator = ComponentValidator()
        
        # 测试有效的LCSC ID
        test_cases = [
            ("C2040", "C2040"),
            ("https://item.szlcsc.com/2040.html", "C2040"),
            ("C12345", "C12345"),
            ("invalid_id", None),
            ("", None)
        ]
        
        for input_text, expected in test_cases:
            result = validator.extract_lcsc_id(input_text)
            if result == expected or (expected is True and result == input_text):
                print(f"✅ 测试通过: {input_text} -> {result}")
            else:
                print(f"❌ 测试失败: {input_text} -> {result} (期望: {expected})")
                return False
                
        return True
        
    except Exception as e:
        print(f"❌ 元件编号验证器测试失败: {e}")
        return False

def test_bom_parser():
    """测试BOM文件解析器"""
    print("\n🧪 测试BOM文件解析器...")
    
    try:
        from utils.bom_parser import BOMParser
        
        parser = BOMParser()
        
        # 测试BOM信息获取
        info = parser.get_bom_info("nonexistent_file.xlsx")
        if not info['exists']:
            print("✅ BOM文件存在性检查正确")
        else:
            print("❌ BOM文件存在性检查错误")
            return False
            
        # 测试格式验证
        valid_format = parser._validate_component_format("C2040")
        if valid_format:
            print("✅ 元件格式验证正确")
        else:
            print("❌ 元件格式验证错误")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ BOM文件解析器测试失败: {e}")
        return False

def test_style_manager():
    """测试样式管理器"""
    print("\n🧪 测试样式管理器...")
    
    try:
        from utils.style_manager import StyleManager
        
        style_manager = StyleManager()
        
        # 测试主题获取
        themes = style_manager.get_available_themes()
        if "light" in themes and "dark" in themes:
            print(f"✅ 主题列表正确: {themes}")
        else:
            print("❌ 主题列表错误")
            return False
            
        # 测试主题颜色
        colors = style_manager.get_theme_colors("light")
        if "primary" in colors and "background" in colors:
            print("✅ 主题颜色获取正确")
        else:
            print("❌ 主题颜色获取错误")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ 样式管理器测试失败: {e}")
        return False

def test_export_worker():
    """测试导出工作线程（不实际执行）"""
    print("\n🧪 测试导出工作线程...")
    
    try:
        from workers.export_worker import ExportWorker
        
        # 测试工作线程创建
        worker = ExportWorker(
            component_ids=["C2040"],
            options={"symbol": True, "footprint": True, "model3d": True},
            export_path="",
            file_prefix="test"
        )
        
        # 测试LCSC ID提取
        lcsc_id = worker.extract_lcsc_id_from_url("https://item.szlcsc.com/2040.html")
        if lcsc_id == "C2040":
            print("✅ LCSC ID提取正确")
        else:
            print(f"❌ LCSC ID提取错误: {lcsc_id}")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ 导出工作线程测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("=" * 50)
    print("🚀 EasyKiConverter PyQt6 UI 功能测试")
    print("=" * 50)
    
    test_results = []
    
    # 运行所有测试
    test_results.append(("模块导入", test_imports()))
    test_results.append(("配置管理器", test_config_manager()))
    test_results.append(("元件编号验证器", test_component_validator()))
    test_results.append(("BOM文件解析器", test_bom_parser()))
    test_results.append(("样式管理器", test_style_manager()))
    test_results.append(("导出工作线程", test_export_worker()))
    
    # 统计结果
    passed = sum(1 for _, result in test_results if result)
    total = len(test_results)
    
    print("\n" + "=" * 50)
    print("📊 测试结果汇总")
    print("=" * 50)
    
    for test_name, result in test_results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{test_name}: {status}")
    
    print(f"\n总计: {passed}/{total} 个测试通过")
    
    if passed == total:
        print("\n🎉 所有测试通过！PyQt6 UI核心功能正常")
        print("\n下一步:")
        print("1. 安装PyQt6: pip install PyQt6>=6.4.0")
        print("2. 运行完整应用: python PyQt6_UI/main.py")
        print("3. 或使用打包脚本创建可执行文件")
        return 0
    else:
        print(f"\n⚠️  {total - passed} 个测试失败，请检查相关模块")
        return 1

if __name__ == "__main__":
    sys.exit(main())