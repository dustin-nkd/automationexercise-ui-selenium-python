import os
import time
from pathlib import Path
from typing import Optional

from utilities.logger import get_logger

logger = get_logger(__name__)


def wait_for_file_download(
        directory: str,
        filename_contains: str,
        timeout: int = 15
) -> Optional[str]:
    """
    Waits for a file t appear in the directory and ensures it's fully downloaded.

    :param directory: The path to the download folder.
    :param filename_contains: Part of the filename to search for.
    :param timeout: Maximum time to wait in seconds.
    :return: The absolute path to the file if found, otherwise None.
    """
    logger.info(f"Waiting for file containing '{filename_contains}' in {directory}")
    end_time = time.time() + timeout

    # Common temporary extensions for browsers
    temp_extensions = {".crdownload", ".part", ".tmp"}

    while time.time() < end_time:
        try:
            files = os.listdir(directory)
            for file in files:
                # Check if file matches name and is NOT a temporary file
                if filename_contains in file:
                    file_path = os.path.join(directory, file)
                    extension = Path(file_path).suffix

                    if extension not in temp_extensions:
                        logger.info(f"File downloaded successfully: {file}")
                        return file_path

            # Polling interval
            time.sleep(1)
        except OSError as e:
            logger.debug(f"Error reading directory: {e}")
            time.sleep(1)

    logger.info(f"File download timeout after {timeout}s for '{filename_contains}'")
    return None


def get_file_size(file_path: str) -> int:
    """Returns the size of the file in bytes."""
    return os.path.getsize(file_path) if os.path.exists(file_path) else 0
