"""
几何计算工具模块
包含所有几何计算相关函数
"""
import math


def get_middle_arc_pos(
    center_x: float,
    center_y: float,
    radius: float,
    angle_start: float,
    angle_end: float,
):
    """
    计算圆弧中间点坐标
    Calculate middle point coordinates of an arc
    """
    middle_x = center_x + radius * math.cos((angle_start + angle_end) / 2)
    middle_y = center_y + radius * math.sin((angle_start + angle_end) / 2)
    return middle_x, middle_y


def get_arc_center(start_x, start_y, end_x, end_y, rotation_direction, radius):
    """
    计算圆弧中心点坐标
    Calculate center point coordinates of an arc
    """
    arc_distance = math.sqrt(
        (end_x - start_x) * (end_x - start_x) + (end_y - start_y) * (end_y - start_y)
    )

    m_x = (start_x + end_x) / 2
    m_y = (start_y + end_y) / 2
    u = (end_x - start_x) / arc_distance
    v = (end_y - start_y) / arc_distance
    h = math.sqrt(radius * radius - (arc_distance * arc_distance) / 4)

    center_x = m_x - rotation_direction * h * v
    center_y = m_y + rotation_direction * h * u

    return center_x, center_y


def get_arc_angle_end(
    center_x: float, end_x: float, radius: float, flag_large_arc: bool
):
    """
    计算圆弧结束角度
    Calculate end angle of an arc
    """
    # Clamp the cosine value to [-1, 1] to handle floating point precision errors
    cosine_value = max(-1.0, min(1.0, (end_x - center_x) / radius))
    theta = math.acos(cosine_value) * 180 / math.pi
    return 180 + theta if flag_large_arc else 180 + theta