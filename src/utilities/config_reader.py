import os
from functools import lru_cache
from pathlib import Path

import yaml

from utilities.logger import get_logger

logger = get_logger(__name__)


class ConfigReader:
    """
    Handles configuration loading, environment merging, and caching.
    """
    # Use Path for cross-platform compatibility
    ROOT_DIR = Path(__file__).parent.parent.parent
    CONFIG_DIR = ROOT_DIR / "src" / "configs"
    BASE_CONFIG_PATH = CONFIG_DIR / "config.yaml"

    def __init__(self):
        # Priority: Environment Variable (set by conftest or OS) > Default 'dev'
        self.env = os.environ.get("TEST_ENV", "dev").lower()
        logger.info("ConfigReader initialized for environment: %s", self.env)

    @lru_cache(maxsize=1)
    def get_config(self) -> dict:
        """
        Loads base config and merges it with environment-specific overrides.
        """
        logger.info("Loading base configuration from: %s", self.BASE_CONFIG_PATH)
        config = self._load_yaml(self.BASE_CONFIG_PATH)

        env_file_path = self.CONFIG_DIR / f"{self.env}.yaml"

        if env_file_path.exists():
            logger.info("Merging environment overrides from: %s", env_file_path)
            env_config = self._load_yaml(env_file_path)
            config = self._merge_dicts(config, env_config)
        else:
            logger.warning("Environment file %s not found. Using base config.", env_file_path)

        return config

    @staticmethod
    def _load_yaml(path: Path) -> dict:
        """Loads a YAML file safety."""
        try:
            with open(path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            logger.error("Failed to read YAML at %s: %s", path, e)
            return {}

    @staticmethod
    def _merge_dicts(base: dict, override: dict) -> dict:
        """Recursively merges to dictionaries."""
        result = base.copy()
        for key, value in override.items():
            if isinstance(value, dict) and key in result and isinstance(result[key], dict):
                result[key] = ConfigReader._merge_dicts(result[key], value)
            else:
                result[key] = value
        return result


# Global instance for easier access
config_reader = ConfigReader()
