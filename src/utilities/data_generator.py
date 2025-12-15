import random
import string
from datetime import datetime


class DataGenerator:
    """
    Utility class for generating unique test data
    """

    @staticmethod
    def random_string(length: int = 8) -> str:
        return "".join(random.choices(string.ascii_lowercase, k=length))

    @staticmethod
    def unique_username(prefix: str = "user") -> str:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"{prefix}_{timestamp}"

    @staticmethod
    def unique_email(prefix: str = "test") -> str:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        rand = DataGenerator.random_string(4)
        return f"{prefix}_{timestamp}_{rand}@example.com"