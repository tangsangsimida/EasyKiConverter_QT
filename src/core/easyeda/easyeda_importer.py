import json
import logging

from .easyeda_api import EasyedaApi
from .parameters_easyeda import *


def add_easyeda_pin(pin_data: str, ee_symbol: EeSymbol):
    segments = pin_data.split("^^")
    ee_segments = [seg.split("~") for seg in segments]

    pin_settings = EeSymbolPinSettings(
        **dict(zip(EeSymbolPinSettings.model_fields.keys(), ee_segments[0][1:]))
    )
    pin_dot = EeSymbolPinDot(
        dot_x=float(ee_segments[1][0]), dot_y=float(ee_segments[1][1])
    )
    pin_path = EeSymbolPinPath(path=ee_segments[2][0], color=ee_segments[2][1])
    pin_name = EeSymbolPinName(
        **dict(zip(EeSymbolPinName.model_fields.keys(), ee_segments[3][:]))
    )

    pin_dot_bis = EeSymbolPinDotBis(
        is_displayed=ee_segments[5][0],
        circle_x=float(ee_segments[5][1]),
        circle_y=float(ee_segments[5][2]),
    )
    pin_clock = EeSymbolPinClock(is_displayed=ee_segments[6][0], path=ee_segments[6][1])

    ee_symbol.pins.append(
        EeSymbolPin(
            settings=pin_settings,
            pin_dot=pin_dot,
            pin_path=pin_path,
            name=pin_name,
            dot=pin_dot_bis,
            clock=pin_clock,
        )
    )


def add_easyeda_rectangle(rectangle_data: str, ee_symbol: EeSymbol):
    ee_symbol.rectangles.append(
        EeSymbolRectangle(
            **dict(zip(EeSymbolRectangle.model_fields.keys(), rectangle_data.split("~")[1:]))
        )
    )


def add_easyeda_polyline(polyline_data: str, ee_symbol: EeSymbol):
    ee_symbol.polylines.append(
        EeSymbolPolyline(
            **dict(zip(EeSymbolPolyline.model_fields.keys(), polyline_data.split("~")[1:]))
        )
    )


def add_easyeda_polygon(polygon_data: str, ee_symbol: EeSymbol):
    ee_symbol.polygons.append(
        EeSymbolPolygon(
            **dict(zip(EeSymbolPolygon.model_fields.keys(), polygon_data.split("~")[1:]))
        )
    )


def add_easyeda_path(path_data: str, ee_symbol: EeSymbol):
    ee_symbol.paths.append(
        EeSymbolPath(**dict(zip(EeSymbolPath.model_fields.keys(), path_data.split("~")[1:])))
    )


def add_easyeda_circle(circle_data: str, ee_symbol: EeSymbol):
    ee_symbol.circles.append(
        EeSymbolCircle(
            **dict(zip(EeSymbolCircle.model_fields.keys(), circle_data.split("~")[1:]))
        )
    )


def add_easyeda_text(text_data: str, ee_symbol: EeSymbol):
    # 文本元素的处理逻辑
    # 目前只是简单记录，避免警告
    logging.debug(f"Skipping text element: {text_data}")


def add_easyeda_ellipse(ellipse_data: str, ee_symbol: EeSymbol):
    """处理椭圆元素
    
    Args:
        ellipse_data: 椭圆数据字符串，格式为 "E~参数1~参数2~..."
        ee_symbol: EasyEDA符号对象
    """
    ee_symbol.ellipses.append(
        EeSymbolEllipse(
            **dict(zip(EeSymbolEllipse.model_fields.keys(), ellipse_data.split("~")[1:]))
        )
    )


def add_easyeda_arc(arc_data: str, ee_symbol: EeSymbol):
    """处理弧线元素
    
    Args:
        arc_data: 弧线数据字符串，格式为 "A~参数1~参数2~..."
        ee_symbol: EasyEDA符号对象
    """
    ee_symbol.arcs.append(
        EeSymbolArc(**dict(zip(EeSymbolArc.model_fields.keys(), arc_data.split("~")[1:])))
    )


easyeda_handlers = {
    # P: 处理引脚元素
    "P": add_easyeda_pin,
    # R: 处理矩形元素
    "R": add_easyeda_rectangle,
    # E: 处理椭圆元素
    "E": add_easyeda_ellipse,
    # C: 处理圆形元素
    "C": add_easyeda_circle,
    # A: 处理弧线元素
    "A": add_easyeda_arc,
    # PL: 处理折线元素
    "PL": add_easyeda_polyline,
    # PG: 处理多边形元素
    "PG": add_easyeda_polygon,
    # PT: 处理路径元素
    "PT": add_easyeda_path,
    # T: 处理文本元素
    "T": add_easyeda_text,
    # "PI" : 饼图/扇形椭圆弧在KiCad中不支持
}


