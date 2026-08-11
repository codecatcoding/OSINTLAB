import logging
from logging.handlers import RotatingFileHandler

from app.config.settings import AppPaths


LOG_FILE = AppPaths.LOGS / "osintlab.log"


def setup_logging() -> None:
    """Configura el logger global de la aplicacion."""

    AppPaths.LOGS.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[
            RotatingFileHandler(
                LOG_FILE,
                maxBytes=1_000_000,
                backupCount=5,
                encoding="utf-8",
            )
        ],
    )


def get_logger(name: str) -> logging.Logger:
    """Devuelve un logger nombrado."""

    return logging.getLogger(name)
