#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
现代化UI增强组件
提供加载动画、过渡效果和其他视觉增强
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                           QFrame, QGraphicsOpacityEffect, QPushButton)
from PyQt6.QtCore import (Qt, QPropertyAnimation, QEasingCurve, QTimer, 
                        QSequentialAnimationGroup)
from PyQt6.QtGui import QColor, QPainter, QPen, QBrush, QLinearGradient, QFont


class LoadingSpinner(QWidget):
    """现代化加载动画"""
    
    def __init__(self, parent=None, size=60, color="#2563eb"):
        super().__init__(parent)
        self.size = size
        self.color = QColor(color)
        self.angle = 0
        self.animation = None
        self.setup_ui()
        
    def setup_ui(self):
        """设置UI"""
        self.setFixedSize(self.size, self.size)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # 创建旋转动画
        self.animation = QPropertyAnimation(self, b"angle")
        self.animation.setDuration(1500)
        self.animation.setStartValue(0)
        self.animation.setEndValue(360)
        self.animation.setLoopCount(-1)  # 无限循环
        self.animation.setEasingCurve(QEasingCurve.Type.Linear)
        
    def start(self):
        """开始动画"""
        self.animation.start()
        self.show()
        
    def stop(self):
        """停止动画"""
        self.animation.stop()
        self.hide()
        
    def paintEvent(self, event):
        """绘制事件"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # 绘制背景圆环
        painter.setPen(QPen(QColor(0, 0, 0, 20), 4))
        painter.drawEllipse(10, 10, self.size - 20, self.size - 20)
        
        # 绘制旋转的进度弧
        gradient = QLinearGradient(0, 0, self.size, self.size)
        gradient.setColorAt(0, self.color)
        gradient.setColorAt(1, QColor(self.color.red(), self.color.green(), self.color.blue(), 100))
        
        pen = QPen(gradient, 4)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        
        # 绘制弧形
        start_angle = self.angle * 16  # Qt使用1/16度
        span_angle = 270 * 16  # 270度的弧
        painter.drawArc(10, 10, self.size - 20, self.size - 20, start_angle, span_angle)
        
    @pyqtProperty(int)
    def angle(self):
        return self._angle if hasattr(self, '_angle') else 0
        
    @angle.setter
    def angle(self, value):
        self._angle = value
        self.update()


class ModernCard(QFrame):
    """现代化卡片组件"""
    
    def __init__(self, parent=None, title="", icon="", description=""):
        super().__init__(parent)
        self.title = title
        self.icon = icon
        self.description = description
        self.setup_ui()
        self.setup_animations()
        
    def setup_ui(self):
        """设置UI"""
        self.setObjectName("modernCard")
        self.setStyleSheet("""
            QFrame#modernCard {
                background-color: white;
                border: 1px solid #e2e8f0;
                border-radius: 16px;
                padding: 25px;
            }
            QFrame#modernCard:hover {
            border-color: #cbd5e1;
        }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(15)
        
        # 标题区域
        header_layout = QHBoxLayout()
        
        if self.icon:
            icon_label = QLabel(self.icon)
            icon_label.setStyleSheet("font-size: 24px; margin-right: 10px;")
            header_layout.addWidget(icon_label)
            
        if self.title:
            title_label = QLabel(self.title)
            title_label.setStyleSheet("""
                font-size: 18px;
                font-weight: 600;
                color: #1e293b;
            """)
            header_layout.addWidget(title_label)
            
        header_layout.addStretch()
        layout.addLayout(header_layout)
        
        # 描述
        if self.description:
            desc_label = QLabel(self.description)
            desc_label.setStyleSheet("""
                font-size: 14px;
                color: #64748b;
                line-height: 20px;
            """)
            desc_label.setWordWrap(True)
            layout.addWidget(desc_label)
            
    def setup_animations(self):
        """设置动画"""
        # 悬停动画
        self.hover_animation = QPropertyAnimation(self, b"geometry")
        self.hover_animation.setDuration(200)
        self.hover_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        # 透明度动画
        self.opacity_effect = QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.opacity_effect)
        self.opacity_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.opacity_animation.setDuration(300)
        
    def enterEvent(self, event):
        """鼠标进入事件"""
        super().enterEvent(event)
        # 添加悬停效果
        current_geom = self.geometry()
        new_geom = current_geom.adjusted(-2, -2, 2, 2)
        self.hover_animation.setStartValue(current_geom)
        self.hover_animation.setEndValue(new_geom)
        self.hover_animation.start()
        
    def leaveEvent(self, event):
        """鼠标离开事件"""
        super().leaveEvent(event)
        # 恢复原状
        current_geom = self.geometry()
        original_geom = current_geom.adjusted(2, 2, -2, -2)
        self.hover_animation.setStartValue(current_geom)
        self.hover_animation.setEndValue(original_geom)
        self.hover_animation.start()
        
    def fade_in(self, delay=0):
        """淡入动画"""
        self.opacity_effect.setOpacity(0)
        self.opacity_animation.setStartValue(0)
        self.opacity_animation.setEndValue(1)
        self.opacity_animation.setStartDelay(delay)
        self.opacity_animation.start()
        
    def fade_out(self, delay=0):
        """淡出动画"""
        self.opacity_animation.setStartValue(1)
        self.opacity_animation.setEndValue(0)
        self.opacity_animation.setStartDelay(delay)
        self.opacity_animation.start()


