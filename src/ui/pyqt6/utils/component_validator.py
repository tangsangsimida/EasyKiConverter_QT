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
        self.lcsc_patterns = [
            # 标准LCSC编号格式
            r'\b(C\d{1,10})\b',
            # 嘉立创URL中的LCSC编号
            r'item\.szlcsc\.com/(\d+)',
            r'item\.szlcsc\.com/(C\d+)',
            # 可能的变体格式
            r'LCSC[:\s]*(C\d{1,10})',
            r'编号[:\s]*(C\d{1,10})',
            r'Part\s*Number[:\s]*(C\d{1,10})',
        ]
        
        # 通用元件编号模式（用于非LCSC格式）
        self.generic_patterns = [
            # 常见的元件编号格式
            r'\b([A-Z]{1,3}\d{3,8}[A-Z]?)\b',  # 如：CC2040, ESP32, LM358N
            r'\b([A-Z]\d+[A-Z]+[A-Z0-9]*)\b',  # 如：LM358N, NE555P
        ]
        
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
        
        # 遍历所有LCSC模式
        for pattern in self.lcsc_patterns:
            matches = re.findall(pattern, component_id, re.IGNORECASE)
            for match in matches:
                # 确保ID以C开头
                if isinstance(match, tuple):
                    match = match[0]  # 取第一个捕获组
                    
                if match and not match.startswith('C'):
                    match = 'C' + match
                    
                # 验证格式
                if self._is_valid_lcsc_id(match):
                    return match
                    
        # 直接匹配LCSC格式（C+数字）
        lcsc_match = re.search(r'\b(C\d+)\b', component_id)
        if lcsc_match:
            return lcsc_match.group(1)
            
        # 如果不是LCSC格式，返回None
        return None
        
    def _is_valid_lcsc_id(self, component_id: str) -> bool:
        """
        验证LCSC元件ID格式
        
        Args:
            component_id: 元件ID
            
        Returns:
            是否为有效的LCSC元件ID
        """
        if not component_id or not isinstance(component_id, str):
            return False
            
        # 必须以C开头，后跟数字
        return bool(re.match(r'^C\d+$', component_id))
        
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