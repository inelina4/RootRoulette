import importlib.util
from pathlib import Path

from PyQt6 import QtCore, uic
from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtWidgets import QApplication, QDialog


class ThemeDialogWidget(QDialog):
    def __init__(self, presets=None, parent=None):
        super().__init__(parent)

        subclass_file = importlib.util.find_spec(self.__class__.__module__).origin
        subclass_dir = Path(subclass_file).parent
        ui_path = (
            subclass_dir / "ThemeDialogWidget.ui"
        )

        if not ui_path.exists():
            raise FileNotFoundError(f"UI file not found: {ui_path}")
        uic.loadUi(str(ui_path), self)

        self.button_box.accepted.connect(self.on_accept)

    def on_accept(self):
        self.accept()

    def get_selected_theme(self):
        if self.very_dark_radio.isChecked():
            return get_very_dark_palette()
        elif self.dark_radio.isChecked():
            return get_dark_palette()
        elif self.system_radio.isChecked():
            return get_system_palette()
        elif self.light_radio.isChecked():
            return get_light_palette()
        elif self.military_green_radio.isChecked():
            return get_military_green_palette()
        return None


def get_system_palette():
    return QApplication.style().standardPalette()


def get_military_green_palette():
    military_green = QPalette()

    # Base UI colors
    military_green.setColor(
        QPalette.ColorRole.Window, QColor(40, 60, 40)
    )  # Dark olive green
    military_green.setColor(QPalette.ColorRole.WindowText, QtCore.Qt.GlobalColor.white)
    military_green.setColor(QPalette.ColorRole.Base, QColor(35, 50, 35))  # Deep green
    military_green.setColor(
        QPalette.ColorRole.AlternateBase, QColor(45, 65, 45)
    )  # Olive variation
    military_green.setColor(QPalette.ColorRole.ToolTipBase, QColor(35, 50, 35))
    military_green.setColor(QPalette.ColorRole.ToolTipText, QtCore.Qt.GlobalColor.white)
    military_green.setColor(QPalette.ColorRole.Text, QtCore.Qt.GlobalColor.white)

    # Buttons & Highlights
    military_green.setColor(QPalette.ColorRole.Button, QColor(50, 70, 50))  # Army green
    military_green.setColor(QPalette.ColorRole.ButtonText, QtCore.Qt.GlobalColor.white)
    military_green.setColor(QPalette.ColorRole.BrightText, QtCore.Qt.GlobalColor.red)
    military_green.setColor(QPalette.ColorRole.Link, QColor(90, 130, 80))  # Faded green
    military_green.setColor(
        QPalette.ColorRole.Highlight, QColor(80, 120, 70)
    )  # Tactical green
    military_green.setColor(
        QPalette.ColorRole.HighlightedText, QColor(190, 190, 190)
    )  # Slightly faded white

    # Shadows & Depth
    military_green.setColor(QPalette.ColorRole.Shadow, QColor(30, 45, 30))
    military_green.setColor(QPalette.ColorRole.Dark, QColor(25, 40, 25))

    # Disabled state colors
    disabled_gray = QColor(90, 90, 90)
    disabled_text = QColor(150, 150, 150)

    military_green.setColor(
        QPalette.ColorGroup.Disabled,
        QPalette.ColorRole.Button,
        QColor(80, 100, 80),  # Muted olive
    )
    military_green.setColor(
        QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, disabled_text
    )
    military_green.setColor(
        QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, disabled_text
    )
    military_green.setColor(
        QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, disabled_text
    )

    return military_green


def get_dark_palette():
    dark = QPalette()
    dark.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
    dark.setColor(QPalette.ColorRole.WindowText, QtCore.Qt.GlobalColor.white)
    dark.setColor(QPalette.ColorRole.Base, QColor(42, 42, 42))
    dark.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
    dark.setColor(QPalette.ColorRole.ToolTipBase, QColor(42, 42, 42))
    dark.setColor(QPalette.ColorRole.ToolTipText, QtCore.Qt.GlobalColor.white)
    dark.setColor(QPalette.ColorRole.Text, QtCore.Qt.GlobalColor.white)
    dark.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
    dark.setColor(QPalette.ColorRole.ButtonText, QtCore.Qt.GlobalColor.white)
    dark.setColor(QPalette.ColorRole.BrightText, QtCore.Qt.GlobalColor.red)
    dark.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
    dark.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
    dark.setColor(QPalette.ColorRole.HighlightedText, QColor(127, 127, 127))
    dark.setColor(QPalette.ColorRole.Shadow, QColor(20, 20, 20))
    dark.setColor(QPalette.ColorRole.Dark, QColor(35, 35, 35))

    # disabled state
    disabled_gray = QColor(90, 90, 90)
    disabled_text = QColor(150, 150, 150)

    dark.setColor(
        QPalette.ColorGroup.Disabled, QPalette.ColorRole.Button, disabled_gray
    )
    dark.setColor(
        QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, disabled_text
    )
    dark.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, disabled_text)
    dark.setColor(
        QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, disabled_text
    )
    return dark


