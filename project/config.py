from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
import os


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    SECRET_AUTH: str
    AUTH_ACCESS_TOKEN_EXPIRE_MINUTES: int
    AUTH_ALGORITHM: str

    @property
    def database_url_asyncpg(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()

load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

SECRET_AUTH = os.environ.get("SECRET_AUTH")
AUTH_ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get("AUTH_ACCESS_TOKEN_EXPIRE_MINUTES")
AUTH_ALGORITHM = os.environ.get("AUTH_ALGORITHM")
