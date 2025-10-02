# -*- coding: utf-8 -*-
"""
配置管理器 - 复用Web UI的配置管理逻辑
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional, List


class ConfigManager:
    """配置管理器"""
    
    def __init__(self, config_file: str = "user_config.json"):
        """
        初始化配置管理器
        
        Args:
            config_file: 配置文件名
        """
        self.config_file = Path(__file__).parent.parent / config_file
        self.default_config = self._get_default_config()
        self.config = self.load_config()
        
    def _get_default_config(self) -> Dict[str, Any]:
        """获取默认配置"""
        return {
            "export_path": "",  # 导出路径
            "file_prefix": "",  # 文件前缀
            "export_options": {  # 导出选项
                "symbol": True,
                "footprint": True,
                "model3d": True
            },
            "component_ids": [],  # 最近使用的元件编号
            "window_geometry": None,  # 窗口几何信息
            "window_state": None,  # 窗口状态
            "language": "zh_CN",  # 语言
            "auto_save": True,  # 自动保存配置
            "max_recent_components": 100,  # 最大最近元件数
            "parallel_workers": 15,  # 并行工作线程数
            "debug_mode": False,  # 调试模式
            "log_level": "INFO",  # 日志级别
            "check_updates": True,  # 检查更新
            "confirm_delete": True,  # 删除确认
            "show_tips": True,  # 显示提示
            "last_used_path": "",  # 最后使用的路径
            "file_dialog_path": "",  # 文件对话框路径
            "network_timeout": 30,  # 网络请求超时时间（秒）
            "max_retries": 3,  # 网络请求最大重试次数
            "retry_delay": 1,  # 重试延迟时间（秒）
        }
        
    def load_config(self) -> Dict[str, Any]:
        """
        加载配置文件
        
        Returns:
            配置字典
        """
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    
                # 合并默认配置和加载的配置
                config = self.default_config.copy()
                config.update(loaded_config)
                
                # 验证配置完整性
                config = self._validate_config(config)
                
                return config
            else:
                # 如果配置文件不存在，创建默认配置
                self.save_config(self.default_config)
                return self.default_config.copy()
                
        except Exception as e:
            print(f"加载配置文件失败: {e}")
            # 如果加载失败，返回默认配置
            return self.default_config.copy()
            
    def save_config(self, config: Dict[str, Any]) -> bool:
        """
        保存配置到文件
        
        Args:
            config: 配置字典
            
        Returns:
            是否保存成功
        """
        try:
            # 确保配置目录存在
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            
            # 验证配置
            config = self._validate_config(config)
            
            # 保存配置
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
                
            self.config = config  # 更新内存中的配置
            return True
            
        except Exception as e:
            print(f"保存配置文件失败: {e}")
            return False
            
    def _validate_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """验证和修复配置"""
        validated_config = self.default_config.copy()
        
        # 更新已知字段
        for key in validated_config.keys():
            if key in config:
                validated_config[key] = config[key]
                
        # 特殊验证
        if 'export_options' in config:
            # 确保导出选项是有效的
            export_options = config['export_options']
            if isinstance(export_options, dict):
                for option in ['symbol', 'footprint', 'model3d']:
                    if option in export_options:
                        validated_config['export_options'][option] = bool(export_options[option])
                        
        # 限制最近元件数量
        if 'component_ids' in config and isinstance(config['component_ids'], list):
            component_ids = config['component_ids']
            max_recent = validated_config.get('max_recent_components', 100)
            if len(component_ids) > max_recent:
                validated_config['component_ids'] = component_ids[-max_recent:]
            else:
                validated_config['component_ids'] = component_ids
                
        return validated_config
        
    def get_config(self) -> Dict[str, Any]:
        """获取当前配置"""
        return self.config.copy()
        
    def get_last_settings(self) -> Dict[str, Any]:
        """获取最后使用的设置（兼容Web UI接口）"""
        return {
            "export_path": self.config.get("export_path", ""),
            "file_prefix": self.config.get("file_prefix", ""),
            "export_options": self.config.get("export_options", self.default_config["export_options"]),
            "component_ids": self.config.get("component_ids", []),
            "theme": self.config.get("theme", "light"),
            "language": self.config.get("language", "zh_CN"),
        }
        
    def update_last_settings(self, export_path: str = "", file_prefix: str = "",
                           export_options: Dict[str, bool] = None,
                           component_ids: list = None) -> bool:
        """
        更新最后使用的设置（兼容Web UI接口）
        
        Args:
            export_path: 导出路径
            file_prefix: 文件前缀
            export_options: 导出选项
            component_ids: 元件编号列表
            
        Returns:
            是否更新成功
        """
        try:
            if export_path is not None:
                self.config["export_path"] = export_path
                
            if file_prefix is not None:
                self.config["file_prefix"] = file_prefix
                
            if export_options is not None:
                self.config["export_options"] = export_options
                
            if component_ids is not None:
                self.config["component_ids"] = component_ids
                
            return self.save_config(self.config)
            
        except Exception as e:
            print(f"更新设置失败: {e}")
            return False
            
    def get_export_path(self) -> str:
        """获取导出路径"""
        return self.config.get("export_path", "")
        
    def set_export_path(self, path: str) -> bool:
        """设置导出路径"""
        self.config["export_path"] = path
        return self.save_config(self.config)
        
    def get_file_prefix(self) -> str:
        """获取文件前缀"""
        return self.config.get("file_prefix", "")
        
    def set_file_prefix(self, prefix: str) -> bool:
        """设置文件前缀"""
        self.config["file_prefix"] = prefix
        return self.save_config(self.config)
        
    def get_export_options(self) -> Dict[str, bool]:
        """获取导出选项"""
        return self.config.get("export_options", self.default_config["export_options"]).copy()
        
    def set_export_options(self, options: Dict[str, bool]) -> bool:
        """设置导出选项"""
        self.config["export_options"] = options
        return self.save_config(self.config)
        
    def get_component_ids(self) -> List[str]:
        """获取最近使用的元件编号"""
        return self.config.get("component_ids", []).copy()
        
    def add_component_id(self, component_id: str) -> bool:
        """添加最近使用的元件编号"""
        component_ids = self.config.get("component_ids", [])
        
        # 如果已存在，先移除（移到末尾）
        if component_id in component_ids:
            component_ids.remove(component_id)
            
        # 添加到末尾
        component_ids.append(component_id)
        
        # 限制数量
        max_recent = self.config.get("max_recent_components", 100)
        if len(component_ids) > max_recent:
            component_ids = component_ids[-max_recent:]
            
        self.config["component_ids"] = component_ids
        return self.save_config(self.config)
        
    def get_theme(self) -> str:
        """获取主题"""
        return self.config.get("theme", "light")
        
    def set_theme(self, theme: str) -> bool:
        """设置主题"""
        if theme in ["light", "dark"]:
            self.config["theme"] = theme
            return self.save_config(self.config)
        return False
        
    def get_window_geometry(self) -> Optional[bytes]:
        """获取窗口几何信息"""
        return self.config.get("window_geometry")
        
    def set_window_geometry(self, geometry: bytes) -> bool:
        """设置窗口几何信息"""
        self.config["window_geometry"] = geometry
        return self.save_config(self.config)
        
    def get_window_state(self) -> Optional[bytes]:
        """获取窗口状态"""
        return self.config.get("window_state")
        
    def set_window_state(self, state: bytes) -> bool:
        """设置窗口状态"""
        self.config["window_state"] = state
        return self.save_config(self.config)
        
    def get_language(self) -> str:
        """获取语言设置"""
        return self.config.get("language", "zh_CN")
        
    def set_language(self, language: str) -> bool:
        """设置语言"""
        supported_languages = ["zh_CN", "en_US"]
        if language in supported_languages:
            self.config["language"] = language
            return self.save_config(self.config)
        return False
        
    def get_parallel_workers(self) -> int:
        """获取并行工作线程数"""
        return self.config.get("parallel_workers", 15)
        
    def set_parallel_workers(self, workers: int) -> bool:
        """设置并行工作线程数"""
        if 1 <= workers <= 50:  # 合理的范围限制
            self.config["parallel_workers"] = workers
            return self.save_config(self.config)
        return False
        
    def is_debug_mode(self) -> bool:
        """是否为调试模式"""
        return self.config.get("debug_mode", False)
        
    def set_debug_mode(self, debug: bool) -> bool:
        """设置调试模式"""
        self.config["debug_mode"] = debug
        return self.save_config(self.config)
        
    def get_log_level(self) -> str:
        """获取日志级别"""
        return self.config.get("log_level", "INFO")
        
    def set_log_level(self, level: str) -> bool:
        """设置日志级别"""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if level in valid_levels:
            self.config["log_level"] = level
            return self.save_config(self.config)
        return False
        
    def should_check_updates(self) -> bool:
        """是否应该检查更新"""
        return self.config.get("check_updates", True)
        
    def set_check_updates(self, check: bool) -> bool:
        """设置是否检查更新"""
        self.config["check_updates"] = check
        return self.save_config(self.config)
        
    def should_confirm_delete(self) -> bool:
        """删除时是否需要确认"""
        return self.config.get("confirm_delete", True)
        
    def set_confirm_delete(self, confirm: bool) -> bool:
        """设置删除确认"""
        self.config["confirm_delete"] = confirm
        return self.save_config(self.config)
        
    def should_show_tips(self) -> bool:
        """是否显示提示"""
        return self.config.get("show_tips", True)
        
    def set_show_tips(self, show: bool) -> bool:
        """设置是否显示提示"""
        self.config["show_tips"] = show
        return self.save_config(self.config)
        
    def get_last_used_path(self) -> str:
        """获取最后使用的路径"""
        return self.config.get("last_used_path", "")
        
    def set_last_used_path(self, path: str) -> bool:
        """设置最后使用的路径"""
        self.config["last_used_path"] = path
        return self.save_config(self.config)
        
    def get_file_dialog_path(self, path: str) -> bool:
        """设置文件对话框路径"""
        self.config["file_dialog_path"] = path
        return self.save_config(self.config)
        
    def get_network_timeout(self) -> int:
        """获取网络请求超时时间"""
        return self.config.get("network_timeout", 30)
        
    def set_network_timeout(self, timeout: int) -> bool:
        """设置网络请求超时时间"""
        if timeout > 0:
            self.config["network_timeout"] = timeout
            return self.save_config(self.config)
        return False
        
    def get_max_retries(self) -> int:
        """获取网络请求最大重试次数"""
        return self.config.get("max_retries", 3)
        
    def set_max_retries(self, retries: int) -> bool:
        """设置网络请求最大重试次数"""
        if retries >= 0:
            self.config["max_retries"] = retries
            return self.save_config(self.config)
        return False
        
    def get_retry_delay(self) -> int:
        """获取重试延迟时间"""
        return self.config.get("retry_delay", 1)
        
    def set_retry_delay(self, delay: int) -> bool:
        """设置重试延迟时间"""
        if delay >= 0:
            self.config["retry_delay"] = delay
            return self.save_config(self.config)
        return False
        
    def reset_to_defaults(self) -> bool:
        """重置为默认配置"""
        self.config = self.default_config.copy()
        return self.save_config(self.config)
        
    def export_config(self, export_path: str) -> bool:
        """导出配置到文件"""
        try:
            export_path = Path(export_path)
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"导出配置失败: {e}")
            return False
            
    def import_config(self, import_path: str) -> bool:
        """从文件导入配置"""
        try:
            import_path = Path(import_path)
            with open(import_path, 'r', encoding='utf-8') as f:
                imported_config = json.load(f)
                
            # 验证导入的配置
            validated_config = self._validate_config(imported_config)
            
            # 保存导入的配置
            self.config = validated_config
            return self.save_config(self.config)
            
        except Exception as e:
            print(f"导入配置失败: {e}")
            return False