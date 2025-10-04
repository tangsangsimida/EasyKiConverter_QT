# -*- coding: utf-8 -*-
"""
现代化导出选项组件
包含炫酷的UI特效和动画
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                           QGraphicsDropShadowEffect, QFrame)
from PyQt6.QtCore import (Qt, QPropertyAnimation, QEasingCurve, pyqtSignal, 
                        QTimer, QPoint, QRect, pyqtProperty)
from PyQt6.QtGui import (QColor, QPainter, QPen, QBrush, QLinearGradient, 
                        QFont, QFontMetrics, QMouseEvent)
import math


class AnimatedExportOption(QWidget):
    """动画导出选项组件"""
    
    # 选项状态改变信号
    stateChanged = pyqtSignal(bool)
    
    def __init__(self, title="", description="", icon="", parent=None):
        super().__init__(parent)
        
        self.title = title
        self.description = description
        self.icon = icon
        self._checked = False
        self._hovered = False
        self.animation_progress = 0.0
        
        # 动画相关
        self.hover_animation = None
        self.check_animation = None
        self.pulse_animation = None
        self.scale_animation = None
        self.ripple_effect = None
        self.ripples = []
        
        self.setup_ui()
        self.setup_animations()
        
    def setup_ui(self):
        """设置UI"""
        self.setFixedSize(280, 120)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
    def setup_animations(self):
        """设置动画"""
        # 悬停动画
        self.hover_animation = QPropertyAnimation(self, b"animation_progress")
        self.hover_animation.setDuration(300)
        self.hover_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        # 选中动画
        self.check_animation = QPropertyAnimation(self, b"animation_progress")
        self.check_animation.setDuration(400)
        self.check_animation.setEasingCurve(QEasingCurve.Type.OutBack)
        
        # 脉冲动画
        self.pulse_animation = QPropertyAnimation(self, b"animation_progress")
        self.pulse_animation.setDuration(1000)
        self.pulse_animation.setLoopCount(-1)
        self.pulse_animation.setStartValue(0.0)
        self.pulse_animation.setEndValue(1.0)
        
        # 初始化缩放因子
        self._scale_factor = 1.0
        
    def isChecked(self):
        """获取选中状态"""
        return self._checked
        
    def setChecked(self, checked):
        """设置选中状态"""
        if self._checked != checked:
            self._checked = checked
            
            # 启动选中动画
            if self.check_animation:
                self.check_animation.stop()
                start_value = 0.0 if checked else 1.0
                end_value = 1.0 if checked else 0.0
                self.check_animation.setStartValue(start_value)
                self.check_animation.setEndValue(end_value)
                self.check_animation.start()
            
            self.stateChanged.emit(checked)
            self.update()
            
    def mousePressEvent(self, event: QMouseEvent):
        """鼠标按下事件"""
        super().mousePressEvent(event)
        self.setChecked(not self._checked)
        
        # 添加涟漪效果
        self.add_ripple(event.pos())
        
        # 添加按下缩放效果
        self._scale_factor = 0.95
        self.update()
            
    def mouseReleaseEvent(self, event: QMouseEvent):
        """鼠标释放事件"""
        super().mouseReleaseEvent(event)
        
        # 恢复原始大小
        self._scale_factor = 1.0
        self.update()
            
    def enterEvent(self, event):
        """鼠标进入事件"""
        super().enterEvent(event)
        self._hovered = True
        
        if self.hover_animation:
            self.hover_animation.stop()
            self.hover_animation.setStartValue(self.animation_progress)
            self.hover_animation.setEndValue(1.0)
            self.hover_animation.start()
            
        # 启动脉冲动画（仅在选中时）
        if self._checked and self.pulse_animation:
            self.pulse_animation.start()
            
        # 添加悬停缩放效果
        self._scale_factor = 1.05
        self.update()
            
    def leaveEvent(self, event):
        """鼠标离开事件"""
        super().leaveEvent(event)
        self._hovered = False
        
        if self.hover_animation:
            self.hover_animation.stop()
            self.hover_animation.setStartValue(self.animation_progress)
            self.hover_animation.setEndValue(0.0)
            self.hover_animation.start()
            
        # 停止脉冲动画
        if self.pulse_animation:
            self.pulse_animation.stop()
            self.animation_progress = 0.0
            
        # 恢复原始大小
        self._scale_factor = 1.0
        self.update()
            
    def add_ripple(self, pos):
        """添加涟漪效果"""
        ripple = {
            'pos': pos,
            'radius': 0,
            'max_radius': 50,
            'opacity': 1.0
        }
        self.ripples.append(ripple)
        
        # 创建动画
        def update_ripple():
            if ripple in self.ripples:
                ripple['radius'] += 2
                ripple['opacity'] -= 0.05
                if ripple['opacity'] <= 0:
                    self.ripples.remove(ripple)
                self.update()
                
        timer = QTimer(self)
        timer.timeout.connect(update_ripple)
        timer.start(20)
        
        # 1秒后自动清理
        QTimer.singleShot(1000, lambda: timer.stop() if ripple in self.ripples else None)
        
    def paintEvent(self, event):
        """绘制事件"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # 应用缩放变换
        if hasattr(self, '_scale_factor') and self._scale_factor != 1.0:
            center_x = self.width() / 2
            center_y = self.height() / 2
            painter.translate(center_x, center_y)
            painter.scale(self._scale_factor, self._scale_factor)
            painter.translate(-center_x, -center_y)
        
        # 绘制背景
        self.draw_background(painter)
        
        # 绘制涟漪效果
        self.draw_ripples(painter)
        
        # 绘制边框
        self.draw_border(painter)
        
        # 绘制图标
        self.draw_icon(painter)
        
        # 绘制文本
        self.draw_text(painter)
        
        # 绘制选中指示器
        self.draw_check_indicator(painter)
        
    def draw_background(self, painter):
        """绘制背景"""
        # 背景渐变
        gradient = QLinearGradient(0, 0, 0, self.height())
        if self._checked:
            # 选中状态的渐变
            gradient.setColorAt(0, QColor(59, 130, 246, 230))  # 蓝色
            gradient.setColorAt(1, QColor(37, 99, 235, 230))  # 深蓝色
        else:
            # 未选中状态的渐变
            gradient.setColorAt(0, QColor(255, 255, 255, 230))  # 白色
            gradient.setColorAt(1, QColor(248, 250, 252, 230))  # 浅灰色
            
        # 悬停效果
        if self._hovered:
            # 增加悬停亮度
            # 使用固定颜色而不是尝试获取渐变颜色
            if self._checked:
                hover_color = QColor(79, 150, 255, 230)  # 更亮的蓝色
            else:
                hover_color = QColor(255, 255, 255, 250)  # 更亮的白色
            gradient.setColorAt(0, hover_color)
            
        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 16, 16)
        
        # 添加内阴影效果
        if self._checked:
            painter.setPen(QPen(QColor(0, 0, 0, 30), 1))
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawRoundedRect(1, 1, self.width() - 2, self.height() - 2, 16, 16)
        
    def draw_ripples(self, painter):
        """绘制涟漪效果"""
        for ripple in self.ripples:
            if ripple['radius'] > 0 and ripple['opacity'] > 0:
                painter.setPen(QPen(QColor(255, 255, 255, int(255 * ripple['opacity'] * 0.3)), 2))
                painter.setBrush(QBrush(QColor(255, 255, 255, int(255 * ripple['opacity'] * 0.1))))
                painter.drawEllipse(ripple['pos'], ripple['radius'], ripple['radius'])
                
    def draw_border(self, painter):
        """绘制边框"""
        # 基础边框
        painter.setPen(QPen(QColor(226, 232, 240), 1))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRoundedRect(1, 1, self.width() - 2, self.height() - 2, 16, 16)
        
        # 选中时的高亮边框
        if self._checked:
            highlight_gradient = QLinearGradient(0, 0, self.width(), 0)
            highlight_gradient.setColorAt(0, QColor(96, 165, 250))
            highlight_gradient.setColorAt(0.5, QColor(59, 130, 246))
            highlight_gradient.setColorAt(1, QColor(37, 99, 235))
            
            pen = QPen(highlight_gradient, 2)
            painter.setPen(pen)
            painter.drawRoundedRect(1, 1, self.width() - 2, self.height() - 2, 16, 16)
            
            # 添加发光效果
            glow_pen = QPen(QColor(59, 130, 246, 80), 4)
            glow_pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
            painter.setPen(glow_pen)
            painter.drawRoundedRect(3, 3, self.width() - 6, self.height() - 6, 14, 14)
            
    def draw_icon(self, painter):
        """绘制图标"""
        if not self.icon:
            return
            
        # 图标位置和大小
        icon_size = 40
        icon_x = 25
        icon_y = (self.height() - icon_size) // 2
        
        # 绘制图标背景圆
        painter.setPen(Qt.PenStyle.NoPen)
        if self._checked:
            # 选中时的渐变背景
            gradient = QLinearGradient(icon_x, icon_y, icon_x + icon_size, icon_y + icon_size)
            gradient.setColorAt(0, QColor(255, 255, 255, 230))
            gradient.setColorAt(1, QColor(241, 245, 249, 230))
            painter.setBrush(QBrush(gradient))
        else:
            painter.setBrush(QBrush(QColor(226, 232, 240, 200)))
        painter.drawEllipse(icon_x, icon_y, icon_size, icon_size)
        
        # 绘制图标文字
        painter.setPen(QColor(30, 41, 59) if self._checked else QColor(100, 116, 139))
        font = QFont("Segoe UI", 16, QFont.Weight.Bold)
        painter.setFont(font)
        painter.drawText(QRect(icon_x, icon_y, icon_size, icon_size), 
                        Qt.AlignmentFlag.AlignCenter, self.icon)
                        
        # 选中时添加发光效果
        if self._checked:
            painter.setPen(QPen(QColor(255, 255, 255, 100), 2))
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawEllipse(icon_x + 2, icon_y + 2, icon_size - 4, icon_size - 4)
            
    def draw_text(self, painter):
        """绘制文本"""
        # 标题
        if self._checked:
            # 选中时使用白色文字
            painter.setPen(QColor(255, 255, 255))
        else:
            # 未选中时使用深色文字
            painter.setPen(QColor(15, 23, 42))
            
        font = QFont("Segoe UI", 12, QFont.Weight.Bold)
        painter.setFont(font)
        
        title_x = 80
        title_y = 35
        painter.drawText(title_x, title_y, self.title)
        
        # 描述
        if self._checked:
            # 选中时使用浅灰色文字
            painter.setPen(QColor(241, 245, 249, 200))
        else:
            # 未选中时使用中灰色文字
            painter.setPen(QColor(100, 116, 139))
            
        font = QFont("Segoe UI", 9, QFont.Weight.Normal)
        painter.setFont(font)
        
        desc_x = 80
        desc_y = 60
        # 自动换行
        metrics = QFontMetrics(font)
        elided_text = metrics.elidedText(self.description, Qt.TextElideMode.ElideRight, 180)
        painter.drawText(desc_x, desc_y, elided_text)
        
    def draw_check_indicator(self, painter):
        """绘制选中指示器"""
        if not self._checked:
            return
            
        # 选中指示器位置
        indicator_size = 24
        indicator_x = self.width() - indicator_size - 20
        indicator_y = 20
        
        # 绘制背景圆（带动画效果）
        painter.setPen(Qt.PenStyle.NoPen)
        
        # 背景圆的动画效果
        if self.check_animation.state() == QPropertyAnimation.State.Running:
            # 动画进行中，根据进度调整透明度
            alpha = int(230 * self.animation_progress)
            painter.setBrush(QBrush(QColor(255, 255, 255, alpha)))
        else:
            painter.setBrush(QBrush(QColor(255, 255, 255, 230)))
            
        painter.drawEllipse(indicator_x, indicator_y, indicator_size, indicator_size)
        
        # 绘制对勾
        painter.setPen(QPen(QColor(37, 99, 235), 3, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        
        # 对勾的三个点
        center_x = indicator_x + indicator_size // 2
        center_y = indicator_y + indicator_size // 2
        
        # 第一个点
        p1_x = center_x - 6
        p1_y = center_y + 0
        
        # 第二个点
        p2_x = center_x - 1
        p2_y = center_y + 5
        
        # 第三个点
        p3_x = center_x + 6
        p3_y = center_y - 6
        
        # 绘制对勾（带动画效果）
        progress = self.animation_progress if self.check_animation.state() == QPropertyAnimation.State.Running else 1.0
        
        if progress > 0.3:
            # 绘制第一段
            end_progress = min(1.0, (progress - 0.3) / 0.7)
            end_x = int(p1_x + (p2_x - p1_x) * end_progress)
            end_y = int(p1_y + (p2_y - p1_y) * end_progress)
            painter.drawLine(QPoint(int(p1_x), int(p1_y)), QPoint(end_x, end_y))
            
        if progress > 0.6:
            # 绘制第二段
            end_progress = min(1.0, (progress - 0.6) / 0.4)
            start_x = int(p2_x)
            start_y = int(p2_y)
            end_x = int(p2_x + (p3_x - p2_x) * end_progress)
            end_y = int(p2_y + (p3_y - p2_y) * end_progress)
            painter.drawLine(QPoint(start_x, start_y), QPoint(end_x, end_y))
            
        # 添加发光效果
        if self.check_animation.state() != QPropertyAnimation.State.Running:
            glow_pen = QPen(QColor(37, 99, 235, 100), 6)
            glow_pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
            painter.setPen(glow_pen)
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawEllipse(indicator_x - 2, indicator_y - 2, indicator_size + 4, indicator_size + 4)
            
    @pyqtProperty(float)
    def animation_progress(self):
        return self._animation_progress if hasattr(self, '_animation_progress') else 0.0
        
    @animation_progress.setter
    def animation_progress(self, value):
        self._animation_progress = value
        self.update()
        
    @pyqtProperty(float)
    def scale_factor(self):
        return self._scale_factor if hasattr(self, '_scale_factor') else 1.0
        
    @scale_factor.setter
    def scale_factor(self, value):
        self._scale_factor = value
        self.update()


class ModernExportOptionsWidget(QFrame):
    """现代化导出选项组件"""
    
    # 导出选项改变信号
    exportOptionsChanged = pyqtSignal(dict)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.options = {
            'symbol': True,
            'footprint': True,
            'model3d': True,
            'manual': False  # 手册下载选项（暂时禁用）
        }
        
        self.symbol_option = None
        self.footprint_option = None
        self.model3d_option = None
        self.manual_option = None  # 手册选项
        
        self.setup_ui()
        self.setup_connections()
        
    def setup_ui(self):
        """设置UI"""
        self.setObjectName("modernExportOptions")
        self.setStyleSheet("""
            QFrame#modernExportOptions {
                background-color: transparent;
                border: none;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)
        
        # 选项容器
        options_layout = QHBoxLayout()
        options_layout.setSpacing(25)
        options_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        # 符号选项
        self.symbol_option = AnimatedExportOption(
            title="原理图符号",
            description="导出.kicad_sym符号库文件",
            icon="S"
        )
        self.symbol_option.setChecked(True)
        options_layout.addWidget(self.symbol_option)
        
        # 封装选项
        self.footprint_option = AnimatedExportOption(
            title="PCB封装",
            description="导出.kicad_mod封装文件",
            icon="F"
        )
        self.footprint_option.setChecked(True)
        options_layout.addWidget(self.footprint_option)
        
        # 3D模型选项
        self.model3d_option = AnimatedExportOption(
            title="3D模型",
            description="导出.step/.wrl 3D模型文件",
            icon="3D"
        )
        self.model3d_option.setChecked(True)
        options_layout.addWidget(self.model3d_option)
        
        # 手册下载选项（暂时禁用）
        self.manual_option = AnimatedExportOption(
            title="手册下载",
            description="下载元件技术手册（即将推出）",
            icon="📖"
        )
        self.manual_option.setChecked(False)
        self.manual_option.setEnabled(False)  # 暂时禁用
        options_layout.addWidget(self.manual_option)
        
        options_layout.addStretch()
        layout.addLayout(options_layout)
        
    def setup_connections(self):
        """设置连接"""
        self.symbol_option.stateChanged.connect(
            lambda checked: self.on_option_changed('symbol', checked))
        self.footprint_option.stateChanged.connect(
            lambda checked: self.on_option_changed('footprint', checked))
        self.model3d_option.stateChanged.connect(
            lambda checked: self.on_option_changed('model3d', checked))
        # 手册选项暂时不连接信号，因为功能未实现
            
    def on_option_changed(self, option_name, checked):
        """选项改变处理"""
        # 手册选项暂时不处理
        if option_name == 'manual':
            return
            
        self.options[option_name] = checked
        self.exportOptionsChanged.emit(self.options.copy())
        
    def get_export_options(self):
        """获取导出选项"""
        return self.options.copy()
        
    def set_export_options(self, options):
        """设置导出选项"""
        self.options.update(options)
        
        if self.symbol_option:
            self.symbol_option.setChecked(self.options.get('symbol', True))
        if self.footprint_option:
            self.footprint_option.setChecked(self.options.get('footprint', True))
        if self.model3d_option:
            self.model3d_option.setChecked(self.options.get('model3d', True))
        # 手册选项暂时不设置
            
    def setEnabled(self, enabled):
        """设置启用状态"""
        super().setEnabled(enabled)
        if self.symbol_option:
            self.symbol_option.setEnabled(enabled)
        if self.footprint_option:
            self.footprint_option.setEnabled(enabled)
        if self.model3d_option:
            self.model3d_option.setEnabled(enabled)
        # 手册选项保持禁用状态
        if self.manual_option:
            self.manual_option.setEnabled(False)