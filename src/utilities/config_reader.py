"""
Features:
    - Loads the default config: config.yaml
    - Loads environment-specific configs: dev.yaml. staging.yaml. prod.yaml
    - Overrides evironment via CLI: pytest --env=staging
    - Merges configs (environment overrides base)
    - Caches config (reads files only once)
"""
import os
import yaml
import sys
from functools import lru_cache

from src.utilities.logger import get_logger

logger = get_logger(__name__)


class ConfigReader:
    BASE_CONFIG = "src/configs/config.yaml"
    ENV_CONFIG_FOLDER = "src/configs/"

    def __init__(self):
        self.env = self._get_env()
        logger.info("ConfigReader initialized (env=%s)", self.env)

    @staticmethod
    def _get_env() -> str:
        if "--env" in sys.argv:
            idx = sys.argv.index("--env") + 1
            if idx < len(sys.argv):
                return sys.argv[idx].lower()

        env_var = os.environ.get("TEST_ENV")
        if env_var:
            return env_var.lower()

        return "dev"

    @lru_cache(maxsize=1)
    def get_config(self) -> dict:
        logger.info("Loading base config: %s", self.BASE_CONFIG)
        base_cfg = self._load_yaml(self.BASE_CONFIG)

        env_cfg_path = os.path.join(self.ENV_CONFIG_FOLDER, f"{self.env}.yaml")

        if os.path.exists(env_cfg_path):
            logger.info("Loading env override config: %s", env_cfg_path)
            env_cfg = self._load_yaml(env_cfg_path)
            merged = self._merge_dicts(base_cfg, env_cfg)
        else:
            logger.warning("Environment config %s not found. Using base config only.", env_cfg_path)
            merged = base_cfg

        logger.info("Final merged config: %s", merged)
        return merged

    @staticmethod
    def _load_yaml(path: str) -> dict:
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}

    @staticmethod
    def _merge_dicts(base: dict, override: dict) -> dict:
        result = base.copy()
        for key, value in override.items():
            if isinstance(value, dict) and key in result:
                result[key] = ConfigReader._merge_dicts(result[key], value)
            else:
                result[key] = value
        return result