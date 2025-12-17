# Global imports
import logging
from math import acos, cos, isnan, pi, sin, sqrt
from typing import Tuple, Union

from ..easyeda.parameters_easyeda import ee_footprint
from .parameters_kicad_footprint import *

# 确保日志级别正确
logger = logging.getLogger(__name__)
if logger.level == 0:
    logger.setLevel(logging.INFO)

# ---------------------------------------


def to_radians(n: float) -> float:
    return (n / 180.0) * pi


def to_degrees(n: float) -> float:
    return (n / pi) * 180.0


# Elliptical arc implementation based on the SVG specification notes
# https://www.w3.org/TR/SVG11/implnote.html#ArcConversionEndpointToCenter


def compute_arc(
    start_x: float,
    start_y: float,
    radius_x: float,
    radius_y: float,
    angle: float,
    large_arc_flag: bool,
    sweep_flag: bool,
    end_x: float,
    end_y: float,
) -> Tuple[float, float, float]:
    # Compute the half distance between the current and the final point
    dx2 = (start_x - end_x) / 2.0
    dy2 = (start_y - end_y) / 2.0

    # Convert angle from degrees to radians
    angle = to_radians(angle % 360.0)
    cos_angle = cos(angle)
    sin_angle = sin(angle)

    # Step 1 : Compute (x1, y1)
    x1 = cos_angle * dx2 + sin_angle * dy2
    y1 = -sin_angle * dx2 + cos_angle * dy2

    # Ensure radii are large enough
    radius_x = abs(radius_x)
    radius_y = abs(radius_y)
    Pradius_x = radius_x * radius_x
    Pradius_y = radius_y * radius_y
    Px1 = x1 * x1
    Py1 = y1 * y1

    # check that radii are large enough

    radiiCheck = (
        Px1 / Pradius_x + Py1 / Pradius_y if Pradius_x != 0 and Pradius_y != 0 else 0
    )
    if radiiCheck > 1:
        radius_x = sqrt(radiiCheck) * radius_x
        radius_y = sqrt(radiiCheck) * radius_y
        Pradius_x = radius_x * radius_x
        Pradius_y = radius_y * radius_y

    # Step 2 : Compute (cx1, cy1)
    sign = -1 if large_arc_flag == sweep_flag else 1
    sq = 0
    if Pradius_x * Py1 + Pradius_y * Px1 > 0:
        sq = (Pradius_x * Pradius_y - Pradius_x * Py1 - Pradius_y * Px1) / (
            Pradius_x * Py1 + Pradius_y * Px1
        )
    sq = max(sq, 0)
    coef = sign * sqrt(sq)
    cx1 = coef * ((radius_x * y1) / radius_y) if radius_y != 0 else 0
    cy1 = coef * -((radius_y * x1) / radius_x) if radius_x != 0 else 0

    # Step 3 : Compute (cx, cy) from (cx1, cy1)
    sx2 = (start_x + end_x) / 2.0
    sy2 = (start_y + end_y) / 2.0
    # print(start_x, end_x)
    cx = sx2 + (cos_angle * cx1 - sin_angle * cy1)
    cy = sy2 + (sin_angle * cx1 + cos_angle * cy1)

    # Step 4 : Compute the angle_extent (dangle)
    ux = (x1 - cx1) / radius_x if radius_x != 0 else 0
    uy = (y1 - cy1) / radius_y if radius_y != 0 else 0
    vx = (-x1 - cx1) / radius_x if radius_x != 0 else 0
    vy = (-y1 - cy1) / radius_y if radius_y != 0 else 0

    # Compute the angle extent
    n = sqrt((ux * ux + uy * uy) * (vx * vx + vy * vy))
    p = ux * vx + uy * vy
    sign = -1 if (ux * vy - uy * vx) < 0 else 1
    if n != 0:
        # Clamp p/n to [-1, 1] to handle floating point precision errors
        cosine_value = max(-1.0, min(1.0, p / n))
        angle_extent = to_degrees(sign * acos(cosine_value))
    else:
        angle_extent = 360 + 359
    if not (sweep_flag) and angle_extent > 0:
        angle_extent -= 360
    elif sweep_flag and angle_extent < 0:
        angle_extent += 360

    angleExtent_sign = 1 if angle_extent < 0 else -1
    angle_extent = (abs(angle_extent) % 360) * angleExtent_sign

    return cx, cy, angle_extent