class AnimatedButton(QPushButton):
    """动画按钮"""
    
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setup_style()
        self.setup_animations()
        
    def setup_style(self):
        """设置样式"""
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumHeight(50)
        self.setFont(QFont("Segoe UI", 12, QFont.Weight.Medium))
        
    def setup_animations(self):
        """设置动画"""
        # 缩放动画
        self.scale_animation = QPropertyAnimation(self, b"geometry")
        self.scale_animation.setDuration(150)
        self.scale_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        # 颜色动画
        self.color_animation = QPropertyAnimation(self, b"styleSheet")
        self.color_animation.setDuration(200)
        
    def mousePressEvent(self, event):
        """鼠标按下"""
        super().mousePressEvent(event)
        # 按下效果
        if self.scale_animation.state() == QPropertyAnimation.State.Stopped:
            current_geom = self.geometry()
            pressed_geom = current_geom.adjusted(1, 1, -1, -1)
            self.scale_animation.setStartValue(current_geom)
            self.scale_animation.setEndValue(pressed_geom)
            self.scale_animation.start()
            
    def mouseReleaseEvent(self, event):
        """鼠标释放"""
        super().mouseReleaseEvent(event)
        # 释放效果
        if hasattr(self, 'original_geometry'):
            current_geom = self.geometry()
            self.scale_animation.setStartValue(current_geom)
            self.scale_animation.setEndValue(self.original_geometry)
            self.scale_animation.start()
            
    def enterEvent(self, event):
        """鼠标进入"""
        super().enterEvent(event)
        if not hasattr(self, 'original_geometry'):
            self.original_geometry = self.geometry()
            
        # 悬停放大效果
        current_geom = self.geometry()
        hover_geom = current_geom.adjusted(-1, -1, 1, 1)
        self.scale_animation.setStartValue(current_geom)
        self.scale_animation.setEndValue(hover_geom)
        self.scale_animation.start()
        
    def leaveEvent(self, event):
        """鼠标离开"""
        super().leaveEvent(event)
        if hasattr(self, 'original_geometry'):
            current_geom = self.geometry()
            self.scale_animation.setStartValue(current_geom)
            self.scale_animation.setEndValue(self.original_geometry)
            self.scale_animation.start()


class SuccessAnimation(QWidget):
    """成功动画组件"""
    
    def __init__(self, parent=None, text="操作成功"):
        super().__init__(parent)
        self.text = text
        self.setup_ui()
        
    def setup_ui(self):
        """设置UI"""
        self.setFixedSize(200, 200)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # 成功图标
        self.icon_label = QLabel("✅")
        self.icon_label.setStyleSheet("""
            font-size: 64px;
            background: transparent;
        """)
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.icon_label)
        
        # 成功文字
        self.text_label = QLabel(self.text)
        self.text_label.setStyleSheet("""
            font-size: 18px;
            font-weight: 600;
            color: #10b981;
            background: transparent;
        """)
        self.text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.text_label)
        
    def show_animation(self, duration=2000):
        """显示动画"""
        self.show()
        
        # 缩放动画
        scale_anim = QPropertyAnimation(self, b"geometry")
        scale_anim.setDuration(300)
        scale_anim.setEasingCurve(QEasingCurve.Type.OutBack)
        
        # 淡入动画
        opacity_effect = QGraphicsOpacityEffect()
        self.setGraphicsEffect(opacity_effect)
        fade_anim = QPropertyAnimation(opacity_effect, b"opacity")
        fade_anim.setDuration(300)
        
        # 设置动画序列
        self.animation_group = QSequentialAnimationGroup()
        self.animation_group.addAnimation(fade_anim)
        self.animation_group.addAnimation(scale_anim)
        
        # 开始动画
        opacity_effect.setOpacity(0)
        fade_anim.setStartValue(0)
        fade_anim.setEndValue(1)
        
        # 延迟后自动隐藏
        QTimer.singleShot(duration, self.hide_animation)
        
        self.animation_group.start()
        
    def hide_animation(self):
        """隐藏动画"""
        fade_anim = QPropertyAnimation(self.graphicsEffect(), b"opacity")
        fade_anim.setDuration(200)
        fade_anim.setStartValue(1)
        fade_anim.setEndValue(0)
        fade_anim.finished.connect(self.hide)
        fade_anim.start()


