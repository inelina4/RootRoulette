import logging
import pathlib
from PyQt6 import uic
from PyQt6.QtWidgets import (
    QGroupBox,
    QMessageBox,
)

logger = logging.getLogger(__name__)

class StartWidget(QGroupBox):
    def __init__(self, parent=None):
        super().__init__(parent)

        ui_path = pathlib.Path(__file__).parent / "StartWidget.ui"
        uic.loadUi(ui_path, self)

        logger.info("Startwidget UI loaded from %s", ui_path)
        self.selected_rounds = None
        self.setup_ui()
        self.connect_signals()

    def setup_ui(self):
        self.play_button.setEnabled(False)
        self.choose_drop.clear()
        self.choose_drop.addItem("Choose")
        placeholder_index = self.choose_drop.findText("Choose")
        placeholder_item = self.choose_drop.model().item(placeholder_index)
        placeholder_item.setEnabled(False)

        self.choose_drop.addItems(["10", "15", "20"])

        self.choose_drop.setCurrentIndex(0)

    def connect_signals(self):
        self.howto_button.clicked.connect(self.show_instructions)
        self.choose_drop.currentIndexChanged.connect(self.on_rounds_selected)
        self.play_button.clicked.connect(self.start_game)

    def show_instructions(self):
        QMessageBox.information(
            self,
            "Welcome to RootRoulette!",
            "How to Play RootRoulette: \n\n"
            "• Choose how many words you want to guess\n"
            "• Each spin presents a word\n"
            "• Guess the correct linguistic origin from the language options\n"
            "• Earn points for each correct answer\n\n"
            "Spin wisely!"
        )

    def on_rounds_selected(self, index):
        if index < 0:
            self.play_button.setEnabled(False)
            return

        self.selected_rounds = int(self.choose_drop.currentText())
        logger.info("Number of rounds selected: %s", self.selected_rounds)
        self.play_button.setEnabled(True)

    def start_game(self):
        logger.info("Starting game with %s rounds", self.selected_rounds)

        parent = self.parent()
        if parent is None:
            return