# ---------------------------------------


def fp_to_ki(dim) -> float:
    # Handle both string and numeric inputs
    if dim in ["", None]:
        return 0.0
    
    try:
        # Convert to float if it's a string
        if isinstance(dim, str):
            dim_float = float(dim)
        else:
            dim_float = float(dim)
        
        # Check for NaN
        if isnan(dim_float):
            return 0.0
            
        return round(dim_float * 10 * 0.0254, 2)
    except (ValueError, TypeError):
        # If conversion fails, return 0.0 as fallback
        return 0.0


# ---------------------------------------


def drill_to_ki(
    hole_radius: float, hole_length: float, pad_height: float, pad_width: float
) -> str:
    if (
        hole_radius > 0
        and hole_length != ""
        and hole_length is not None
        and hole_length != 0
    ):
        max_distance_hole = max(hole_radius * 2, hole_length)
        pos_0 = pad_height - max_distance_hole
        pos_90 = pad_width - max_distance_hole
        max_distance = max(pos_0, pos_90)

        if max_distance == pos_0:
            return f"(drill oval {hole_radius*2} {hole_length})"
        else:
            return f"(drill oval {hole_length} {hole_radius*2})"
    if hole_radius > 0:
        return f"(drill {2 * hole_radius})"
    return ""


# ---------------------------------------


def angle_to_ki(rotation: float) -> Union[float, str]:
    if isnan(rotation) is False:
        return -(360 - rotation) if rotation > 180 else rotation
    return ""


# ---------------------------------------


def rotate(x: float, y: float, degrees: float) -> Tuple[float, float]:
    radians = (degrees / 180) * 2 * pi
    new_x = x * cos(radians) - y * sin(radians)
    new_y = x * sin(radians) + y * cos(radians)
    return new_x, new_y


# ---------------------------------------


