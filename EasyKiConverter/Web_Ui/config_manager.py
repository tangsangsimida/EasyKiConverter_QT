import json
import os
from typing import Dict, Any, Optional
from pathlib import Path

class ConfigManager:
    """用户配置管理器，支持保存和加载用户设置"""
    
    def __init__(self, config_file: str = "user_config.json"):
        self.config_dir = Path(__file__).parent
        self.config_file = self.config_dir / config_file
        self.default_config = {
            "output_folder_path": "",
            "output_lib_name": "",
            "export_options": {
                "symbol": True,
                "footprint": True,
                "model3d": True
            },
            "last_component_ids": []
        }
    
    def load_config(self) -> Dict[str, Any]:
        """加载用户配置，如果文件不存在则返回默认配置"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                # 合并默认配置，确保所有必要的键都存在
                return self._merge_config(self.default_config, config)
            else:
                return self.default_config.copy()
        except (json.JSONDecodeError, IOError) as e:
            print(f"配置文件加载失败: {e}，使用默认配置")
            return self.default_config.copy()
    
    def save_config(self, config: Dict[str, Any]) -> bool:
        """保存用户配置到文件"""
        try:
            # 确保配置目录存在
            self.config_dir.mkdir(exist_ok=True)
            
            # 合并当前配置和新配置
            current_config = self.load_config()
            merged_config = self._merge_config(current_config, config)
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(merged_config, f, ensure_ascii=False, indent=2)
            return True
        except IOError as e:
            print(f"配置文件保存失败: {e}")
            return False
    
    def update_last_settings(self, export_path: str, file_prefix: str, 
                           export_options: Dict[str, bool], component_ids: list = None) -> bool:
        """更新最后使用的设置"""
        config_update = {
            "output_folder_path": export_path or "",
            "output_lib_name": file_prefix or "",
            "export_options": export_options
        }
        
        # 可选择是否保存组件ID（可能包含敏感信息）
        if component_ids and len(component_ids) <= 10:  # 只保存少量ID作为示例
            config_update["last_component_ids"] = component_ids[:10]
        
        return self.save_config(config_update)
    
    def get_last_settings(self) -> Dict[str, Any]:
        """获取最后使用的设置"""
        config = self.load_config()
        return {
            "output_folder_path": config.get("output_folder_path", ""),
            "output_lib_name": config.get("output_lib_name", ""),
            "export_options": config.get("export_options", self.default_config["export_options"]),
            "last_component_ids": config.get("last_component_ids", [])
        }
    
    def _merge_config(self, base: Dict[str, Any], update: Dict[str, Any]) -> Dict[str, Any]:
        """递归合并配置字典"""
        result = base.copy()
        for key, value in update.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_config(result[key], value)
            else:
                result[key] = value
        return result
    
    def reset_config(self) -> bool:
        """重置配置为默认值"""
        try:
            if self.config_file.exists():
                self.config_file.unlink()
            return True
        except IOError as e:
            print(f"重置配置失败: {e}")
            return False