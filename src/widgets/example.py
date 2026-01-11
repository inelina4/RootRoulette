#ielādē UI no Qt Designer .ui faila un izveido galveno logu
#pārbauda, vai pogas pastāv pirms signālu savienojumu pievienošanas; pieslēdz pogām klikšķus

import logging
import pathlib
from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow

#ļauj filtrēt dažāda veida ziņojumus
logger = logging.getLogger(__name__)

#galvenā loga klase
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        #ielādē UI no .ui faila
        ui_path = pathlib.Path(__file__).parent / "exampleui.ui"
        uic.loadUi(ui_path, self)

        logger.info("MainWindow UI loaded from %s", ui_path)

        #pārbauda, vai pogas pastāv, pirms pievieno signālu savienojumus
        if hasattr(self, "pushButton_2"):
            self.pushButton_2.clicked.connect(lambda: self.handle_choice("French"))
        if hasattr(self, "pushButton_3"):
            self.pushButton_3.clicked.connect(lambda: self.handle_choice("English"))
        if hasattr(self, "pushButton_4"):
            self.pushButton_4.clicked.connect(lambda: self.handle_choice("German"))

    #apstrādā pogas klikšķus
    def handle_choice(self, language: str):
        logger.info("Button clicked: %s", language)
