from os.path import join, dirname
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str

    model_config = SettingsConfigDict(
        env_file=join(dirname(__file__), ".env"), extra="ignore"
    )


config = Settings()
