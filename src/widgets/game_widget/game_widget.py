import logging
import pathlib
import random
from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QGroupBox,
    QMessageBox, QPushButton,
)

logger = logging.getLogger(__name__)

WORDS = [
    {
        "word": "school",
        "origin": "Greek",
        "explanation": "From Greek 'scholē', meaning leisure or learning."
    },
    {
        "word": "hospital",
        "origin": "Latin",
        "explanation": "From Latin 'hospitalis', meaning guest or host."
    },
    {
        "word": "anger",
        "origin": "Old English",
        "explanation": "From Old English 'angr', meaning grief or distress."
    },
    {
        "word": "judge",
        "origin": "French",
        "explanation": "From Old French 'juger', meaning to judge."
    },
]

LANGUAGES = ["Greek", "Latin", "Old English", "French"]


class GameWidget(QGroupBox):
    game_finished_signal = pyqtSignal(int, int)
    
    def __init__(self, rounds: int = 10, parent=None):
        super().__init__(parent)

        ui_path = pathlib.Path(__file__).parent / "GameWidget.ui"
        uic.loadUi(ui_path, self)

        logger.info("GameWidget UI loaded from %s", ui_path)

        self.max_rounds = rounds
        self.current_round = 0
        self.score = 0
        self.current_word = None

        self.language_buttons: list[QPushButton] = [
            self.lg_Button_1,
            self.lg_Button_2,
            self.lg_Button_3,
            self.lg_Button_4,
        ]

        self.setup_ui()
        self.connect_signals()
        self.start_round()

    def setup_ui(self):
        self.next_button.setEnabled(False)
        self.more_button.setEnabled(False)
        self.update_score_label()

    def connect_signals(self):
        for btn in self.language_buttons:
            btn.clicked.connect(self.handle_guess)

        self.next_button.clicked.connect(self.start_round)
        self.more_button.clicked.connect(self.show_explanation)

    def start_round(self):
        if self.current_round >= self.max_rounds:
            self.switch_to_end_widget()
            return
        self.current_round += 1
        self.current_word = random.choice(WORDS)
        self.word_label.setText(self.current_word["word"])

        random.shuffle(LANGUAGES)
        for btn, lang in zip(self.language_buttons, LANGUAGES):
            btn.setText(lang)
            btn.setEnabled(True)
            btn.setStyleSheet("")

        self.next_button.setEnabled(False)
        self.more_button.setEnabled(False)
        self.update_score_label()

    def handle_guess(self):
        clicked_button = self.sender()
        chosen_language = clicked_button.text()
        correct_language = self.current_word["origin"]

        for btn in self.language_buttons:
            btn.setEnabled(False)
            if btn.text() == correct_language:
                btn.setStyleSheet("background-color: green; color: white;")
            elif btn is clicked_button:
                btn.setStyleSheet("background-color: red; color: white;")

        if chosen_language == correct_language:
            self.score += 1
        self.update_score_label()
        self.next_button.setEnabled(True)
        self.more_button.setEnabled(True)

    def show_explanation(self):
        QMessageBox.information(
            self,
            f"Origin of '{self.current_word['word']}'",
            self.current_word["explanation"]
        )
    def update_score_label(self):
        self.score_label.setText(f"{self.score}/{self.max_rounds}")

    def switch_to_end_widget(self):
        """Emit signal when all rounds are done"""
        logger.info("Game finished with score %s/%s", self.score, self.max_rounds)
        self.game_finished_signal.emit(self.score, self.max_rounds)

