import importlib.util
from pathlib import Path

from PyQt6 import QtCore, uic
from PyQt6.QtCore import QSettings
from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtWidgets import QApplication, QDialog

THEME_FACTORIES = {
    "light": lambda: get_light_palette(),
    "system": lambda: get_system_palette(),
    "forest": lambda: get_forest_palette(),
    "bubble_gum": lambda: get_bubble_gum_palette(),
    "dark": lambda: get_dark_palette(),
}

class ThemeDialogWidget(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        subclass_file = importlib.util.find_spec(self.__class__.__module__).origin
        subclass_dir = Path(subclass_file).parent
        ui_path = subclass_dir / "ThemeDialogWidget.ui"

        if not ui_path.exists():
            raise FileNotFoundError(f"UI file not found: {ui_path}")
        uic.loadUi(str(ui_path), self)

        self.bubble_radio.setStyleSheet("color: hotpink;")
        self.forest_radio.setStyleSheet("color: darkgreen;")
        self.dark_radio.setStyleSheet("color: black;")
        self.light_radio.setStyleSheet("color: silver;")
        self.system_radio.setStyleSheet("color: goldenrod;")

        self.button_box.accepted.connect(self.on_accept)
        self.restore_radio_state()

    def restore_radio_state(self):
        settings = QSettings("RootRoulette", "RootRouletteApp")
        theme = settings.value("theme", "system")

        radio_map = {
            "dark": self.dark_radio,
            "light": self.light_radio,
            "system": self.system_radio,
            "forest": self.forest_radio,
            "bubble_gum": self.bubble_radio,
        }
        if theme in radio_map:
            radio_map[theme].setChecked(True)

    def on_accept(self):
        settings = QSettings("RootRoulette", "RootRouletteApp")
        if self.dark_radio.isChecked():
            settings.setValue("theme", "dark")
        elif self.light_radio.isChecked():
            settings.setValue("theme", "light")
        elif self.system_radio.isChecked():
            settings.setValue("theme", "system")
        elif self.forest_radio.isChecked():
            settings.setValue("theme", "forest")
        elif self.bubble_radio.isChecked():
            settings.setValue("theme", "bubble_gum")
        self.accept()

def apply_saved_theme():
    settings = QSettings("RootRoulette", "RootRouletteApp")
    theme_key = settings.value("theme", "system")

    palette_factory = THEME_FACTORIES.get(theme_key, get_system_palette)
    QApplication.instance().setPalette(palette_factory())

def get_system_palette():
    return QApplication.style().standardPalette()

def get_bubble_gum_palette():
    p = QPalette()
    p.setColor(QPalette.ColorRole.Window, QColor(255, 235, 245))
    p.setColor(QPalette.ColorRole.Base, QColor(245, 250, 255))
    p.setColor(QPalette.ColorRole.AlternateBase, QColor(235, 225, 245))
    dark_pink = QColor(150, 0, 100)
    p.setColor(QPalette.ColorRole.WindowText, dark_pink)
    p.setColor(QPalette.ColorRole.Text, dark_pink)
    p.setColor(QPalette.ColorRole.ButtonText, dark_pink)
    p.setColor(QPalette.ColorRole.Button, QColor(255, 200, 225))
    p.setColor(QPalette.ColorRole.Highlight, QColor(180, 210, 255))
    p.setColor(QPalette.ColorRole.HighlightedText, QtCore.Qt.GlobalColor.white)
    p.setColor(QPalette.ColorRole.Dark, QColor(200, 150, 180))
    p.setColor(QPalette.ColorRole.Light, QColor(255, 245, 255))
    return p

def get_forest_palette():
    p = QPalette()
    p.setColor(QPalette.ColorRole.Window, QColor(180, 230, 180))
    p.setColor(QPalette.ColorRole.Base, QColor(210, 250, 210))
    p.setColor(QPalette.ColorRole.AlternateBase, QColor(200, 245, 200))
    dark_green = QColor(0, 50, 0)
    p.setColor(QPalette.ColorRole.WindowText, dark_green)
    p.setColor(QPalette.ColorRole.Text, dark_green)
    p.setColor(QPalette.ColorRole.ButtonText, dark_green)
    p.setColor(QPalette.ColorRole.Button, QColor(190, 240, 190))
    p.setColor(QPalette.ColorRole.Highlight, QColor(140, 210, 140))
    p.setColor(QPalette.ColorRole.HighlightedText, QtCore.Qt.GlobalColor.white)
    p.setColor(QPalette.ColorRole.Dark, QColor(120, 180, 120))
    p.setColor(QPalette.ColorRole.Light, QColor(220, 255, 220))
    return p

def get_dark_palette():
    p = QPalette()
    p.setColor(QPalette.ColorRole.Window, QColor(100, 100, 100))
    p.setColor(QPalette.ColorRole.Base, QColor(120, 120, 120))
    p.setColor(QPalette.ColorRole.AlternateBase, QColor(130, 130, 130))
    p.setColor(QPalette.ColorRole.WindowText, QtCore.Qt.GlobalColor.black)
    p.setColor(QPalette.ColorRole.Text, QtCore.Qt.GlobalColor.black)
    p.setColor(QPalette.ColorRole.ButtonText, QtCore.Qt.GlobalColor.black)
    p.setColor(QPalette.ColorRole.Button, QColor(140, 140, 140))
    p.setColor(QPalette.ColorRole.Highlight, QColor(150, 180, 220))
    p.setColor(QPalette.ColorRole.HighlightedText, QtCore.Qt.GlobalColor.black)
    p.setColor(QPalette.ColorRole.Dark, QColor(80, 80, 80))
    p.setColor(QPalette.ColorRole.Light, QColor(200, 200, 200))
    return p


def get_light_palette():
    p = QPalette()
    p.setColor(QPalette.ColorRole.Window, QColor(245, 245, 245))
    p.setColor(QPalette.ColorRole.WindowText, QtCore.Qt.GlobalColor.black)
    p.setColor(QPalette.ColorRole.Base, QColor(255, 255, 255))
    p.setColor(QPalette.ColorRole.Text, QtCore.Qt.GlobalColor.black)
    p.setColor(QPalette.ColorRole.Button, QColor(230, 230, 230))
    p.setColor(QPalette.ColorRole.ButtonText, QtCore.Qt.GlobalColor.black)
    p.setColor(QPalette.ColorRole.Highlight, QColor(0, 122, 204))
    p.setColor(QPalette.ColorRole.HighlightedText, QtCore.Qt.GlobalColor.white)
    return p