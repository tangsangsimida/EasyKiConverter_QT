#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
剪贴板处理器模块
用于从剪贴板文本中智能提取和处理元件ID
"""

import re
from typing import List, Set, Optional
from PyQt6.QtWidgets import QApplication


class ClipboardProcessor:
    """剪贴板处理器类"""
    
    def __init__(self):
        """初始化剪贴板处理器"""
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
        
    def extract_component_ids(self, text: str) -> List[str]:
        """
        从文本中提取元件ID
        
        Args:
            text: 输入文本
            
        Returns:
            提取的元件ID列表
        """
        if not text or not isinstance(text, str):
            return []
            
        # 清理文本
        text = text.strip()
        if not text:
            return []
            
        component_ids = []
        
        # 1. 首先尝试提取LCSC编号
        lcsc_ids = self._extract_lcsc_ids(text)
        component_ids.extend(lcsc_ids)
        
        # 2. 如果没有找到LCSC编号，尝试提取通用元件编号
        if not component_ids:
            generic_ids = self._extract_generic_ids(text)
            component_ids.extend(generic_ids)
            
        # 3. 去重并保持顺序
        unique_ids = self._deduplicate_ids(component_ids)
        
        return unique_ids
        
    def _extract_lcsc_ids(self, text: str) -> List[str]:
        """
        从文本中提取LCSC元件ID
        
        Args:
            text: 输入文本
            
        Returns:
            提取的LCSC元件ID列表
        """
        ids = []
        
        # 遍历所有LCSC模式
        for pattern in self.lcsc_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                # 确保ID以C开头
                if isinstance(match, tuple):
                    match = match[0]  # 取第一个捕获组
                    
                if match and not match.startswith('C'):
                    match = 'C' + match
                    
                # 验证格式
                if self._is_valid_lcsc_id(match):
                    ids.append(match)
                    
        return ids
        
    def _extract_generic_ids(self, text: str) -> List[str]:
        """
        从文本中提取通用元件ID
        
        Args:
            text: 输入文本
            
        Returns:
            提取的通用元件ID列表
        """
        ids = []
        
        # 遍历所有通用模式
        for pattern in self.generic_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if self._is_valid_generic_id(match):
                    ids.append(match.upper())  # 统一转为大写
                    
        return ids
        
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
        
    def _is_valid_generic_id(self, component_id: str) -> bool:
        """
        验证通用元件ID格式
        
        Args:
            component_id: 元件ID
            
        Returns:
            是否为有效的通用元件ID
        """
        if not component_id or not isinstance(component_id, str):
            return False
            
        component_id = component_id.strip()
        
        # 基本长度检查
        if len(component_id) < 2 or len(component_id) > 20:
            return False
            
        # 检查是否包含有效的字符（字母、数字）
        if not re.match(r'^[A-Z0-9]+$', component_id):
            return False
            
        # 必须包含至少一个字母和一个数字
        has_letter = bool(re.search(r'[A-Z]', component_id))
        has_digit = bool(re.search(r'\d', component_id))
        
        return has_letter and has_digit
        
    def _deduplicate_ids(self, ids: List[str]) -> List[str]:
        """
        去重元件ID并保持顺序
        
        Args:
            ids: 元件ID列表
            
        Returns:
            去重后的元件ID列表
        """
        if not ids:
            return []
            
        seen: Set[str] = set()
        unique_ids = []
        
        for component_id in ids:
            if component_id and component_id not in seen:
                unique_ids.append(component_id)
                seen.add(component_id)
                
        return unique_ids
        
    def process_clipboard_text(self, text: str) -> List[str]:
        """
        处理剪贴板文本并提取元件ID
        
        Args:
            text: 剪贴板文本
            
        Returns:
            提取的元件ID列表
        """
        if not text or not isinstance(text, str):
            return []
            
        # 清理文本
        text = text.strip()
        if not text:
            return []
            
        # 提取元件ID
        component_ids = self.extract_component_ids(text)
        
        return component_ids
        
    def get_clipboard_component_ids(self) -> List[str]:
        """
        从剪贴板获取元件ID
        
        Returns:
            提取的元件ID列表
        """
        try:
            clipboard = QApplication.clipboard()
            text = clipboard.text().strip()
            return self.process_clipboard_text(text)
        except Exception:
            return []
            
    def get_component_info(self, text: str) -> dict:
        """
        获取剪贴板文本中的元件信息
        
        Args:
            text: 剪贴板文本
            
        Returns:
            元件信息字典
        """
        info = {
            'original_text': text,
            'component_ids': [],
            'count': 0,
            'has_lcsc_ids': False,
            'has_generic_ids': False,
            'errors': []
        }
        
        try:
            if not text or not isinstance(text, str):
                info['errors'].append('Empty or invalid text')
                return info
                
            # 清理文本
            text = text.strip()
            if not text:
                info['errors'].append('Empty text')
                return info
                
            # 提取LCSC ID
            lcsc_ids = self._extract_lcsc_ids(text)
            generic_ids = []
            
            # 如果没有LCSC ID，尝试通用ID
            if not lcsc_ids:
                generic_ids = self._extract_generic_ids(text)
                
            all_ids = lcsc_ids + generic_ids
            unique_ids = self._deduplicate_ids(all_ids)
            
            info['component_ids'] = unique_ids
            info['count'] = len(unique_ids)
            info['has_lcsc_ids'] = len(lcsc_ids) > 0
            info['has_generic_ids'] = len(generic_ids) > 0
            
        except Exception as e:
            info['errors'].append(str(e))
            
        return info
