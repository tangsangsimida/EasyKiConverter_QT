# -*- coding: utf-8 -*-
"""
元件编号验证器
"""

import re
from typing import Optional, List


class ComponentValidator:
    """元件编号验证器"""
    
    def __init__(self):
        # LCSC编号格式：C + 数字
        self.lcsc_pattern = re.compile(r'^C\d+$')
        
        # 支持的URL格式
        self.url_patterns = [
            re.compile(r'item\.szlcsc\.com/(C?\d+)\.html'),  # 标准URL格式
            re.compile(r'item\.szlcsc\.com/(C\d+)'),         # 不带.html的格式
            re.compile(r'/(C\d+)(?:\.html)?$'),              # 任何以/C数字结尾的URL
            re.compile(r'\b(C\d+)\b')                        # 任何包含C+数字的文本
        ]
        
    def extract_lcsc_id(self, input_text: str) -> Optional[str]:
        """
        从输入文本中提取LCSC ID
        
        Args:
            input_text: 输入文本（可以是LCSC ID或URL）
            
        Returns:
            提取的LCSC ID，如果无法提取则返回None
        """
        if not input_text or not isinstance(input_text, str):
            return None
            
        input_text = input_text.strip()
        
        # 检查是否已经是LCSC ID格式
        if self.is_valid_lcsc_id(input_text):
            return input_text
            
        # 从URL中提取LCSC ID
        for pattern in self.url_patterns:
            match = pattern.search(input_text)
            if match:
                lcsc_id = match.group(1)
                # 确保以C开头
                if not lcsc_id.startswith('C'):
                    lcsc_id = 'C' + lcsc_id
                return lcsc_id
                
        return None
        
    def is_valid_lcsc_id(self, component_id: str) -> bool:
        """
        验证LCSC ID格式
        
        Args:
            component_id: 元件编号
            
        Returns:
            是否为有效的LCSC ID格式
        """
        if not component_id or not isinstance(component_id, str):
            return False
            
        return bool(self.lcsc_pattern.match(component_id.strip()))
        
    def _validate_component_format(self, component_id: str) -> bool:
        """
        验证元件编号格式（更通用的验证）
        
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
        if not re.match(r'^[A-Za-z0-9_-]+
        
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
                # 尝试通用验证
                normalized = self.normalize_component_id(component_id)
                if normalized:
                    info['normalized'] = normalized
                    info['is_valid'] = True
                else:
                    info['error'] = '无效的元件编号格式'
                    
        except Exception as e:
            info['error'] = f'验证失败: {str(e)}'
            
        return info, component_id):
            return False
            
        # 检查是否以字母开头（LCSC编号通常以C开头）
        if not component_id[0].isalpha():
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
                # 尝试通用验证
                normalized = self.normalize_component_id(component_id)
                if normalized:
                    info['normalized'] = normalized
                    info['is_valid'] = True
                else:
                    info['error'] = '无效的元件编号格式'
                    
        except Exception as e:
            info['error'] = f'验证失败: {str(e)}'
            
        return info