import json
import logging
import pathlib
from PyQt6 import uic
from PyQt6.QtCore import QSettings
from PyQt6.QtWidgets import QMainWindow, QDialog, QApplication, QStackedWidget
from src.helpers.palette import dump_palette

logger = logging.getLogger(__name__)

from src.widgets.start_widget.start_widget import StartWidget
from src.widgets.game_widget.game_widget import GameWidget
from src.widgets.end_widget.end_widget import EndWidget
from src.widgets.theme_widget.widget_theme_dialog import ThemeDialogWidget , apply_saved_theme

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RootRoulette")

        ui_path = pathlib.Path(__file__).parent / "Mainwindow.ui"
        uic.loadUi(ui_path, self)

        logger.info("MainWindow UI loaded from %s", ui_path)
        self.settings = QSettings("RootRoulette", "RootRouletteApp")
        self.setup_ui()
        self.setup_connections()

        menu_bar = self.menubar
        font = menu_bar.font()
        font.setPointSize(16)
        menu_bar.setFont(font)

    def setup_ui(self):
        self.actionChoose_a_theme.triggered.connect(self.open_theme_dialog)
        
        self.stacked_widget = QStackedWidget()
        self.main_layout.addWidget(self.stacked_widget)
        
        self.show_start_widget()

    def open_theme_dialog(self):
        theme_dialog = ThemeDialogWidget(self)
        if theme_dialog.exec():
            apply_saved_theme()


    def setup_connections(self):
        pass
    
    def setup_navigation(self):
        self.start_widget = None
        self.game_widget = None
        self.end_widget = None
    
    def show_start_widget(self):
        logger.info("Showing start widget")
        last_result = self.get_last_result()
        self.start_widget = StartWidget(last_result=last_result)
        self.start_widget.start_game_signal.connect(self.show_game_widget)
        self.start_widget.exit_game_signal.connect(self.close)
        self.clear_stacked_widget()
        self.stacked_widget.addWidget(self.start_widget)
        self.stacked_widget.setCurrentWidget(self.start_widget)
    
    def show_game_widget(self, rounds):
        logger.info("Showing game widget with %s rounds", rounds)
        
        self.game_widget = GameWidget(rounds)
        self.game_widget.game_finished_signal.connect(self.show_end_widget)
        
        self.clear_stacked_widget()
        self.stacked_widget.addWidget(self.game_widget)
        self.stacked_widget.setCurrentWidget(self.game_widget)
    
    def show_end_widget(self, score, max_score, correct_words: list, incorrect_words: list):
        logger.info("Showing end widget with score %s/%s", score, max_score)
        self.settings.setValue("last_result", json.dumps({"score": score, "max_score": max_score}))
        self.end_widget = EndWidget(score, max_score, correct_words, incorrect_words)
        self.end_widget.restart_game_signal.connect(self.show_start_widget)
        self.end_widget.exit_game_signal.connect(self.close)
        
        self.clear_stacked_widget()
        self.stacked_widget.addWidget(self.end_widget)
        self.stacked_widget.setCurrentWidget(self.end_widget)
    
    def get_last_result(self):
        val = self.settings.value("last_result", "")
        if val:
            try:
                return json.loads(val)
            except Exception:
                return None
        return None

    def clear_stacked_widget(self):
        while self.stacked_widget.count():
            widget = self.stacked_widget.widget(0)
            self.stacked_widget.removeWidget(widget)
            if widget:
                widget.deleteLater()