class EasyedaSymbolImporter:
    def __init__(self, easyeda_cp_cad_data: dict):
        self.input = easyeda_cp_cad_data
        self.output: EeSymbol = self.extract_easyeda_data(
            ee_data=easyeda_cp_cad_data,
            ee_data_info=easyeda_cp_cad_data["dataStr"]["head"]["c_para"],
        )

    def get_symbol(self) -> EeSymbol:
        return self.output

    def extract_easyeda_data(self, ee_data: dict, ee_data_info: dict) -> EeSymbol:
        new_ee_symbol = EeSymbol(
            info=EeSymbolInfo(
                name=ee_data_info["name"],
                prefix=ee_data_info["pre"],
                package=ee_data_info.get("package", None),
                manufacturer=ee_data_info.get("BOM_Manufacturer", None),
                datasheet=ee_data["lcsc"].get("url", None),
                lcsc_id=ee_data["lcsc"].get("number", None),
                jlc_id=ee_data_info.get("BOM_JLCPCB Part Class", None),
            ),
            bbox=EeSymbolBbox(
                x=float(ee_data["dataStr"]["head"]["x"]),
                y=float(ee_data["dataStr"]["head"]["y"]),
            ),
        )

        for line in ee_data["dataStr"]["shape"]:
            designator = line.split("~")[0]
            if designator in easyeda_handlers:
                easyeda_handlers[designator](line, new_ee_symbol)
            else:
                logging.warning(f"Unknow symbol designator : {designator}")

        return new_ee_symbol


class EasyedaFootprintImporter:
    def __init__(self, easyeda_cp_cad_data: dict):
        self.input = easyeda_cp_cad_data
        self.output = self.extract_easyeda_data(
            ee_data_str=self.input["packageDetail"]["dataStr"],
            ee_data_info=self.input["packageDetail"]["dataStr"]["head"]["c_para"],
            is_smd=self.input.get("SMT")
            and "-TH_" not in self.input["packageDetail"]["title"],
        )

    def get_footprint(self):
        return self.output

    def extract_easyeda_data(
        self, ee_data_str: dict, ee_data_info: dict, is_smd: bool
    ) -> ee_footprint:
        new_ee_footprint = ee_footprint(
            info=EeFootprintInfo(
                name=ee_data_info["package"],
                fp_type="smd" if is_smd else "tht",
                model_3d_name=ee_data_info.get("3DModel"),
            ),
            bbox=EeFootprintBbox(
                x=float(ee_data_str["head"]["x"]),
                y=float(ee_data_str["head"]["y"]),
            ),
            model_3d=None,
        )

        for line in ee_data_str["shape"]:
            ee_designator = line.split("~")[0]
            ee_fields = line.split("~")[1:]

            if ee_designator == "PAD":
                ee_pad = EeFootprintPad(
                    **dict(zip(EeFootprintPad.model_fields.keys(), ee_fields[:18]))
                )
                new_ee_footprint.pads.append(ee_pad)
            elif ee_designator == "TRACK":
                ee_track = EeFootprintTrack(
                    **dict(zip(EeFootprintTrack.model_fields.keys(), ee_fields))
                )
                new_ee_footprint.tracks.append(ee_track)
            elif ee_designator == "HOLE":
                ee_hole = EeFootprintHole(
                    **dict(zip(EeFootprintHole.model_fields.keys(), ee_fields))
                )
                new_ee_footprint.holes.append(ee_hole)
            elif ee_designator == "VIA":
                ee_via = EeFootprintVia(
                    **dict(zip(EeFootprintVia.model_fields.keys(), ee_fields))
                )
                new_ee_footprint.vias.append(ee_via)
            elif ee_designator == "CIRCLE":
                ee_circle = EeFootprintCircle(
                    **dict(zip(EeFootprintCircle.model_fields.keys(), ee_fields))
                )
                new_ee_footprint.circles.append(ee_circle)
            elif ee_designator == "ARC":
                ee_arc = EeFootprintArc(
                    **dict(zip(EeFootprintArc.model_fields.keys(), ee_fields))
                )
                new_ee_footprint.arcs.append(ee_arc)
            elif ee_designator == "RECT":
                ee_rectangle = EeFootprintRectangle(
                    **dict(zip(EeFootprintRectangle.model_fields.keys(), ee_fields))
                )
                new_ee_footprint.rectangles.append(ee_rectangle)
            elif ee_designator == "TEXT":
                ee_text = EeFootprintText(
                    **dict(zip(EeFootprintText.model_fields.keys(), ee_fields))
                )
                new_ee_footprint.texts.append(ee_text)
            elif ee_designator == "SVGNODE":
                new_ee_footprint.model_3d = Easyeda3dModelImporter(
                    easyeda_cp_cad_data=[line], download_raw_3d_model=False
                ).output

            elif ee_designator == "SOLIDREGION":
                ...
            else:
                logging.warning(f"Unknow footprint designator : {ee_designator}")

        return new_ee_footprint


