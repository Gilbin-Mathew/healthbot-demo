# main.py

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QScrollArea
from PyQt6.QtCore import Qt
from ui.blecal_ui import Ui_BleCal

from chat_bubble import ChatBubble
from worker import ChatWorker


class BleCalWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_BleCal()
        self.ui.setupUi(self)

        self.setup_chat_area()
        self.connect_signals()

        self.worker = None
        self.loading_bubble = None

    def setup_chat_area(self):
        # Replace chatcontentframe with scrollable layout

        self.scroll = QScrollArea(self.ui.chatcontentframe)
        self.scroll.setGeometry(0, 0, 511, 521)
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.chat_container = QWidget()
        self.chat_layout = QVBoxLayout(self.chat_container)
        self.chat_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.chat_layout.setSpacing(10)

        self.scroll.setWidget(self.chat_container)

    def connect_signals(self):
        self.ui.uploadbutton.clicked.connect(self.send_message)

    def send_message(self):
        text = self.ui.chatedit.toPlainText().strip()
        if not text:
            return

        self.ui.chatedit.clear()

        # User bubble
        self.add_bubble(text=text, is_user=True)

        # Loading bubble
        self.loading_bubble = ChatBubble(text="...", is_user=False)
        self.chat_layout.addWidget(self.loading_bubble)
        self.auto_scroll()

        # Start worker
        self.worker = ChatWorker(text)
        self.worker.finished_signal.connect(self.handle_response)
        self.worker.start()

    def handle_response(self, text, images):
        if self.loading_bubble:
            self.loading_bubble.deleteLater()
            self.loading_bubble = None

        if text:
            self.add_bubble(text=text, is_user=False)

        for img in images:
            self.add_bubble(image=img, is_user=False)

    def add_bubble(self, text=None, image=None, is_user=False):
        bubble = ChatBubble(text=text, image=image, is_user=is_user)
        self.chat_layout.addWidget(bubble)
        self.auto_scroll()

    def auto_scroll(self):
        bar = self.scroll.verticalScrollBar()
        bar.setValue(bar.maximum())

def main():
    app = QApplication(sys.argv)
    window = BleCalWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
