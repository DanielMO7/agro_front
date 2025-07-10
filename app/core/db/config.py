import os
from dotenv import load_dotenv, dotenv_values
from typing import ClassVar
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    env_values: ClassVar[dict] = dotenv_values()
    DB_USER: str = env_values.get("DB_USER")
    DB_PASSWORD: str = env_values.get("DB_PASSWORD")
    DB_HOST: str = env_values.get("DB_HOST")
    DB_PORT: int = int(env_values.get("DB_PORT", 3306))
    DB_NAME: str = env_values.get("DB_NAME")
    SECRET_JTW: str = env_values.get("SECRET_JTW")

    MAIL_USERNAME: str = env_values.get("MAIL_USERNAME")
    MAIL_PASSWORD: str = env_values.get("MAIL_PASSWORD")
    MAIL_FROM: str = env_values.get("MAIL_FROM")
    MAIL_PORT: str = env_values.get("MAIL_PORT")
    MAIL_SERVER: str = env_values.get("MAIL_SERVER")
    ADMIN_EMAIL: str = env_values.get("ADMIN_EMAIL")
    MAIL_FROM_NAME: str = "Administrador"  # ✅ Corregido

    MAIL_STARTTLS: bool = env_values.get("MAIL_STARTTLS", "true").lower() in ("true", "1")
    MAIL_SSL_TLS: bool = env_values.get("MAIL_SSL_TLS", "false").lower() in ("true", "1")
    USE_CREDENTIALS: bool = env_values.get("USE_CREDENTIALS", "true").lower() in ("true", "1")    

settings = Settings()