def get_very_dark_palette():
    very_dark = QPalette()
    very_dark.setColor(QPalette.ColorRole.Window, QColor(15, 15, 15))
    very_dark.setColor(QPalette.ColorRole.WindowText, QtCore.Qt.GlobalColor.white)
    very_dark.setColor(QPalette.ColorRole.Base, QColor(10, 10, 10))
    very_dark.setColor(QPalette.ColorRole.AlternateBase, QColor(20, 20, 20))
    very_dark.setColor(QPalette.ColorRole.ToolTipBase, QColor(35, 35, 35))
    very_dark.setColor(QPalette.ColorRole.ToolTipText, QtCore.Qt.GlobalColor.white)
    very_dark.setColor(QPalette.ColorRole.Text, QtCore.Qt.GlobalColor.white)
    very_dark.setColor(QPalette.ColorRole.Button, QColor(25, 25, 25))
    very_dark.setColor(QPalette.ColorRole.ButtonText, QtCore.Qt.GlobalColor.white)
    very_dark.setColor(QPalette.ColorRole.BrightText, QtCore.Qt.GlobalColor.red)
    very_dark.setColor(QPalette.ColorRole.Link, QColor(100, 150, 255))
    very_dark.setColor(QPalette.ColorRole.Highlight, QColor(50, 100, 200))
    very_dark.setColor(QPalette.ColorRole.HighlightedText, QtCore.Qt.GlobalColor.white)
    very_dark.setColor(QPalette.ColorRole.Shadow, QColor(5, 5, 5))
    very_dark.setColor(QPalette.ColorRole.Dark, QColor(10, 10, 10))

    # disabled state
    disabled_gray = QColor(90, 90, 90)
    disabled_text = QColor(150, 150, 150)

    very_dark.setColor(
        QPalette.ColorGroup.Disabled, QPalette.ColorRole.Button, disabled_gray
    )
    very_dark.setColor(
        QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, disabled_text
    )
    very_dark.setColor(
        QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, disabled_text
    )
    very_dark.setColor(
        QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, disabled_text
    )
    return very_dark


def get_light_palette():
    light = QPalette()
    light.setColor(QPalette.ColorRole.Window, QColor(245, 245, 245))  # light background
    light.setColor(QPalette.ColorRole.WindowText, QtCore.Qt.GlobalColor.black)
    light.setColor(QPalette.ColorRole.Base, QColor(255, 255, 255))  # input fields
    light.setColor(QPalette.ColorRole.AlternateBase, QColor(240, 240, 240))
    light.setColor(QPalette.ColorRole.ToolTipBase, QtCore.Qt.GlobalColor.white)
    light.setColor(QPalette.ColorRole.ToolTipText, QtCore.Qt.GlobalColor.black)
    light.setColor(QPalette.ColorRole.Text, QtCore.Qt.GlobalColor.black)
    light.setColor(QPalette.ColorRole.Button, QColor(230, 230, 230))
    light.setColor(QPalette.ColorRole.ButtonText, QtCore.Qt.GlobalColor.black)
    light.setColor(QPalette.ColorRole.BrightText, QtCore.Qt.GlobalColor.red)
    light.setColor(QPalette.ColorRole.Link, QColor(0, 122, 204))
    light.setColor(QPalette.ColorRole.Highlight, QColor(0, 122, 204))
    light.setColor(QPalette.ColorRole.HighlightedText, QtCore.Qt.GlobalColor.white)
    light.setColor(QPalette.ColorRole.Shadow, QColor(160, 160, 160))
    light.setColor(QPalette.ColorRole.Dark, QColor(200, 200, 200))

    # Disabled state
    disabled_gray = QColor(210, 210, 210)
    disabled_text = QColor(150, 150, 150)

    light.setColor(
        QPalette.ColorGroup.Disabled, QPalette.ColorRole.Button, disabled_gray
    )
    light.setColor(
        QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, disabled_text
    )
    light.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, disabled_text)
    light.setColor(
        QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, disabled_text
    )
    return light
