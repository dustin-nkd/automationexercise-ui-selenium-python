import random
import string
import time
from datetime import datetime


class DataGenerator:
    """
    Utility class for generating unique and realistic test data.
    """

    @staticmethod
    def random_string(length: int = 8) -> str:
        """Generates a random string of lowercase letters."""
        return "".join(random.choices(string.ascii_lowercase, k=length))

    @staticmethod
    def random_number(length: int = 10) -> str:
        """Generates a random string of numbers."""
        return "".join(random.choices(string.digits, k=length))

    @staticmethod
    def unique_username(prefix: str = "user") -> str:
        """
        Generates a unique username using high-resolution timestamp.
        Example: user_1708456789
        """
        # Use time.time_ns() for nanasecond precision to avoid collisions in parallel runs
        timestamp = str(time.time_ns())[-10:]
        return f"{prefix}_{timestamp}"

    @staticmethod
    def unique_email(domain: str = "example.com", prefix: str = "test") -> str:
        """
        Generates a unique email address.
        Example: test_20240520_143005_abcd@example.com
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        rand = DataGenerator.random_string(4)
        return f"{prefix}_{timestamp}_{rand}@{domain}"

    @staticmethod
    def generate_user_profile() -> dict:
        """
        Generate a complete mock user profile for signup tests.
        """
        first_name = DataGenerator.random_string(6).capitalize()
        last_name = DataGenerator.random_string(6).capitalize()

        return {
            "first_name": first_name,
            "last_name": last_name,
            "full_name": f"{first_name} {last_name}",
            "email": DataGenerator.unique_email(prefix=first_name.lower()),
            "password": f"Pass_{DataGenerator.random_string(5)}123!",
            "mobile": f"09{DataGenerator.random_number(8)}"
        }
