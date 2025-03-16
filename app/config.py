from pydantic_settings import BaseSettings
from pydantic import Field, computed_field


class Settings(BaseSettings):
    DB_HOST: str = Field(..., description="Database host")
    DB_PORT: int = Field(..., description="Database port")
    DB_USER: str = Field(..., description="Database user")
    DB_PASS: str = Field(..., description="Database password")
    DB_NAME: str = Field(..., description="Database name")

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    SECRET_KEY: str
    ALGORITHM: str

    REDIS_HOST: str = Field(..., description="Redis host")
    REDIS_PORT: int = Field(..., description="Redis port")

    SMTP_HOST: str = Field(..., description="SMTP host")
    SMTP_PORT: int = Field(..., description="SMTP port")
    SMTP_USER: str = Field(..., description="SMTP user")
    SMTP_PASS: str = Field(..., description="SMTP password")

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }


settings = Settings()
