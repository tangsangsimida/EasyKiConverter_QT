# Global imports
import logging

import requests

# 版本信息
__version__ = "1.0.0"

API_ENDPOINT = "https://easyeda.com/api/products/{lcsc_id}/components?version=6.4.19.5"
ENDPOINT_3D_MODEL = "https://modules.easyeda.com/3dmodel/{uuid}"
ENDPOINT_3D_MODEL_STEP = "https://modules.easyeda.com/qAxj6KHrDKw4blvCG8QJPs7Y/{uuid}"
# ENDPOINT_3D_MODEL_STEP found in https://modules.lceda.cn/smt-gl-engine/0.8.22.6032922c/smt-gl-engine.js : points to the bucket containing the step files.

# ------------------------------------------------------------


class EasyedaApi:
    """
    EasyEDA API接口类，用于与EasyEDA服务器通信获取组件数据
    EasyEDA API interface class for communicating with EasyEDA server to fetch component data
    """

    def __init__(self) -> None:
        """
        初始化API客户端，设置请求头信息
        Initialize API client and setup request headers
        """
        self.headers = {
            "Accept-Encoding": "gzip, deflate",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent": f"easyeda2kicad v{__version__}",
        }

    def get_info_from_easyeda_api(self, lcsc_id: str) -> dict:
        """
        从EasyEDA API获取指定LCSC ID的组件信息
        Fetch component information from EasyEDA API for specified LCSC ID
        
        参数:
        Args:
            lcsc_id (str): LCSC组件ID，应以'C'开头 / LCSC component ID, should start with 'C'
            
        返回:
        Returns:
            dict: API响应数据，失败时返回空字典 / API response data, empty dict on failure
        """
        r = requests.get(url=API_ENDPOINT.format(lcsc_id=lcsc_id), headers=self.headers)
        api_response = r.json()

        if not api_response or (
            "code" in api_response and api_response["success"] is False
        ):
            logging.debug(f"{api_response}")
            return {}

        return r.json()

    def get_cad_data_of_component(self, lcsc_id: str) -> dict:
        """
        获取指定LCSC ID的组件CAD数据（包含符号、封装、3D模型等信息）
        Fetch CAD data for specified LCSC ID (includes symbol, footprint, 3D model info)
        
        参数:
        Args:
            lcsc_id (str): LCSC组件ID / LCSC component ID
            
        返回:
        Returns:
            dict: 组件的完整CAD数据 / Complete CAD data of the component
        """
        cp_cad_info = self.get_info_from_easyeda_api(lcsc_id=lcsc_id)
        if cp_cad_info == {}:
            return {}
        return cp_cad_info["result"]

    def get_raw_3d_model_obj(self, uuid: str) -> str:
        """
        获取原始3D模型数据（OBJ格式）
        Fetch raw 3D model data (OBJ format)
        
        参数:
        Args:
            uuid (str): 3D模型的UUID标识符 / UUID identifier for 3D model
            
        返回:
        Returns:
            str: 3D模型OBJ文件内容，失败返回None / 3D model OBJ file content, None on failure
        """
        r = requests.get(
            url=ENDPOINT_3D_MODEL.format(uuid=uuid),
            headers={"User-Agent": self.headers["User-Agent"]},
        )
        if r.status_code != requests.codes.ok:
            logging.error(f"No raw 3D model data found for uuid:{uuid} on easyeda")
            return None
        return r.content.decode()

    def get_step_3d_model(self, uuid: str) -> bytes:
        """
        获取STEP格式的3D模型数据
        Fetch 3D model data in STEP format
        
        参数:
        Args:
            uuid (str): 3D模型的UUID标识符 / UUID identifier for 3D model
            
        返回:
        Returns:
            bytes: STEP格式的3D模型二进制数据，失败返回None / 3D model binary data in STEP format, None on failure
        """
        r = requests.get(
            url=ENDPOINT_3D_MODEL_STEP.format(uuid=uuid),
            headers={"User-Agent": self.headers["User-Agent"]},
        )
        if r.status_code != requests.codes.ok:
            logging.error(f"No step 3D model data found for uuid:{uuid} on easyeda")
            return None
        return r.content
