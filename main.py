import os
import sys
import time
import asyncio
import yaml

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QScrollArea, QInputDialog
from PyQt6.QtCore import Qt

from utils.config_loader import ConfigLoader
from models.model import FoodClassifier
from ui.blecal_ui import Ui_BleCal
from ui.chat_bubble import ChatBubble
from services.worker import ChatWorker
from ui.paste_image_label import PasteImageLabel


class ChatWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_BleCal()
        self.ui.setupUi(self)

        self.setup_chat_area()
        self.connect_signals()
        
        self.worker = None
        self.loading_bubble = None

        self.paste_label = PasteImageLabel(self.ui.imagelabel.parent())
        self.paste_label.setGeometry(self.ui.imagelabel.geometry())

        self.ui.imagelabel.deleteLater()
        self.ui.imagelabel = self.paste_label
        self.ui.addbutton.clicked.connect(self.on_click_add)

        self.user_age = None
        self.user_gender = None
        self.user_height = None

        self.ui.ActionAge.triggered.connect(self.set_age)
        self.ui.ActionHeight.triggered.connect(self.set_height)
        self.ui.ActionGender.triggered.connect(self.set_gender)

        return

    def set_age(self):

        with open("config.yaml") as f:
            config = yaml.safe_load(f)

        current_age = config["scale"]["user"]["age"]

        value, ok = QInputDialog.getInt(
            self,
            "Age",
            "Enter Age:",
            current_age,   # previously saved value
            1,
            120
        )

        if ok:
            config["scale"]["user"]["age"] = value

            with open("config.yaml", "w") as f:
                yaml.dump(config, f, sort_keys=False)
        return

    def set_height(self):

        with open("config.yaml") as f:
            config = yaml.safe_load(f)

        current_height = config["scale"]["user"]["height"]

        value, ok = QInputDialog.getDouble(
            self,
            "Height",
            "Enter Height (cm):",
            current_height,   # default value
            50,
            250
        )

        if ok:
            config["scale"]["user"]["height"] = value

            with open("config.yaml", "w") as f:
                yaml.dump(config, f, sort_keys=False)
        return

    def set_gender(self):

        with open("config.yaml") as f:
            config = yaml.safe_load(f)

        current_gender = config["scale"]["user"]["gender"]

        items = ["male", "female"]
        default_index = items.index(current_gender)

        value, ok = QInputDialog.getItem(
            self,
            "Gender",
            "Select Gender:",
            items,
            default_index,   # previously saved value
            False
        )

        if ok:
            config["scale"]["user"]["gender"] = value

            with open("config.yaml", "w") as f:
                yaml.dump(config, f, sort_keys=False)
        return

    def on_click_add(self):
        self.ui.chatedit.setPlaceholderText("  Loading image...")
        self.recognition("models/food_model.pth")
        self.delete_image()
        if self.classified["confidence"] > 60:
            self.ui.chatedit.setPlainText(self.classified["food"])
        self.ui.chatedit.setPlaceholderText(" Ask anything  ")
        return

    def recognition(self, model_path):
        imgpath = self.ui.imagelabel.image_path
        if not imgpath:
            print("image not exists")
            return ''
        if not model_path:
            print('model not found')
            return ''
        self.rec_model = FoodClassifier(model_path)
        self.classified = self.rec_model.predict(imgpath)
        return


    def delete_image(self):
        path = self.ui.imagelabel.image_path

        if not path:
            print("No image to delete")
            return

        if os.path.exists(path):
            os.remove(path)
            print("Image deleted")

            # Optional: clear the label visually
            self.ui.imagelabel.clear()
            self.ui.imagelabel._image_path = None
        else:
            print("File already removed")
        return

    def setup_chat_area(self):
        # Replace chatcontentframe with scrollable layout

        self.scroll_bar = QScrollArea(self.ui.chatcontentframe)
        self.scroll_bar.setGeometry(0, 0, 511, 521)
        self.scroll_bar.setWidgetResizable(True)
        self.scroll_bar.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_bar.setStyleSheet("""
        QScrollArea {
            background: transparent;
            border: none;
        }
    """)
        

        self.chat_container = QWidget()
        self.chat_container.setStyleSheet("background: transparent;")
        self.chat_layout = QVBoxLayout(self.chat_container)
        self.chat_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.chat_layout.setSpacing(10)

        self.scroll_bar.setWidget(self.chat_container)

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
        bar = self.scroll_bar.verticalScrollBar()
        bar.setValue(bar.maximum())

def main():
    app = QApplication(sys.argv)
    window = ChatWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
