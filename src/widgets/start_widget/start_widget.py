import logging
import pathlib
import json
import random
from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QGroupBox,
    QMessageBox,
    QLabel,
)

logger = logging.getLogger(__name__)

class StartWidget(QGroupBox):
    start_game_signal = pyqtSignal(int)
    exit_game_signal = pyqtSignal()
    def __init__(self, parent=None, last_result=None):
        super().__init__(parent)

        ui_path = pathlib.Path(__file__).parent / "StartWidget.ui"
        uic.loadUi(ui_path, self)

        self.setWindowTitle("RootRoulette")


        logger.info("Startwidget UI loaded from %s", ui_path)
        self.selected_rounds = None
        self.greeting_label = QLabel(self)
        self.greeting_label.setObjectName("greeting_label")
        self.greeting_label.setWordWrap(True)

        font = QFont("Bahnschrift")
        font.setPointSize(12)
        font.setWeight(QFont.Weight.Medium)
        font.setItalic(True)
        self.greeting_label.setFont(font)

        self.layout().insertWidget(0, self.greeting_label)
        self.setup_ui()
        self.connect_signals()
        self.set_greeting(last_result)

    def set_greeting(self, last_result):
        try:
            # Load greetings from JSON file  
            base_dir = pathlib.Path(__file__).resolve().parent.parent.parent.parent
            greetings_path = base_dir / "greetings.json"
            
            with open(greetings_path, 'r', encoding='utf-8') as f:
                greetings = json.load(f)
            
            if not last_result:
                # First time player
                greeting = random.choice(greetings["first_time"])
                self.greeting_label.setText(greeting)
                return
            
            score = last_result.get("score", 0)
            max_score = last_result.get("max_score", 1)
            
            if max_score == 0:
                percent = 0
            else:
                percent = score / max_score
            
            if percent >= 0.8:
                greeting_list = greetings["high_score"]
            elif percent <= 0.4:
                greeting_list = greetings["low_score"] 
            else:
                greeting_list = greetings["medium_score"]
            
            greeting_template = random.choice(greeting_list)
            greeting = greeting_template.format(score=score, max_score=max_score)
            self.greeting_label.setText(greeting)
            
        except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
            logger.warning(f"Failed to load greetings: {e}")
            if not last_result:
                self.greeting_label.setText("Welcome to RootRoulette!")
            else:
                score = last_result.get("score", 0)
                max_score = last_result.get("max_score", 1)
                self.greeting_label.setText(f"Welcome back! Last score: {score} out of {max_score}.")

    def setup_ui(self):
        self.play_button.setEnabled(False)
        self.choose_drop.clear()
        self.choose_drop.addItem("Choose")
        placeholder_index = self.choose_drop.findText("Choose")
        placeholder_item = self.choose_drop.model().item(placeholder_index)
        placeholder_item.setEnabled(False)

        self.choose_drop.addItems(["2","10", "15", "20"])

        self.choose_drop.setCurrentIndex(0)

    def connect_signals(self):
        self.howto_button.clicked.connect(self.show_instructions)
        self.choose_drop.currentIndexChanged.connect(self.on_rounds_selected)
        self.play_button.clicked.connect(self.start_game)
        self.exit_button.clicked.connect(self.emit_exit_signal)


    def emit_exit_signal(self):
        """Emit signal to main window to close the app."""
        self.exit_game_signal.emit()

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
        self.start_game_signal.emit(self.selected_rounds)





