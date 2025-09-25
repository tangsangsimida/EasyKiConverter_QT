# EasyEDA模块初始化
from .easyeda_api import EasyedaApi
from .easyeda_importer import EasyedaSymbolImporter, EasyedaFootprintImporter, Easyeda3dModelImporter
from .svg_path_parser import parse_svg_path
from .parameters_easyeda import *

# 创建统一的EasyEDAImporter类
class EasyEDAImporter:
    """统一的EasyEDA导入器类"""
    
    def __init__(self):
        """初始化导入器"""
        self.api = EasyedaApi()
        
    def import_component(self, lcsc_id: str):
        """
        导入指定LCSC ID的元件数据
        
        Args:
            lcsc_id: LCSC元件ID (必须以'C'开头)
            
        Returns:
            包含符号、封装和3D模型数据的字典，失败时返回None
        """
        try:
            # 验证LCSC ID格式
            if not lcsc_id or not lcsc_id.startswith('C'):
                print(f"Invalid LCSC ID format: {lcsc_id}")
                return None
                
            # 从EasyEDA API获取数据
            api_data = self.api.get_info_from_easyeda_api(lcsc_id)
            if not api_data:
                print(f"Failed to fetch data for LCSC ID: {lcsc_id}")
                return None
                
            # 检查API响应是否成功 - 适配新的API响应格式
            if not api_data.get("success", False):
                print(f"API error for LCSC ID {lcsc_id}: {api_data.get('result', 'Unknown error')}")
                return None
                
            component_data = api_data.get("result", {})
            if not component_data:
                print(f"No component data found for LCSC ID: {lcsc_id}")
                return None
                
            # 调试：打印返回的数据结构
            print(f"成功获取LCSC ID {lcsc_id} 的数据结构:")
            print(f"- 数据键: {list(component_data.keys())}")
            if 'dataStr' in component_data:
                print(f"- dataStr键: {list(component_data['dataStr'].keys()) if isinstance(component_data['dataStr'], dict) else '不是字典'}")
            if 'packageDetail' in component_data:
                print(f"- packageDetail键: {list(component_data['packageDetail'].keys()) if isinstance(component_data['packageDetail'], dict) else '不是字典'}")
            
            print(f"Successfully imported component data for LCSC ID: {lcsc_id}")
            return component_data
            
        except Exception as e:
            print(f"Error importing component {lcsc_id}: {str(e)}")
            return None

__all__ = [
    'EasyedaApi',
    'EasyEDAImporter', 
    'EasyedaSymbolImporter',
    'EasyedaFootprintImporter', 
    'Easyeda3dModelImporter',
    'parse_svg_path'
]