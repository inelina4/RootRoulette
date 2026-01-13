#nolasa un pielāgo Qt paleti JSON saglabāšanai un ielādei

import sys
import json

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QBrush, QColor, QPalette
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton

#ņem QColor un pārveido to HEX formātā
def dump_color(color: QColor) -> str:
    return f"#{color.rgba():08x}"

#ņem QBrush un pārveido to vārdnīcā, lai saglabātu JSON formātā
def dump_brush(brush: QBrush) -> dict:
    return {
        "color": dump_color(brush.color()),
        "style": brush.style().name,
    }

#ņem QPalette un pārveido to vārdnīcā, lai saglabātu JSON formātā
def dump_palette(palette: QPalette) -> dict:
    return {
        color_group.name: {
            color_role.name: {
                "brush": dump_brush(palette.brush(color_group, color_role)),
                "color": dump_color(palette.color(color_group, color_role)),
            }
            for color_role in list(QPalette.ColorRole)[:-1]
        }
        for color_group in [
            QPalette.ColorGroup.Active,
            QPalette.ColorGroup.Inactive,
            QPalette.ColorGroup.Disabled,
        ]
    }

#ņem vārdnīcu un pārveido to atpakaļ par QPalette
def apply_palette(palette: QPalette, d: dict):
    for color_group in [
        QPalette.ColorGroup.Active,
        QPalette.ColorGroup.Inactive,
        QPalette.ColorGroup.Disabled,
    ]:
        for color_role in list(QPalette.ColorRole)[:-1]:
            if color_group.name in d and color_role.name in d[color_group.name]:
                color = QColor(d[color_group.name][color_role.name]["color"])
                brush = QBrush(color)
                brush_style_str = d[color_group.name][color_role.name]["brush"]["style"]
                brush.setStyle(Qt.BrushStyle[brush_style_str])
                palette.setBrush(color_group, color_role, brush)
                palette.setColor(color_group, color_role, color)

#uzstāda QWidget fona krāsu, izmantojot QPalette, neietekmējot fontu vai citas lietas
def set_widget_background(widget: QWidget, color: str):
    palette = widget.palette()
    palette.setColor(QPalette.ColorRole.Window, QColor(color))
    widget.setAutoFillBackground(True)
    widget.setPalette(palette)

#uzstāda QPushButton fona krāsu, izmantojot QPalette, neizmantojot stilu lapas
def set_button_background(button: QPushButton, color: str):
    """Uzstāda QPushButton fona krāsu, izmantojot QPalette bez stilu lapām."""
    palette = button.palette()
    palette.setColor(QPalette.ColorRole.Button, QColor(color))
    button.setAutoFillBackground(True)
    button.setPalette(palette)
    button.update()

#izveido aplikāciju, pārveido tās paleti uz vārdnīcu un atpakaļ, lai pārbaudītu funkcijas
if __name__ == "__main__":
    app = QApplication(sys.argv)
    palette = app.style().standardPalette()
    d = dump_palette(palette)
    print(json.dumps(d, indent=4))
    apply_palette(palette, d)
