# shortener_app/config.py

from pydantic import BaseSettings

class Settings(BaseSettings):
    env_name: str = "local"
    base_url: str = "http://localhost:8000"
    db_url: str = "sqlite:///./shortener.db"


def get_settings() -> Settings:
    settings = Settings()
    print(f"Loading settings for environment: {settings.env_name}")
    return settings