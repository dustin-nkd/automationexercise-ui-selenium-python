import os
import time


def wait_for_file_download(
        directory: str,
        filename_contains: str,
        timeout: int = 10
) -> str | None:
    end_time = time.time() + timeout
    while time.time() < end_time:
        for file in os.listdir(directory):
            if filename_contains in file:
                return os.path.join(directory, file)
            time.sleep(0.5)
    return None