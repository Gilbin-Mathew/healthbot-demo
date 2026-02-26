# chat_bubble.py

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QFrame, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap


class ChatBubble(QWidget):
    def __init__(self, text=None, image=None, is_user=False):
        super().__init__()

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(10, 5, 10, 5)

        bubble = QFrame()
        bubble.setMaximumWidth(380)   # prevents stretching
        bubble.setStyleSheet(f"""
            QFrame {{
                background: transparent;
                border-radius: 15px;
                border: {" 1px solid #9AF23F" if is_user else "1px solid #FFDE52;"};
                padding: 8px;
            }}
        """)

        bubble_layout = QVBoxLayout(bubble)

        if text:
            label = QLabel(text)
            label.setWordWrap(True)
            label.setStyleSheet("color: white;")
            label.setMaximumWidth(360)
            bubble_layout.addWidget(label)

        if image:
            label = QLabel()
            pixmap = QPixmap()
            pixmap.loadFromData(image)
            pixmap = pixmap.scaledToWidth(
                300,
                Qt.TransformationMode.SmoothTransformation
            )
            label.setPixmap(pixmap)
            bubble_layout.addWidget(label)

        if is_user:
            main_layout.addStretch()
            main_layout.addWidget(bubble)
        else:
            main_layout.addWidget(bubble)
            main_layout.addStretch()
