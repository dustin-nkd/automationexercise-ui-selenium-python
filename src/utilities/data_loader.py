from pathlib import Path

import yaml

from utilities.logger import get_logger

logger = get_logger(__name__)


class DataLoader:
    SRC_DIR = Path(__file__).parent.parent.resolve()
    DATA_DIR = SRC_DIR / "test_data"

    @staticmethod
    def load_yaml(file_name: str) -> dict:
        file_path = DataLoader.DATA_DIR / file_name

        logger.info(f"--- Loading data from: {file_path}")

        if not file_path.exists():
            alternative_path = DataLoader.SRC_DIR.parent / "test_data" / file_name
            if alternative_path.exists():
                file_path = alternative_path
            else:
                logger.error(f"--- File NOT FOUND at: {file_path}")
                return {}

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = yaml.safe_load(f)
                return content if content else {}
        except Exception as e:
            logger.error(f"--- Failed to parse YAML: {e}")
            return {}

    @classmethod
    def get_user_data(cls) -> dict:
        return cls.load_yaml("user_data.yaml")
