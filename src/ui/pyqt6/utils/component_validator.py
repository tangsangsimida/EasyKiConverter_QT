#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
元件验证器模块
用于验证和标准化元件编号
"""

import re
from typing import Optional, List


class ComponentValidator:
    """元件验证器类"""
    
    def __init__(self):
        """初始化验证器"""
        # LCSC元件编号的正则表达式模式（C+至少1位数字）
        self.lcsc_pattern = re.compile(r'C\d+')
        
    def extract_lcsc_id(self, component_id: str) -> Optional[str]:
        """
        从元件编号或URL中提取LCSC ID
        
        Args:
            component_id: 元件编号或URL
            
        Returns:
            提取的LCSC ID，如果未找到则返回None
        """
        if not component_id or not isinstance(component_id, str):
            return None
            
        # 清理输入
        component_id = component_id.strip()
        
        # 直接匹配LCSC格式（C+数字）
        match = self.lcsc_pattern.search(component_id)
        if match:
            return match.group()
            
        # 如果不是LCSC格式，返回None
        return None
        
    def validate_component_format(self, component_id: str) -> bool:
        """
        验证元件编号格式
        
        Args:
            component_id: 元件编号
            
        Returns:
            是否为有效的元件编号格式
        """
        if not component_id or not isinstance(component_id, str):
            return False
            
        component_id = component_id.strip()
        
        # 基本长度检查
        if len(component_id) < 2:
            return False
            
        # 检查是否包含有效的字符（字母、数字、下划线、连字符）
        if not re.match(r'^[A-Za-z0-9_-]+$', component_id):
            return False
            
        return True
        
    def normalize_component_id(self, component_id: str) -> Optional[str]:
        """
        标准化元件编号
        
        Args:
            component_id: 元件编号
            
        Returns:
            标准化的元件编号，如果无效则返回None
        """
        if not component_id or not isinstance(component_id, str):
            return None
            
        # 提取LCSC ID
        lcsc_id = self.extract_lcsc_id(component_id)
        if lcsc_id:
            return lcsc_id
            
        # 如果不是LCSC格式，尝试通用标准化
        normalized = component_id.strip()
        if self.validate_component_format(normalized):
            return normalized
            
        return None
        
    def filter_valid_components(self, component_ids: List[str]) -> List[str]:
        """
        过滤有效的元件编号
        
        Args:
            component_ids: 元件编号列表
            
        Returns:
            有效的元件编号列表
        """
        if not component_ids:
            return []
            
        valid_components = []
        for component_id in component_ids:
            normalized = self.normalize_component_id(component_id)
            if normalized:
                valid_components.append(normalized)
                
        return valid_components
        
    def deduplicate_components(self, component_ids: List[str]) -> List[str]:
        """
        去重元件编号并保持顺序
        
        Args:
            component_ids: 元件编号列表
            
        Returns:
            去重后的元件编号列表
        """
        if not component_ids:
            return []
            
        seen = set()
        unique_ids = []
        
        for component_id in component_ids:
            normalized = self.normalize_component_id(component_id)
            if normalized and normalized not in seen:
                unique_ids.append(normalized)
                seen.add(normalized)
                
        return unique_ids
        
    def get_component_info(self, component_id: str) -> dict:
        """
        获取元件编号信息
        
        Args:
            component_id: 元件编号
            
        Returns:
            元件信息字典
        """
        info = {
            'original': component_id,
            'normalized': None,
            'is_valid': False,
            'is_lcsc_format': False,
            'extracted_from_url': False,
            'error': None
        }
        
        try:
            # 尝试提取LCSC ID
            lcsc_id = self.extract_lcsc_id(component_id)
            
            if lcsc_id:
                info['normalized'] = lcsc_id
                info['is_valid'] = True
                info['is_lcsc_format'] = True
                info['extracted_from_url'] = lcsc_id != component_id.strip()
            else:
                # 尝试通用标准化
                normalized = self.normalize_component_id(component_id)
                if normalized:
                    info['normalized'] = normalized
                    info['is_valid'] = True
                else:
                    info['error'] = 'Invalid component format'
                    
        except Exception as e:
            info['error'] = str(e)
            
        return info