# -*- coding: utf-8 -*-
"""
现代化卡片组件
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QGraphicsDropShadowEffect
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor


class ModernCard(QWidget):
    """现代化卡片组件"""
    
    def __init__(self, title, subtitle="", parent=None):
        super().__init__(parent)
        
        self.title = title
        self.subtitle = subtitle
        
        self.setup_ui()
        self.setup_shadow()
        
    def setup_ui(self):
        """设置UI"""
        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 卡片容器
        card_container = QWidget()
        card_container.setObjectName("cardContainer")
        card_layout = QVBoxLayout(card_container)
        card_layout.setContentsMargins(30, 25, 30, 25)
        card_layout.setSpacing(15)
        
        # 标题区域
        if self.title:
            title_layout = QHBoxLayout()
            title_layout.setSpacing(10)
            
            title_label = QLabel(self.title)
            title_label.setObjectName("cardTitle")
            title_label.setStyleSheet("""
                QLabel#cardTitle {
                    font-size: 20px;
                    font-weight: 700;
                    color: #1e293b;
                }
            """)
            title_layout.addWidget(title_label)
            
            title_layout.addStretch()
            card_layout.addLayout(title_layout)
        
        # 副标题
        if self.subtitle:
            subtitle_label = QLabel(self.subtitle)
            subtitle_label.setObjectName("cardSubtitle")
            subtitle_label.setStyleSheet("""
                QLabel#cardSubtitle {
                    font-size: 14px;
                    color: #64748b;
                    margin-bottom: 10px;
                }
            """)
            card_layout.addWidget(subtitle_label)
        
        # 内容区域
        self.content_layout = QVBoxLayout()
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(15)
        card_layout.addLayout(self.content_layout)
        
        # 设置卡片样式
        card_container.setStyleSheet("""
            QWidget#cardContainer {
                background-color: white;
                border-radius: 16px;
                border: 1px solid #e2e8f0;
            }
        """)
        
        main_layout.addWidget(card_container)
        
    def setup_shadow(self):
        """设置阴影效果"""
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 10))
        shadow.setOffset(0, 4)
        self.setGraphicsEffect(shadow)


class ModernProgressBar(QWidget):
    """现代化进度条"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.progress = 0
        self.setup_ui()
        
    def setup_ui(self):
        """设置UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        
        # 进度条容器
        progress_container = QWidget()
        progress_container.setObjectName("progressContainer")
        progress_container.setFixedHeight(8)
        progress_container.setStyleSheet("""
            QWidget#progressContainer {
                background-color: #e2e8f0;
                border-radius: 4px;
            }
        """)
        
        # 进度条填充
        self.progress_fill = QWidget(progress_container)
        self.progress_fill.setObjectName("progressFill")
        self.progress_fill.setStyleSheet("""
            QWidget#progressFill {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #667eea, stop:1 #764ba2);
                border-radius: 4px;
            }
        """)
        self.progress_fill.setFixedWidth(0)
        
        layout.addWidget(progress_container)
        
        # 进度文本
        self.progress_label = QLabel("0%")
        self.progress_label.setStyleSheet("""
            color: #64748b;
            font-size: 12px;
            text-align: center;
        """)
        self.progress_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.progress_label)
        
    def set_progress(self, value):
        """设置进度"""
        self.progress = max(0, min(100, value))
        
        # 更新进度条宽度
        container_width = self.findChild(QWidget, "progressContainer").width()
        fill_width = int(container_width * self.progress / 100)
        self.progress_fill.setFixedWidth(fill_width)
        
        # 更新进度文本
        self.progress_label.setText(f"{self.progress}%")