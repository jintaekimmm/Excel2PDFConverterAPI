import logging
import os
import pathlib
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

log = logging.getLogger("uvicorn")
BASE_DIR = pathlib.Path(__file__).parent.parent


class Settings(BaseSettings):
    env: str = os.environ.get("ENV", "production")
    log_level: str = "INFO"


class LocalSettings(Settings):
    model_config = SettingsConfigDict(env_file=f"{BASE_DIR}/.env.local")


class DevelopmentSettings(Settings):
    model_config = SettingsConfigDict(env_file=f"{BASE_DIR}/.env.dev")


class ProductionSettings(Settings):
    model_config = SettingsConfigDict(env_file=f"{BASE_DIR}/.env")


class TestingSettings(Settings):
    model_config = SettingsConfigDict(env_file=f"{BASE_DIR}/.env.test")


@lru_cache
def get_settings() -> BaseSettings:
    settings_cls_dict = {
        "local": LocalSettings,
        "development": DevelopmentSettings,
        "production": ProductionSettings,
        "testing": TestingSettings,
    }

    env = os.environ.get("ENV", "production")
    settings_cls = settings_cls_dict[env]

    return settings_cls()


settings = get_settings()
