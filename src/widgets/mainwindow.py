import logging
import pathlib
from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        ui_path = pathlib.Path(__file__).parent / "exampleui.ui"
        uic.loadUi(ui_path, self)

        logger.info("MainWindow UI loaded from %s", ui_path)

        # Example connections (optional)
        if hasattr(self, "pushButton_2"):
            self.pushButton_2.clicked.connect(lambda: self.handle_choice("French"))
        if hasattr(self, "pushButton_3"):
            self.pushButton_3.clicked.connect(lambda: self.handle_choice("English"))
        if hasattr(self, "pushButton_4"):
            self.pushButton_4.clicked.connect(lambda: self.handle_choice("German"))

    def handle_choice(self, language: str):
        logger.info("Button clicked: %s", language)
