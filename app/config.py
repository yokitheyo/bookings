import os
from typing import Literal
from pydantic_settings import BaseSettings
from pydantic import ConfigDict, Field, computed_field


class Settings(BaseSettings):
    MODE: Literal["DEV", "TEST", "PROD"] = "DEV"

    DB_HOST: str = Field(..., description="Database host")
    DB_PORT: int = Field(..., description="Database port")
    DB_USER: str = Field(..., description="Database user")
    DB_PASS: str = Field(..., description="Database password")
    DB_NAME: str = Field(..., description="Database name")

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    TEST_DB_HOST: str = Field(..., description="Database host")
    TEST_DB_PORT: int = Field(..., description="Database port")
    TEST_DB_USER: str = Field(..., description="Database user")
    TEST_DB_PASS: str = Field(..., description="Database password")
    TEST_DB_NAME: str = Field(..., description="Database name")

    @computed_field
    @property
    def TEST_DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.TEST_DB_USER}:{self.TEST_DB_PASS}@{self.TEST_DB_HOST}:{self.TEST_DB_PORT}/{self.TEST_DB_NAME}"

    SECRET_KEY: str
    ALGORITHM: str

    REDIS_HOST: str = Field(..., description="Redis host")
    REDIS_PORT: int = Field(..., description="Redis port")

    SMTP_HOST: str = Field(..., description="SMTP host")
    SMTP_PORT: int = Field(..., description="SMTP port")
    SMTP_USER: str = Field(..., description="SMTP user")
    SMTP_PASS: str = Field(..., description="SMTP password")

    model_config = ConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()

print(f"MODE from env: {os.getenv('MODE')}")
print(f"MODE from settings: {settings.MODE}")