class RippleEffect:
    """涟漪效果类"""
    
    def __init__(self, parent, color=QColor(37, 99, 235, 100)):
        self.parent = parent
        self.color = color
        self.ripples = []
        
    def add_ripple(self, pos, radius=50):
        """添加涟漪"""
        ripple = {
            'pos': pos,
            'radius': 0,
            'max_radius': radius,
            'opacity': 1.0,
            'animation': None
        }
        self.ripples.append(ripple)
        
        # 创建动画
        anim = QPropertyAnimation(self.parent, b"")
        anim.setDuration(600)
        anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        anim.valueChanged.connect(lambda: self.update_ripple(ripple))
        anim.finished.connect(lambda: self.remove_ripple(ripple))
        
        ripple['animation'] = anim
        anim.start()
        
    def update_ripple(self, ripple):
        """更新涟漪状态"""
        if ripple['animation']:
            progress = ripple['animation'].currentValue() if hasattr(ripple['animation'], 'currentValue') else 0
            ripple['radius'] = progress * ripple['max_radius']
            ripple['opacity'] = 1.0 - progress
            self.parent.update()
            
    def remove_ripple(self, ripple):
        """移除涟漪"""
        if ripple in self.ripples:
            self.ripples.remove(ripple)
            self.parent.update()
            
    def paint_ripples(self, painter):
        """绘制所有涟漪"""
        for ripple in self.ripples:
            if ripple['radius'] > 0:
                painter.setPen(QPen(QColor(self.color.red(), self.color.green(), self.color.blue(), 
                                         int(self.color.alpha() * ripple['opacity'])), 2))
                painter.setBrush(QBrush(QColor(self.color.red(), self.color.green(), self.color.blue(), 
                                             int(self.color.alpha() * ripple['opacity'] * 0.3))))
                painter.drawEllipse(ripple['pos'], ripple['radius'], ripple['radius'])


class ModernProgressBar(QWidget):
    """现代化进度条"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.progress = 0
        self.animation_duration = 500
        self.setup_ui()
        
    def setup_ui(self):
        """设置UI"""
        self.setFixedHeight(8)
        self.setStyleSheet("""
            QWidget {
                background-color: #f1f5f9;
                border-radius: 4px;
            }
        """)
        
    def set_progress(self, value, animated=True):
        """设置进度"""
        if animated:
            self.animation = QPropertyAnimation(self, b"progress")
            self.animation.setDuration(self.animation_duration)
            self.animation.setStartValue(self.progress)
            self.animation.setEndValue(value)
            self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)
            self.animation.start()
        else:
            self.progress = value
            self.update()
            
    def paintEvent(self, event):
        """绘制事件"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # 背景
        painter.setBrush(QBrush(QColor(241, 245, 249)))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 4, 4)
        
        # 进度
        if self.progress > 0:
            gradient = QLinearGradient(0, 0, self.width(), 0)
            gradient.setColorAt(0, QColor(37, 99, 235))
            gradient.setColorAt(1, QColor(59, 130, 246))
            
            painter.setBrush(QBrush(gradient))
            progress_width = int(self.width() * self.progress / 100)
            painter.drawRoundedRect(0, 0, progress_width, self.height(), 4, 4)
            
    @pyqtProperty(int)
    def progress(self):
        return self._progress if hasattr(self, '_progress') else 0
        
    @progress.setter
    def progress(self, value):
        self._progress = max(0, min(100, value))
        self.update()