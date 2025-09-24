# -*- coding: utf-8 -*-
"""
BOM文件解析器 - 复用Web UI的BOM解析逻辑
"""

import os
import pandas as pd
from pathlib import Path
from typing import Dict, List, Any, Optional


class BOMParser:
    """BOM文件解析器"""
    
    def __init__(self):
        self.supported_formats = ['.xlsx', '.xls', '.csv']
        
    def parse_bom_file(self, file_path: str) -> Dict[str, Any]:
        """
        解析BOM文件，提取Supplier Part列中的元件编号
        
        Args:
            file_path: BOM文件路径
            
        Returns:
            Dict包含:
                - success: 是否成功
                - component_ids: 提取的元件编号列表
                - total_count: 元件总数
                - column_name: 使用的列名
                - message: 处理消息
                - error: 错误信息（如果失败）
        """
        try:
            # 验证文件存在
            file_path = Path(file_path)
            if not file_path.exists():
                return {
                    'success': False,
                    'error': f'文件不存在: {file_path}'
                }
                
            # 验证文件格式
            file_ext = file_path.suffix.lower()
            if file_ext not in self.supported_formats:
                return {
                    'success': False,
                    'error': f'不支持的文件格式: {file_ext}。支持的格式: {", ".join(self.supported_formats)}'
                }
                
            # 读取文件内容
            df = self._read_bom_file(file_path)
            if df is None:
                return {
                    'success': False,
                    'error': '无法读取BOM文件内容'
                }
                
            # 查找元件编号列
            component_column = self._find_component_column(df)
            if not component_column:
                return {
                    'success': False,
                    'error': f'未找到元器件编号列。支持的列名包括: Supplier Part, LCSC, Part Number, Component ID, MPN等\n可用列名: {", ".join(df.columns)}'
                }
                
            # 提取元件编号
            component_ids = self._extract_component_ids(df, component_column)
            
            if not component_ids:
                return {
                    'success': False,
                    'error': f'在"{component_column}"列中没有找到有效的元件编号'
                }
                
            # 去重并保持顺序
            unique_component_ids = self._deduplicate_components(component_ids)
            
            return {
                'success': True,
                'component_ids': unique_component_ids,
                'total_count': len(unique_component_ids),
                'column_name': component_column,
                'message': f'从"{component_column}"列成功解析 {len(unique_component_ids)} 个唯一元件编号'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'BOM解析失败: {str(e)}'
            }
            
    def _read_bom_file(self, file_path: Path) -> Optional[pd.DataFrame]:
        """读取BOM文件"""
        try:
            file_ext = file_path.suffix.lower()
            
            if file_ext == '.csv':
                # 尝试不同的编码读取CSV文件
                encodings = ['utf-8', 'gbk', 'latin-1']
                for encoding in encodings:
                    try:
                        return pd.read_csv(file_path, encoding=encoding)
                    except UnicodeDecodeError:
                        continue
                return None
                
            elif file_ext in ['.xlsx', '.xls']:
                # Excel文件 - 首先尝试自动检测表头位置
                try:
                    # 读取前10行来检测表头
                    df_temp = pd.read_excel(file_path, header=None, nrows=10)
                    header_row = self._find_header_row(df_temp)
                    
                    if header_row is not None:
                        # 重新读取文件，使用找到的表头行
                        return pd.read_excel(file_path, header=header_row)
                    else:
                        # 如果没找到，尝试默认方式读取
                        return pd.read_excel(file_path)
                        
                except Exception as e:
                    print(f"Excel读取失败，尝试默认方式: {e}")
                    return pd.read_excel(file_path)
                    
            else:
                return None
                
        except Exception as e:
            print(f"读取BOM文件失败: {e}")
            return None
            
    def _find_header_row(self, df: pd.DataFrame) -> Optional[int]:
        """查找包含表头的行"""
        try:
            component_column_keywords = [
                'supplier part', 'supplier_part', 'lcsc', 'lcsc part', 'lcsc_part',
                'part number', 'part_number', 'component id', 'component_id',
                'mpn', 'manufacturer part', 'manufacturer_part',
                'no.', 'quantity', 'comment', 'designator', 'footprint', 'value'
            ]
            
            # 检查前10行
            for i in range(min(10, len(df))):
                row = df.iloc[i]
                row_str = ' '.join([str(x) for x in row if pd.notna(x)]).lower()
                
                # 检查是否包含任何元器件编号相关的关键词
                for keyword in component_column_keywords:
                    if keyword in row_str:
                        return i
                        
            return None
            
        except Exception as e:
            print(f"查找表头行失败: {e}")
            return None
            
    def _find_component_column(self, df: pd.DataFrame) -> Optional[str]:
        """查找元件编号列"""
        try:
            component_column_keywords = [
                'supplier part', 'supplier_part', 'lcsc', 'lcsc part', 'lcsc_part',
                'part number', 'part_number', 'component id', 'component_id',
                'mpn', 'manufacturer part', 'manufacturer_part'
            ]
            
            # 优先查找 Supplier Part 列（嘉立创BOM标准格式）
            for col in df.columns:
                col_lower = str(col).lower().strip()
                if 'supplier part' in col_lower:
                    return col
                    
            # 如果没找到 Supplier Part，再查找其他可能的列名
            for col in df.columns:
                col_lower = str(col).lower()
                for keyword in component_column_keywords:
                    if keyword in col_lower:
                        return col
                        
            return None
            
        except Exception as e:
            print(f"查找元件编号列失败: {e}")
            return None
            
    def _extract_component_ids(self, df: pd.DataFrame, column_name: str) -> List[str]:
        """从指定列提取元件编号"""
        try:
            component_ids = []
            
            for value in df[column_name].dropna():
                # 转换为字符串并清理
                component_id = str(value).strip()
                if component_id and component_id.lower() != 'nan':
                    # 检查是否是有效的元件编号（通常以字母开头）
                    if len(component_id) > 1:
                        component_ids.append(component_id)
                        
            return component_ids
            
        except Exception as e:
            print(f"提取元件编号失败: {e}")
            return []
            
    def _deduplicate_components(self, component_ids: List[str]) -> List[str]:
        """去重并保持顺序"""
        seen = set()
        unique_ids = []
        
        for component_id in component_ids:
            if component_id not in seen:
                unique_ids.append(component_id)
                seen.add(component_id)
                
        return unique_ids
        
    def validate_bom_file(self, file_path: str) -> Dict[str, Any]:
        """
        验证BOM文件格式
        
        Args:
            file_path: BOM文件路径
            
        Returns:
            Dict包含验证结果
        """
        try:
            result = self.parse_bom_file(file_path)
            
            if not result['success']:
                return {
                    'valid': False,
                    'error': result['error']
                }
                
            component_ids = result['component_ids']
            
            if not component_ids:
                return {
                    'valid': False,
                    'error': 'BOM文件中没有找到有效的元件编号'
                }
                
            # 验证元件编号格式
            valid_count = 0
            invalid_components = []
            
            for component_id in component_ids:
                if self._validate_component_format(component_id):
                    valid_count += 1
                else:
                    invalid_components.append(component_id)
                    
            return {
                'valid': True,
                'total_components': len(component_ids),
                'valid_components': valid_count,
                'invalid_components': invalid_components,
                'column_name': result['column_name'],
                'component_ids': component_ids
            }
            
        except Exception as e:
            return {
                'valid': False,
                'error': f'验证失败: {str(e)}'
            }
            
    def _validate_component_format(self, component_id: str) -> bool:
        """验证元件编号格式"""
        # 基本的格式验证 - 可以扩展
        if not component_id or len(component_id) < 2:
            return False
            
        # 检查是否包含有效的字符
        import re
        # 允许字母、数字、下划线、连字符
        if not re.match(r'^[A-Za-z0-9_-]+$', component_id):
            return False
            
        # 检查是否以字母开头（LCSC编号通常以C开头）
        if not component_id[0].isalpha():
            return False
            
        return True
        
    def get_bom_info(self, file_path: str) -> Dict[str, Any]:
        """获取BOM文件基本信息"""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                return {
                    'exists': False,
                    'error': '文件不存在'
                }
                
            # 读取文件获取基本信息
            df = self._read_bom_file(file_path)
            if df is None:
                return {
                    'exists': True,
                    'readable': False,
                    'error': '无法读取文件内容'
                }
                
            return {
                'exists': True,
                'readable': True,
                'file_name': file_path.name,
                'file_size': file_path.stat().st_size,
                'row_count': len(df),
                'column_count': len(df.columns),
                'columns': list(df.columns),
                'file_type': file_path.suffix.lower()
            }
            
        except Exception as e:
            return {
                'exists': True,
                'readable': False,
                'error': str(e)
            }