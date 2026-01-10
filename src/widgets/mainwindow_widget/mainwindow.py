import logging
import pathlib
from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow

logger = logging.getLogger(__name__)
from src.widgets.start_widget.start_widget import StartWidget
from src.widgets.game_widget.game_widget import GameWidget
from src.widgets.end_widget.end_widget import EndWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        ui_path = pathlib.Path(__file__).parent / "Mainwindow.ui"
        uic.loadUi(ui_path, self)

        logger.info("MainWindow UI loaded from %s", ui_path)

        self.setup_ui()
        self.setup_connections()

    def setup_ui(self):
        # self.widget_handler = WidgetHandler()
        # self.widget_handler
        #self.active_widget = EndWidget(5, 10)
        self.active_widget = StartWidget()
        #self.active_widget.exit_game_signal.connect(self.close)
        self.main_layout.addWidget(self.active_widget)

    def setup_connections(self):
        # self.active_view.

        pass


