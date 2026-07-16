from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE = Path(__file__).resolve().parents[2] / ".env"

class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    #app
    app_name: str = "Iron-Hat"
    debug: bool = False

    #db
    database_url: str

    #auth
    secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

config = Config()