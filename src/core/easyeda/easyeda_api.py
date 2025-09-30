# Global imports
import logging
import json
import time

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# 版本信息
__version__ = "1.0.0"

API_ENDPOINT = "https://easyeda.com/api/products/{lcsc_id}/components?version=6.4.19.5"
ENDPOINT_3D_MODEL = "https://modules.easyeda.com/3dmodel/{uuid}"
ENDPOINT_3D_MODEL_STEP = "https://modules.easyeda.com/qAxj6KHrDKw4blvCG8QJPs7Y/{uuid}"
# ENDPOINT_3D_MODEL_STEP found in https://modules.lceda.cn/smt-gl-engine/0.8.22.6032922c/smt-gl-engine.js : points to the bucket containing the step files.

# 重试策略
def create_session_with_retries():
    """Create a requests session with retry strategy"""
    session = requests.Session()
    
    # 定义重试策略
    retry_strategy = Retry(
        total=3,  # 总重试次数
        backoff_factor=1,  # 重试间隔倍数
        status_forcelist=[429, 500, 502, 503, 504],  # 需要重试的HTTP状态码
        allowed_methods=["HEAD", "GET", "OPTIONS"]  # 允许重试的HTTP方法
    )
    
    # 创建适配器并应用重试策略
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    return session

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
        # 创建带重试机制的会话
        self.session = create_session_with_retries()

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
        try:
            # 构建API URL
            api_url = API_ENDPOINT.format(lcsc_id=lcsc_id)
            print(f"正在请求EasyEDA API: {api_url}")
            
            # 发送请求（使用带重试机制的会话）
            r = self.session.get(url=api_url, headers=self.headers, timeout=30)
            
            # 检查HTTP响应状态
            print(f"HTTP状态码: {r.status_code}")
            if r.status_code != 200:
                print(f"API请求失败，状态码: {r.status_code}")
                print(f"响应内容: {r.text[:500]}")  # 打印前500个字符
                return {}
            
            # 解析JSON响应
            api_response = r.json()
            print(f"API响应结构: {type(api_response)}")
            print(f"响应键: {list(api_response.keys()) if isinstance(api_response, dict) else '不是字典'}")
            
            return api_response
            
        except requests.exceptions.RequestException as e:
            print(f"网络请求错误: {e}")
            logging.error(f"网络请求错误 (LCSC ID: {lcsc_id}): {e}")
            return {}
        except json.JSONDecodeError as e:
            print(f"JSON解析错误: {e}")
            print(f"原始响应: {r.text[:500]}")
            logging.error(f"JSON解析错误 (LCSC ID: {lcsc_id}): {e}")
            return {}
        except Exception as e:
            print(f"未知错误: {e}")
            logging.error(f"未知错误 (LCSC ID: {lcsc_id}): {e}")
            return {}

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
        try:
            r = self.session.get(
                url=ENDPOINT_3D_MODEL.format(uuid=uuid),
                headers={"User-Agent": self.headers["User-Agent"]},
                timeout=30
            )
            if r.status_code != requests.codes.ok:
                logging.error(f"No raw 3D model data found for uuid:{uuid} on easyeda, status code: {r.status_code}")
                return None
            return r.content.decode()
        except requests.exceptions.RequestException as e:
            logging.error(f"网络请求错误 (3D模型OBJ, UUID: {uuid}): {e}")
            # 尝试重试一次
            try:
                time.sleep(1)  # 等待1秒后重试
                r = self.session.get(
                    url=ENDPOINT_3D_MODEL.format(uuid=uuid),
                    headers={"User-Agent": self.headers["User-Agent"]},
                    timeout=30
                )
                if r.status_code != requests.codes.ok:
                    logging.error(f"重试后仍失败 - No raw 3D model data found for uuid:{uuid} on easyeda, status code: {r.status_code}")
                    return None
                return r.content.decode()
            except Exception as retry_error:
                logging.error(f"重试后仍失败 - 网络请求错误 (3D模型OBJ, UUID: {uuid}): {retry_error}")
                return None
        except Exception as e:
            logging.error(f"未知错误 (3D模型OBJ, UUID: {uuid}): {e}")
            return None

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
        try:
            r = self.session.get(
                url=ENDPOINT_3D_MODEL_STEP.format(uuid=uuid),
                headers={"User-Agent": self.headers["User-Agent"]},
                timeout=30
            )
            if r.status_code != requests.codes.ok:
                logging.error(f"No step 3D model data found for uuid:{uuid} on easyeda, status code: {r.status_code}")
                return None
            return r.content
        except requests.exceptions.RequestException as e:
            logging.error(f"网络请求错误 (3D模型STEP, UUID: {uuid}): {e}")
            # 尝试重试一次
            try:
                time.sleep(1)  # 等待1秒后重试
                r = self.session.get(
                    url=ENDPOINT_3D_MODEL_STEP.format(uuid=uuid),
                    headers={"User-Agent": self.headers["User-Agent"]},
                    timeout=30
                )
                if r.status_code != requests.codes.ok:
                    logging.error(f"重试后仍失败 - No step 3D model data found for uuid:{uuid} on easyeda, status code: {r.status_code}")
                    return None
                return r.content
            except Exception as retry_error:
                logging.error(f"重试后仍失败 - 网络请求错误 (3D模型STEP, UUID: {uuid}): {retry_error}")
                return None
        except Exception as e:
            logging.error(f"未知错误 (3D模型STEP, UUID: {uuid}): {e}")
            return None
