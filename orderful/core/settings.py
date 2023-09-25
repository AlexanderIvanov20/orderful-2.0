import secrets
from typing import Any

from pydantic import EmailStr, PostgresDsn, validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "OrderFul"
    REST_ROUTE: str = "/rest"

    SUPERUSER_EMAIL: EmailStr
    SUPERUSER_PASSWORD: str

    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    TOKEN_TYPE: str = "bearer"

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    SQLALCHEMY_DATABASE_URI: str | None = None
    SQLALCHEMY_TEST_DATABASE_URI: str = "sqlite://"

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_database_connection(cls, value: str | None, values: dict[str, Any]) -> str:
        if isinstance(value, str):
            return value

        return str(
            PostgresDsn.build(
                scheme="postgresql",
                username=values.get("POSTGRES_USER"),
                password=values.get("POSTGRES_PASSWORD"),
                host=values.get("POSTGRES_SERVER"),
                path=f"{values.get('POSTGRES_DB') or ''}",
            )
        )

    OFFSET: int = 0
    LIMIT: int = 100

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=True)


settings = Settings()
