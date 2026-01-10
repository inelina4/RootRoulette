import json
import logging
import pathlib
from PyQt6 import uic
from PyQt6.QtCore import QSettings
from PyQt6.QtWidgets import QMainWindow, QDialog, QApplication

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
        self.resize(700, 450)
        self.setMinimumSize(700, 450)
        ui_path = pathlib.Path(__file__).parent / "Mainwindow.ui"
        uic.loadUi(ui_path, self)

        logger.info("MainWindow UI loaded from %s", ui_path)
        self.settings = QSettings()
        self.setup_ui()
        self.setup_connections()

        menu_bar = self.menubar
        font = menu_bar.font()
        font.setPointSize(16)
        menu_bar.setFont(font)

    def setup_ui(self):
        # self.widget_handler = WidgetHandler()

        self.actionChoose_a_theme.triggered.connect(self.open_theme_dialog)

        # self.widget_handler
        self.active_widget = EndWidget(5, 10)
        #self.active_widget = StartWidget()
        #self.active_widget = GameWidget(15)
        self.active_widget.exit_game_signal.connect(self.close)
        self.main_layout.addWidget(self.active_widget)

    def open_theme_dialog(self):
        theme_dialog = ThemeDialogWidget(self)
        if theme_dialog.exec():
            apply_saved_theme()

    def setup_connections(self):

        pass