class ExporterFootprintKicad:
    def __init__(self, footprint: ee_footprint):
        self.input = footprint
        if not isinstance(self.input, ee_footprint):
            logging.error("Unsupported conversion")
        else:
            self.generate_kicad_footprint()

    def generate_kicad_footprint(self) -> None:
        # Convert dimension from easyeda to kicad
        self.input.bbox.convert_to_mm()

        for fields in (
            self.input.pads,
            self.input.tracks,
            self.input.holes,
            self.input.vias,
            self.input.circles,
            self.input.rectangles,
            self.input.texts,
        ):
            for field in fields:
                field.convert_to_mm()

        ki_info = KiFootprintInfo(
            name=self.input.info.name, fp_type=self.input.info.fp_type
        )

        if self.input.model_3d is not None:
            # 记录转换前的原始值
            logging.info("=" * 60)
            logging.info(f"3D模型位置计算")
            logging.info("=" * 60)
            logging.info(f"模型名称: {self.input.model_3d.name}")
            logging.info(f"🆔 模型UUID: {self.input.model_3d.uuid}")
            logging.info("")
            logging.info(f"原始数据 (EasyEDA单位，转换前):")
            logging.info(f"   Translation:")
            logging.info(f"     - X: {self.input.model_3d.translation.x:.4f}")
            logging.info(f"     - Y: {self.input.model_3d.translation.y:.4f}")
            logging.info(f"     - Z: {self.input.model_3d.translation.z:.4f}")
            logging.info(f"   Rotation:")
            logging.info(f"     - X: {self.input.model_3d.rotation.x:.2f}°")
            logging.info(f"     - Y: {self.input.model_3d.rotation.y:.2f}°")
            logging.info(f"     - Z: {self.input.model_3d.rotation.z:.2f}°")
            logging.info(f"   BBox (封装边界):")
            logging.info(f"     - X: {self.input.bbox.x:.4f}")
            logging.info(f"     - Y: {self.input.bbox.y:.4f}")
            logging.info("")
            
            # 单位转换
            self.input.model_3d.convert_to_mm()
            
            logging.info(f"单位转换后 (毫米 mm):")
            logging.info(f"   Translation:")
            logging.info(f"     - X: {self.input.model_3d.translation.x:.4f} mm")
            logging.info(f"     - Y: {self.input.model_3d.translation.y:.4f} mm")
            logging.info(f"     - Z: {self.input.model_3d.translation.z:.4f} mm")
            logging.info(f"   Rotation (不变):")
            logging.info(f"     - X: {self.input.model_3d.rotation.x:.2f}°")
            logging.info(f"     - Y: {self.input.model_3d.rotation.y:.2f}°")
            logging.info(f"     - Z: {self.input.model_3d.rotation.z:.2f}°")
            logging.info("")

            # 3D模型偏移计算策略：
            # 
            # 问题分析：
            # 1. EasyEDA的bbox数据有时不可靠（可能是画布坐标而非封装坐标）
            # 2. 当bbox值异常大（如1000mm）时，计算出的偏移也会异常
            # 3. 实际上，3D模型文件本身已经包含了正确的位置信息
            # 4. 用户反馈：在KiCad中将偏移设置为0就能正常显示
            #
            # 解决方案：
            # - 检查bbox是否可靠（是否在合理范围内）
            # - 如果bbox不可靠，直接使用0偏移
            # - 如果bbox可靠，进行计算但仍需边界检查
            
            # 安全获取bbox值
            bbox_x = self.input.bbox.x if self.input.bbox.x is not None and not isnan(self.input.bbox.x) else 0.0
            bbox_y = self.input.bbox.y if self.input.bbox.y is not None and not isnan(self.input.bbox.y) else 0.0
            
            logging.info(f"BBox (转换后):")
            logging.info(f"     - X: {bbox_x:.4f} mm")
            logging.info(f"     - Y: {bbox_y:.4f} mm")
            logging.info("")
            
            # 获取Z轴值（Z轴不受bbox影响，始终使用原始值）
            trans_z = self.input.model_3d.translation.z if not isnan(self.input.model_3d.translation.z) else 0.0
            
            # 检查bbox是否可靠
            # 合理的封装位置应该在 ±500mm 以内（大多数PCB不会超过500mm）
            MAX_REASONABLE_BBOX = 500.0
            bbox_is_reliable = (abs(bbox_x) <= MAX_REASONABLE_BBOX and abs(bbox_y) <= MAX_REASONABLE_BBOX)
            
            logging.info(f"BBox可靠性检查:")
            logging.info(f"   - 阈值: ±{MAX_REASONABLE_BBOX} mm")
            logging.info(f"   - BBox X: {bbox_x:.2f} mm {'✓ 可靠' if abs(bbox_x) <= MAX_REASONABLE_BBOX else '✗ 超出范围'}")
            logging.info(f"   - BBox Y: {bbox_y:.2f} mm {'✓ 可靠' if abs(bbox_y) <= MAX_REASONABLE_BBOX else '✗ 超出范围'}")
            logging.info(f"   - 结论: {'✓ BBox数据可靠' if bbox_is_reliable else '✗ BBox数据不可靠'}")
            logging.info("")
            
            if not bbox_is_reliable:
                # bbox数据不可靠，XY使用0偏移，Z轴保留原始值
                logging.info(f"偏移计算策略 (BBox不可靠):")
                logging.info(f"   - X偏移: 0.0 mm (使用零偏移)")
                logging.info(f"   - Y偏移: 0.0 mm (使用零偏移)")
                logging.info(f"   - Z偏移: {trans_z:.4f} mm (保留EasyEDA原始值)")
                translation_x = 0.0
                translation_y = 0.0
                translation_z = trans_z  # Z轴保留原始值
            else:
                # bbox数据可靠，进行正常计算
                trans_x = self.input.model_3d.translation.x if not isnan(self.input.model_3d.translation.x) else 0.0
                trans_y = self.input.model_3d.translation.y if not isnan(self.input.model_3d.translation.y) else 0.0
                
                # 计算相对偏移（Z轴不需要减去bbox，因为bbox只包含XY）
                translation_x = trans_x - bbox_x
                translation_y = trans_y - bbox_y
                translation_z = trans_z  # Z轴直接使用原始值
                
                logging.info(f"偏移计算 (BBox可靠):")
                logging.info(f"   X偏移计算:")
                logging.info(f"     {trans_x:.4f} (translation.x) - {bbox_x:.4f} (bbox.x) = {translation_x:.4f} mm")
                logging.info(f"   Y偏移计算:")
                logging.info(f"     {trans_y:.4f} (translation.y) - {bbox_y:.4f} (bbox.y) = {translation_y:.4f} mm")
                logging.info(f"   Z偏移:")
                logging.info(f"     {trans_z:.4f} mm (直接使用translation.z，不减去bbox)")
                logging.info("")
                
                # 边界检查：即使bbox可靠，计算结果也可能异常
                MAX_REASONABLE_OFFSET = 100.0
                
                needs_correction = False
                if abs(translation_x) > MAX_REASONABLE_OFFSET:
                    logging.warning(f"offset_x ({translation_x:.2f}mm) 超出合理范围 (±{MAX_REASONABLE_OFFSET}mm)")
                    translation_x = 0.0
                    needs_correction = True
                    
                if abs(translation_y) > MAX_REASONABLE_OFFSET:
                    logging.warning(f"offset_y ({translation_y:.2f}mm) 超出合理范围 (±{MAX_REASONABLE_OFFSET}mm)")
                    translation_y = 0.0
                    needs_correction = True
                    
                if abs(translation_z) > MAX_REASONABLE_OFFSET:
                    logging.warning(f"offset_z ({translation_z:.2f}mm) 超出合理范围 (±{MAX_REASONABLE_OFFSET}mm)")
                    translation_z = 0.0
                    needs_correction = True
                
                if needs_correction:
                    logging.info(f"   ✓ 已修正为零偏移")

            # 坐标系转换（Y轴和Z轴需要反转）
            final_x = round(translation_x, 2)
            final_y = -round(translation_y, 2)  # Y轴反转
            final_z = -round(translation_z, 2) if self.input.info.fp_type == "smd" else 0  # SMD元件Z轴反转
            
            final_rot_x = (360 - self.input.model_3d.rotation.x) % 360
            final_rot_y = (360 - self.input.model_3d.rotation.y) % 360
            final_rot_z = (360 - self.input.model_3d.rotation.z) % 360
            
            ki_3d_model_info = Ki3dModel(
                name=self.input.model_3d.name,
                translation=Ki3dModelBase(
                    x=final_x,
                    y=final_y,
                    z=final_z,
                ),
                rotation=Ki3dModelBase(
                    x=final_rot_x,
                    y=final_rot_y,
                    z=final_rot_z,
                ),
                raw_wrl=None,
            )
            
            logging.info(f"最终输出 (KiCad格式):")
            logging.info(f"   封装类型: {self.input.info.fp_type.upper()}")
            logging.info("")
            logging.info(f"   Offset (偏移):")
            logging.info(f"     - X: {translation_x:.4f} → {final_x:.2f} mm")
            logging.info(f"     - Y: {translation_y:.4f} → {final_y:.2f} mm (Y轴反转)")
            logging.info(f"     - Z: {translation_z:.4f} → {final_z:.2f} mm {'(SMD反转)' if self.input.info.fp_type == 'smd' else '(THT保持)'}")
            logging.info("")
            logging.info(f"   Rotation (旋转):")
            logging.info(f"     - X: {self.input.model_3d.rotation.x:.2f}° → {final_rot_x:.2f}°")
            logging.info(f"     - Y: {self.input.model_3d.rotation.y:.2f}° → {final_rot_y:.2f}°")
            logging.info(f"     - Z: {self.input.model_3d.rotation.z:.2f}° → {final_rot_z:.2f}°")
            logging.info("")
            logging.info(f"   KiCad文件中的值:")
            logging.info(f"     (offset (xyz {final_x} {final_y} {final_z}))")
            logging.info(f"     (rotate (xyz {final_rot_x} {final_rot_y} {final_rot_z}))")
            logging.info("=" * 60)
        else:
            ki_3d_model_info = None

        self.output = KiFootprint(info=ki_info, model_3d=ki_3d_model_info)

        # For pads
        for ee_pad in self.input.pads:
            ki_pad = KiFootprintPad(
                type="thru_hole" if ee_pad.hole_radius > 0 else "smd",
                shape=KI_PAD_SHAPE[ee_pad.shape]
                if ee_pad.shape in KI_PAD_SHAPE
                else "custom",
                pos_x=ee_pad.center_x - self.input.bbox.x,
                pos_y=ee_pad.center_y - self.input.bbox.y,
                width=max(ee_pad.width, 0.01),
                height=max(ee_pad.height, 0.01),
                layers=(
                    KI_PAD_LAYER if ee_pad.hole_radius <= 0 else KI_PAD_LAYER_THT
                ).get(ee_pad.layer_id, ""),
                number=ee_pad.number,
                drill=0.0,
                orientation=angle_to_ki(ee_pad.rotation),
                polygon="",
            )

            ki_pad.drill = drill_to_ki(
                ee_pad.hole_radius, ee_pad.hole_length, ki_pad.height, ki_pad.width
            )
            if "(" in ki_pad.number and ")" in ki_pad.number:
                ki_pad.number = ki_pad.number.split("(")[1].split(")")[0]

            # For custom polygon
            is_custom_shape = ki_pad.shape == "custom"
            point_list = [fp_to_ki(point) for point in ee_pad.points.split(" ")]
            if is_custom_shape:
                if len(point_list) <= 0:
                    logging.warning(
                        f"PAD ${ee_pad.id} is a polygon, but has no points defined"
                    )
                else:
                    # Set the pad width and height to the smallest value allowed by KiCad.
                    # KiCad tries to draw a pad that forms the base of the polygon,
                    # but this is often unnecessary and should be disabled.
                    ki_pad.width = 0.005
                    ki_pad.height = 0.005

                    # The points of the polygon always seem to correspond to coordinates when orientation=0.
                    ki_pad.orientation = 0

                    # Generate polygon with coordinates relative to the base pad's position.
                    path = "".join(
                        "(xy {} {})".format(
                            round(point_list[i] - self.input.bbox.x - ki_pad.pos_x, 2),
                            round(
                                point_list[i + 1] - self.input.bbox.y - ki_pad.pos_y, 2
                            ),
                        )
                        for i in range(0, len(point_list), 2)
                    )
                    ki_pad.polygon = (
                        "\n\t\t(primitives \n\t\t\t(gr_poly \n\t\t\t\t(pts"
                        f" {path}\n\t\t\t\t) \n\t\t\t\t(width 0.1) \n\t\t\t)\n\t\t)\n\t"
                    )

            self.output.pads.append(ki_pad)

        # For tracks
        for ee_track in self.input.tracks:
            ki_track = KiFootprintTrack(
                layers=KI_PAD_LAYER[ee_track.layer_id]
                if ee_track.layer_id in KI_PAD_LAYER
                else "F.Fab",
                stroke_width=max(ee_track.stroke_width, 0.01),
            )

            # Generate line
            point_list = [fp_to_ki(point) for point in ee_track.points.split(" ") if point.strip()]
            # Ensure we have at least 4 points (2 coordinate pairs) to form a line
            if len(point_list) >= 4:
                for i in range(0, len(point_list) - 3, 2):
                    ki_track.points_start_x.append(
                        round(point_list[i] - self.input.bbox.x, 2)
                    )
                    ki_track.points_start_y.append(
                        round(point_list[i + 1] - self.input.bbox.y, 2)
                    )
                    ki_track.points_end_x.append(
                        round(point_list[i + 2] - self.input.bbox.x, 2)
                    )
                    ki_track.points_end_y.append(
                        round(point_list[i + 3] - self.input.bbox.y, 2)
                    )
            else:
                logging.warning(f"Track has insufficient points: {len(point_list)} points, need at least 4")

            self.output.tracks.append(ki_track)

        # For holes
        for ee_hole in self.input.holes:
            ki_hole = KiFootprintHole(
                pos_x=ee_hole.center_x - self.input.bbox.x,
                pos_y=ee_hole.center_y - self.input.bbox.y,
                size=ee_hole.radius * 2,
            )

            self.output.holes.append(ki_hole)

        # For Vias
        for ee_via in self.input.vias:
            ki_via = KiFootprintVia(
                pos_x=ee_via.center_x - self.input.bbox.x,
                pos_y=ee_via.center_y - self.input.bbox.y,
                size=ee_via.radius * 2,
                diameter=ee_via.diameter,
            )

            self.output.vias.append(ki_via)

        # For circles
        for ee_circle in self.input.circles:
            ki_circle = KiFootprintCircle(
                cx=ee_circle.cx - self.input.bbox.x,
                cy=ee_circle.cy - self.input.bbox.y,
                end_x=0.0,
                end_y=0.0,
                layers=KI_LAYERS[ee_circle.layer_id]
                if ee_circle.layer_id in KI_LAYERS
                else "F.Fab",
                stroke_width=max(ee_circle.stroke_width, 0.01),
            )
            ki_circle.end_x = ki_circle.cx + ee_circle.radius
            ki_circle.end_y = ki_circle.cy
            self.output.circles.append(ki_circle)

        # For rectangles
        for ee_rectangle in self.input.rectangles:
            ki_rectangle = KiFootprintRectangle(
                layers=KI_PAD_LAYER[ee_rectangle.layer_id]
                if ee_rectangle.layer_id in KI_PAD_LAYER
                else "F.Fab",
                stroke_width=max(ee_rectangle.stroke_width, 0.01),
            )

            start_x = ee_rectangle.x - self.input.bbox.x
            start_y = ee_rectangle.y - self.input.bbox.y
            width = ee_rectangle.width
            height = ee_rectangle.height

            ki_rectangle.points_start_x = [
                start_x,
                start_x + width,
                start_x + width,
                start_x,
            ]
            ki_rectangle.points_start_y = [start_y, start_y, start_y + height, start_y]
            ki_rectangle.points_end_x = [
                start_x + width,
                start_x + width,
                start_x,
                start_x,
            ]
            ki_rectangle.points_end_y = [
                start_y,
                start_y + height,
                start_y + height,
                start_y,
            ]

            self.output.rectangles.append(ki_rectangle)

        # For arcs
        for ee_arc in self.input.arcs:
            arc_path = (
                ee_arc.path.replace(",", " ").replace("M ", "M").replace("A ", "A")
            )

            start_x, start_y = arc_path.split("A")[0][1:].split(" ", 1)
            start_x = fp_to_ki(start_x) - self.input.bbox.x
            start_y = fp_to_ki(start_y) - self.input.bbox.y

            arc_parameters = arc_path.split("A")[1].replace("  ", " ")
            (
                svg_rx,
                svg_ry,
                x_axis_rotation,
                large_arc,
                sweep,
                end_x,
                end_y,
            ) = arc_parameters.split(" ", 6)
            rx, ry = rotate(fp_to_ki(svg_rx), fp_to_ki(svg_ry), 0)

            end_x = fp_to_ki(end_x) - self.input.bbox.x
            end_y = fp_to_ki(end_y) - self.input.bbox.y
            if ry != 0:
                cx, cy, extent = compute_arc(
                    start_x,
                    start_y,
                    rx,
                    ry,
                    float(x_axis_rotation),
                    large_arc == "1",
                    sweep == "1",
                    end_x,
                    end_y,
                )
            else:
                cx = 0.0
                cy = 0.0
                extent = 0.0

            ki_arc = KiFootprintArc(
                start_x=cx,
                start_y=cy,
                end_x=end_x,
                end_y=end_y,
                angle=extent,
                layers=KI_LAYERS[ee_arc.layer_id]
                if ee_arc.layer_id in KI_LAYERS
                else "F.Fab",
                stroke_width=max(fp_to_ki(ee_arc.stroke_width), 0.01),
            )
            self.output.arcs.append(ki_arc)

        # For texts
        for ee_text in self.input.texts:
            ki_text = KiFootprintText(
                pos_x=ee_text.center_x - self.input.bbox.x,
                pos_y=ee_text.center_y - self.input.bbox.y,
                orientation=angle_to_ki(ee_text.rotation),
                text=ee_text.text,
                layers=KI_LAYERS[ee_text.layer_id]
                if ee_text.layer_id in KI_LAYERS
                else "F.Fab",
                font_size=max(ee_text.font_size, 1),
                thickness=max(ee_text.stroke_width, 0.01),
                display=" hide" if ee_text.is_displayed is False else "",
                mirror="",
            )
            ki_text.layers = (
                ki_text.layers.replace(".SilkS", ".Fab")
                if ee_text.type == "N"
                else ki_text.layers
            )
            ki_text.mirror = " mirror" if ki_text.layers[0] == "B" else ""
            self.output.texts.append(ki_text)

    def get_ki_footprint(self) -> KiFootprint:
        return self.output

    def export(self, footprint_full_path: str, model_3d_path: str) -> None:
        ki = self.output
        ki_lib = ""

        ki_lib += KI_MODULE_INFO.format(
            package_lib="easyeda2kicad", package_name=ki.info.name, edit="5DC5F6A4"
        )

        if ki.info.fp_type:
            ki_lib += KI_FP_TYPE.format(
                component_type=("smd" if ki.info.fp_type == "smd" else "through_hole")
            )

        # Get y_min and y_max to put component info
        y_low = min(pad.pos_y for pad in ki.pads)
        y_high = max(pad.pos_y for pad in ki.pads)

        ki_lib += KI_REFERENCE.format(pos_x="0", pos_y=y_low - 4)

        ki_lib += KI_PACKAGE_VALUE.format(
            package_name=ki.info.name, pos_x="0", pos_y=y_high + 4
        )
        ki_lib += KI_FAB_REF

        # ---------------------------------------

        for track in ki.tracks + ki.rectangles:
            for i in range(len(track.points_start_x)):
                ki_lib += KI_LINE.format(
                    start_x=track.points_start_x[i],
                    start_y=track.points_start_y[i],
                    end_x=track.points_end_x[i],
                    end_y=track.points_end_y[i],
                    layers=track.layers,
                    stroke_width=track.stroke_width,
                )

        for pad in ki.pads:
            ki_lib += KI_PAD.format(**vars(pad))

        for hole in ki.holes:
            ki_lib += KI_HOLE.format(**vars(hole))

        for via in ki.vias:
            ki_lib += KI_VIA.format(**vars(via))

        for circle in ki.circles:
            ki_lib += KI_CIRCLE.format(**vars(circle))

        for arc in ki.arcs:
            ki_lib += KI_ARC.format(**vars(arc))

        for text in ki.texts:
            ki_lib += KI_TEXT.format(**vars(text))

        if ki.model_3d is not None:
            # 构建3D模型路径：用户导出路径 + 库名.3dshapes/模型名.wrl
            # Build 3D model path: user export path + lib_name.3dshapes/model_name.wrl
            # 使用正斜杠以确保在Windows和Linux上都能正确显示
            import os
            model_3d_path_normalized = model_3d_path.replace(os.sep, "/")
            model_file_path = f"{model_3d_path_normalized}.3dshapes/{ki.model_3d.name}.wrl"
            ki_lib += KI_MODEL_3D.format(
                file_3d=model_file_path,
                pos_x=ki.model_3d.translation.x,
                pos_y=ki.model_3d.translation.y,
                pos_z=ki.model_3d.translation.z,
                rot_x=ki.model_3d.rotation.x,
                rot_y=ki.model_3d.rotation.y,
                rot_z=ki.model_3d.rotation.z,
            )

        ki_lib += KI_END_FILE

        with open(
            file=footprint_full_path,
            mode="w",
            encoding="utf-8",
        ) as my_lib:
            my_lib.write(ki_lib)
