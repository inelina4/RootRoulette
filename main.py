import logging
import pathlib
import sys
from datetime import datetime

# Ensure src is importable
BASE_DIR = pathlib.Path(__file__).resolve().parent
SRC_DIR = BASE_DIR / "src"
sys.path.append(str(SRC_DIR))

from PyQt6.QtWidgets import QApplication
from src.widgets.mainwindow import MainWindow


def setup_logging():
    logs_dir = SRC_DIR / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    log_file = logs_dir / f"session-{timestamp}.log"

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
    )

    logging.getLogger(__name__).info("Logging initialized. Log file: %s", log_file)


def main():
    setup_logging()

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    logging.getLogger(__name__).info("RootRoulette app started")
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
