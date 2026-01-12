import json
import logging
import pathlib
import sys
import signal
from datetime import datetime

#lai izmantotu lietotāja definētos motīvus un paletes
from src.widgets.theme_widget.widget_theme_dialog import apply_saved_theme
from src.helpers.palette import apply_palette

#nodrošina, lai src modulis būtu pieejams / to varētu atrast
BASE_DIR = pathlib.Path(__file__).resolve().parent #te atrodas src
SRC_DIR = BASE_DIR / "src"
sys.path.append(str(SRC_DIR))

from PyQt6.QtWidgets import QApplication
from src.widgets.mainwindow_widget.mainwindow import MainWindow

#iestata logging saglabāšanas vietu un formātu, sagatavo logus visai spēlei
def setup_logging():
    logs_dir = SRC_DIR / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    log_file = logs_dir / f"session-{timestamp}.log"

    #iestata, kā raksta logus un kur tos saglabā
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
    )
    logging.getLogger(__name__).info("Logging initialized. Log file: %s", log_file)

#palaiž spēli un ieslēdz logus
def main():
    setup_logging()
    logger = logging.getLogger()

    #lai palaistu Qt lietotni un pielietotu theme
    app = QApplication(sys.argv)
    apply_saved_theme()

    #nodrošina, ka Ctrl+C terminālī pareizi aizver lietotni un izveido, parāda galveno logu
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    window = MainWindow()
    window.show()

    #ziņo, ka lietotne ir palaista un darbojas līdz logs tiek aizvērts
    logging.getLogger(__name__).info("RootRoulette app started")
    sys.exit(app.exec())

#funkcija tiek izsaukta tikai tad, ja fails tiek palaists kā pats galvenais
if __name__ == "__main__":
    main()
