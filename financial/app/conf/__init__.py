from pydantic import BaseSettings

from typing import Union, List

from decouple import config


class CommonSettings(BaseSettings):
    APP_NAME: str = config("APP_NAME", default="Financeiro API")
    DEBUG_MODE: bool = config("DEBUG_MODE", cast=bool, default=False)
    VERSION: str = config("VERSION", default="test")


class ServerSettings(BaseSettings):
    HOST: str = config("HOST", default="0.0.0.0")
    PORT: int = config("PORT", default="8081", cast=int)
    ORIGINS: Union[str, List[str]] = config(
        "ORIGINS", cast=lambda v: [c.strip() for c in v.split("|")]
    )


class DatabaseSettings(BaseSettings):
    DB_URL: str = config("DB_URL")
    DB_NAME: str = config("DB_NAME")


class Settings(CommonSettings, ServerSettings, DatabaseSettings):
    pass

settings = Settings()
