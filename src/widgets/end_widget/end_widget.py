import logging
import pathlib
from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QGroupBox,
)

logger = logging.getLogger(__name__)

class EndWidget(QGroupBox):
    exit_game_signal = pyqtSignal()
    restart_game_signal = pyqtSignal()
    def __init__(self, score: int, max_score: int, parent=None):
        super().__init__(parent)

        ui_path = pathlib.Path(__file__).parent / "EndWidget.ui"
        uic.loadUi(ui_path, self)

        logger.info("EndWidget UI loaded from %s", ui_path)

        self.score = score
        self.max_score = max_score

        self.setup_ui()
        self.connect_signals()

    def setup_ui(self):
        self.finalscore_label.setText(f"{self.score}/{self.max_score}")

    def connect_signals(self):
        self.again_button.clicked.connect(self.restart_game)
        self.exit_button.clicked.connect(self.emit_exit_signal)

    def restart_game(self):
        """Emit signal to restart the game."""
        logger.info("Restarting game")
        self.restart_game_signal.emit()

    def emit_exit_signal(self):
        """Emit signal to main window to close the app."""
        self.exit_game_signal.emit()