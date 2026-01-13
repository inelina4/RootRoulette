import logging
import pathlib
from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QGroupBox,
    QMessageBox,
)

logger = logging.getLogger(__name__)

class EndWidget(QGroupBox):
    exit_game_signal = pyqtSignal()
    restart_game_signal = pyqtSignal()

    def __init__(self, score: int, max_score: int, correct_words=None, incorrect_words=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("RootRoulette")

        ui_path = pathlib.Path(__file__).parent / "EndWidget.ui"
        uic.loadUi(ui_path, self)

        logger.info("EndWidget UI loaded from %s", ui_path)

        self.score = score
        self.max_score = max_score
        self.correct_words = correct_words or []
        self.incorrect_words = incorrect_words or []

        print(self.correct_words, self.incorrect_words)

        self.setup_ui()
        self.connect_signals()

    def setup_ui(self):
        self.finalscore_label.setText(f"{self.score}/{self.max_score}")

    def connect_signals(self):
        self.again_button.clicked.connect(self.restart_game)
        self.exit_button.clicked.connect(self.emit_exit_signal)
        if hasattr(self, "check_button"):
            self.check_button.clicked.connect(self.show_summary)

    def restart_game(self):
        logger.info("Restarting game")
        self.restart_game_signal.emit()

    def emit_exit_signal(self):
        self.exit_game_signal.emit()

    def show_summary(self):
        summary_text = "Correct Words:\n"
        if self.correct_words:
            summary_text += "\n".join(self.correct_words)
        else:
            summary_text += "None"

        summary_text += "\n\nIncorrect Words:\n"
        if self.incorrect_words:
            summary_text += "\n".join(self.incorrect_words)
        else:
            summary_text += "None"

        QMessageBox.information(self, "Game Summary", summary_text)