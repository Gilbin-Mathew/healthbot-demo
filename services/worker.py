# worker.py

from PyQt6.QtCore import QThread, pyqtSignal
from services.backend import generate_response


class ChatWorker(QThread):
    finished_signal = pyqtSignal(str, list)

    def __init__(self, prompt):
        super().__init__()
        self.prompt = prompt

    def run(self):
        try:
            text, images = generate_response(self.prompt)
            self.finished_signal.emit(text, images)
        except Exception as e:
            self.finished_signal.emit(f"Error: {e}", [])