# ------------------------------------------------------------------------------


class Easyeda3dModelImporter:
    def __init__(self, easyeda_cp_cad_data, download_raw_3d_model: bool):
        self.input = easyeda_cp_cad_data
        self.download_raw_3d_model = download_raw_3d_model
        self.output = self.create_3d_model()

    def create_3d_model(self) -> Union[Ee3dModel, None]:
        """Create 3D model with enhanced error handling and logging"""
        try:
            ee_data = (
                self.input["packageDetail"]["dataStr"]["shape"]
                if isinstance(self.input, dict)
                else self.input
            )

            if model_3d_info := self.get_3d_model_info(ee_data=ee_data):
                logging.info(f"Found 3D model info: {model_3d_info.get('title', 'Unknown')}")
                model_3d: Ee3dModel = self.parse_3d_model_info(info=model_3d_info)
                
                if self.download_raw_3d_model:
                    logging.info(f"Downloading 3D model data for UUID: {model_3d.uuid}")
                    
                    # 创建API实例用于下载
                    api = EasyedaApi()
                    
                    # Download OBJ format with retry
                    raw_obj = None
                    for attempt in range(3):  # 最多尝试3次
                        raw_obj = api.get_raw_3d_model_obj(uuid=model_3d.uuid)
                        if raw_obj:
                            model_3d.raw_obj = raw_obj
                            logging.info(f"Successfully downloaded OBJ 3D model")
                            break
                        else:
                            logging.warning(f"Failed to download OBJ 3D model for UUID: {model_3d.uuid}, attempt {attempt + 1}/3")
                            if attempt < 2:  # 不是最后一次尝试，等待后重试
                                import time
                                time.sleep(2 ** attempt)  # 指数退避
                    
                    if not raw_obj:
                        logging.warning(f"最终失败 - Failed to download OBJ 3D model for UUID: {model_3d.uuid} after 3 attempts")
                    
                    # Download STEP format with retry
                    step_data = None
                    for attempt in range(3):  # 最多尝试3次
                        step_data = api.get_step_3d_model(uuid=model_3d.uuid)
                        if step_data:
                            model_3d.step = step_data
                            logging.info(f"Successfully downloaded STEP 3D model")
                            break
                        else:
                            logging.warning(f"Failed to download STEP 3D model for UUID: {model_3d.uuid}, attempt {attempt + 1}/3")
                            if attempt < 2:  # 不是最后一次尝试，等待后重试
                                import time
                                time.sleep(2 ** attempt)  # 指数退避
                    
                    if not step_data:
                        logging.warning(f"最终失败 - Failed to download STEP 3D model for UUID: {model_3d.uuid} after 3 attempts")
                
                return model_3d
            else:
                logging.warning("No 3D model available for this component")
                return None
                
        except Exception as e:
            logging.error(f"Error creating 3D model: {e}")
            return None

    def get_3d_model_info(self, ee_data: str) -> dict:
        for line in ee_data:
            ee_designator = line.split("~")[0]
            if ee_designator == "SVGNODE":
                raw_json = line.split("~")[1:][0]
                return json.loads(raw_json)["attrs"]
        return {}

    def parse_3d_model_info(self, info: dict) -> Ee3dModel:
        return Ee3dModel(
            name=info["title"],
            uuid=info["uuid"],
            translation=Ee3dModelBase(
                x=info["c_origin"].split(",")[0],
                y=info["c_origin"].split(",")[1],
                z=info["z"],
            ),
            rotation=Ee3dModelBase(
                **dict(zip(Ee3dModelBase.model_fields.keys(), info["c_rotation"].split(",")))
            ),
        )
