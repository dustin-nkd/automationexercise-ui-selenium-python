import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


# --- Color Codes for Console ---
class LogColors:
    RESET = "\033[0m"
    DEBUB = "\033[36m"  # Cyan
    INFO = "\033[32m"  # Green
    WARNING = "\033[33m"  # Yellow
    ERROR = "\033[31m"  # Red
    CRITICAL = "\033[1;31m"  # Bold Red


class ColoredFormatter(logging.Formatter):
    """Custom formatter to add colors to console logs."""
    COLORS = {
        logging.DEBUG: LogColors.DEBUB,
        logging.INFO: LogColors.INFO,
        logging.WARNING: LogColors.WARNING,
        logging.ERROR: LogColors.ERROR,
        logging.CRITICAL: LogColors.CRITICAL,
    }

    def format(self, record):
        color = self.COLORS.get(record.levelno, LogColors.RESET)
        record.levelname = f"{color}{record.levelname}{LogColors.RESET}"
        return super().format(record)


def get_logger(name: str = None) -> logging.Logger:
    """
    Initialize and return a colorized and rotating looger.
    """
    LOG_DIR = Path("logs")
    LOG_FILE = LOG_DIR / "test_run.log"

    # Ensure logs directory exists
    LOG_DIR.mkdir(exist_ok=True)

    logger = logging.getLogger(name or "framework")

    # Avoid adding multiple handlers to same logger
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    # Unified formatting
    log_fmt = "%(asctime)s [%(levelname)s] %(name)s:%(lineno)d - %(message)s"
    date_fmt = "%Y-%m-%d %H:%M:%S"

    # 1. Console Handler (with Colors)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(ColoredFormatter(fmt=log_fmt, datefmt=date_fmt))

    # 2. File Handler (Rotating, Plain Text)
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=5_000_000,  # 5MB
        backupCount=5,
        encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(ColoredFormatter(fmt=log_fmt, datefmt=date_fmt))

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    # Prevent logs from propagating to the root logger
    logger.propagate = False

    return logger
