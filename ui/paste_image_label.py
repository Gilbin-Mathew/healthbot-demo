import os
import uuid
from PyQt6.QtWidgets import QLabel, QMenu
from PyQt6.QtGui import QPixmap, QGuiApplication, QAction
from PyQt6.QtCore import Qt, pyqtSignal


class PasteImageLabel(QLabel):

    image_pasted = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # IMPORTANT FIXES
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

        self._image_path = None
        self._original_pixmap = None

        # Optional placeholder
        self.setText("Right Click → Paste\nor\nClick and Press Ctrl+V")
        self.setStyleSheet("""
            QLabel {
                border: 2px dashed gray;
                color: gray;
            }
        """)

    # ---------------------------
    # Mouse click gives focus
    # ---------------------------
    def mousePressEvent(self, event):
        self.setFocus()
        super().mousePressEvent(event)

    # ---------------------------
    # Ctrl+V detection
    # ---------------------------
    def keyPressEvent(self, event):
        if event.matches(event.StandardKey.Paste):
            self.paste_image()
        else:
            super().keyPressEvent(event)

    # ---------------------------
    # Right-click menu
    # ---------------------------
    def show_context_menu(self, position):
        menu = QMenu(self)

        paste_action = QAction("Paste", self)
        paste_action.triggered.connect(self.paste_image)

        menu.addAction(paste_action)
        menu.exec(self.mapToGlobal(position))

    # ---------------------------
    # Paste logic
    # ---------------------------
    def paste_image(self):
        clipboard = QGuiApplication.clipboard()
        mime = clipboard.mimeData()

        if not mime.hasImage():
            print("Clipboard does not contain an image")
            return

        image = clipboard.image()

        filename = f"pasted_{uuid.uuid4().hex}.png"
        path = os.path.join(os.getcwd(), filename)
        image.save(path)

        self._image_path = path
        self._original_pixmap = QPixmap.fromImage(image)

        self.setStyleSheet("")  # remove dashed border
        self.setText("")        # remove placeholder

        self.update_scaled_pixmap()

        self.image_pasted.emit(path)

    # ---------------------------
    # Resize handling
    # ---------------------------
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_scaled_pixmap()

    def update_scaled_pixmap(self):
        if not self._original_pixmap:
            return

        scaled = self._original_pixmap.scaled(
            self.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )

        self.setPixmap(scaled)

    @property
    def image_path(self):
        return self._image_path
