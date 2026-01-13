import logging
import pathlib
import random
from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal, QThread, pyqtSlot, QObject
from PyQt6.QtWidgets import (
    QGroupBox,
    QMessageBox, QPushButton,
)

from src.services.etymology_service import EtymologyService, WordData

logger = logging.getLogger(__name__)

class WordLoaderWorker(QObject):
    finished = pyqtSignal(list)
    error = pyqtSignal(str)

    def __init__(self, total_rounds: int):
        super().__init__()
        self.total_rounds = total_rounds
        self.service = EtymologyService()

    def run(self):
        words = []
        seen = set()

        try:
            while len(words) < self.total_rounds:
                word = self.service.get_random_word()
                if not word or word in seen:
                    continue
                data = self.service.get_word_data_sync(word)
                if not data:
                    continue
                seen.add(word)
                words.append(data)
            self.finished.emit(words)
        except Exception as e:
            self.error.emit(str(e))

class GameWidget(QGroupBox):
    game_finished_signal = pyqtSignal(int, int, list, list)
    def __init__(self, total_rounds: int = 10, parent=None):
        super().__init__(parent)
        self.setWindowTitle("RootRoulette")

        ui_path = pathlib.Path(__file__).parent / "GameWidget.ui"
        uic.loadUi(ui_path, self)
        logger.info("GameWidget UI loaded from %s", ui_path)

        self.total_rounds = total_rounds
        self.current_round = 0
        self.score = 0

        self.word_pool: list[WordData] = []
        self.current_word_data: WordData | None = None

        self.correct_words = []
        self.incorrect_words = []

        self.language_buttons: list[QPushButton] = [
            self.lg_Button_1,
            self.lg_Button_2,
            self.lg_Button_3,
            self.lg_Button_4,
        ]

        self.setup_ui()
        self.connect_signals()
        self.prefetch_words()

    def setup_ui(self):
        self.word_label.setText("Loading words…")
        self.next_button.setEnabled(False)
        self.more_button.setEnabled(False)
        self.update_score_label()
        self.update_progress_label()

        for btn in self.language_buttons:
            btn.setEnabled(False)

    def update_progress_label(self):
        self.progress_label.setText(
        f"{self.current_round} spins out of {self.total_rounds}"
        )

    def prefetch_words(self):
        self.thread = QThread()
        self.worker = WordLoaderWorker(self.total_rounds)

        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.on_words_loaded)
        self.worker.error.connect(self.on_loading_error)

        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    def on_words_loaded(self, words: list[WordData]):
        self.word_pool = words
        self.start_round()

    def on_loading_error(self, message: str):
        QMessageBox.critical(self, "Loading Error", message)
        self.switch_to_end_widget()

    def connect_signals(self):
        for btn in self.language_buttons:
            btn.clicked.connect(self.handle_guess)

        self.next_button.clicked.connect(self.start_round)
        self.more_button.clicked.connect(self.show_explanation)

    def start_round(self):
        if self.current_round >= self.total_rounds:
            self.switch_to_end_widget()
            return

        self.current_word_data = self.word_pool[self.current_round]
        self.current_round += 1
        self.update_progress_label()

        self.word_label.setText(self.current_word_data.word.title())

        options = EtymologyService().get_language_options(
            self.current_word_data.correct_language
        )

        for btn, lang in zip(self.language_buttons, options):
            btn.setText(lang)
            btn.setEnabled(True)
            btn.setStyleSheet("")

        self.next_button.setEnabled(False)
        self.more_button.setEnabled(False)

    def handle_guess(self):
        clicked = self.sender()
        chosen = clicked.text()
        correct = self.current_word_data.correct_language

        for btn in self.language_buttons:
            btn.setEnabled(False)
            if btn.text() == correct:
                btn.setStyleSheet("background-color: green; color: white;")
            elif btn is clicked:
                btn.setStyleSheet("background-color: red; color: white;")

        if chosen == correct:
            self.score += 1
            self.correct_words.append(self.current_word_data.word)
        else:
            self.incorrect_words.append(self.current_word_data.word)

        self.update_score_label()
        self.next_button.setEnabled(True)
        self.more_button.setEnabled(True)

    def show_explanation(self):
        if self.current_word_data:
            explanation = f"Correct Answer: {self.current_word_data.correct_language}\n\n"
            explanation += self.current_word_data.etymology_text
            
            QMessageBox.information(
                self,
                f"Etymology of '{self.current_word_data.word.title()}'",
                explanation
            )
    def update_score_label(self):
        self.score_label.setText(f"{self.score}/{self.total_rounds}")

    def switch_to_end_widget(self):
        logger.info("Game finished with score %s/%s", self.score, self.total_rounds)
        self.game_finished_signal.emit(self.score, self.total_rounds, self.correct_words, self.incorrect_words)

