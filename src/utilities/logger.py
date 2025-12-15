"""
Features:
    - Colorized console handler
    - Rotating file handler
    - Ensures no duplicate handlers are added
    - Unified log formatting across the entire project
"""
import logging
import os
from logging.handlers import RotatingFileHandler

LOG_DIR = "logs"
LOG_FILE = "test_run.log"

# Create the logs directory if it does not exist
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)


def get_logger(name: str = None) -> logging.Logger:
    """
    Initialize and return logger
    :param name: Logger name, typically __name__
    :return: Configured logger instance with handlers attached
    """
    logger = logging.getLogger(name or "framework")

    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s:%(lineno)d - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(formatter)

    file_handler = RotatingFileHandler(
        os.path.join(LOG_DIR, LOG_FILE),
        maxBytes=5_000_000,
        backupCount=5,
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(console)
    logger.addHandler(file_handler)

    logger.propagate = False

    return logger