from typing import Optional
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Environment
    ENVIRONMENT: str
    DEBUG: bool = True

    # Application
    PROJECT_NAME: str = "Reals API"
    API_V1_STR: str = "/api/v1"

    # Database
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str = "reals"

    # Database Pool Settings
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10
    DB_POOL_TIMEOUT: int = 30
    DB_POOL_RECYCLE: int = 1800  # 30 minutes
    DB_ECHO_LOG: bool = True

    # Migration Settings
    MIGRATIONS_DIR: str = "migrations"
    ALEMBIC_CONFIG: str = "alembic.ini"

    # OpenAI Settings
    OPENAI_API_KEY: str
    OPENAI_MODEL: str
    GPT_API_URL: str = "https://api.openai.com/v1/chat/completions"
    ORGANIZATION_ID: str
    PROJECT_ID: str

    @property
    def DATABASE_URL(self) -> str:
        """Get database URL based on environment"""
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    @property
    def SYNC_DATABASE_URL(self) -> str:
        """Get synchronous database URL for migrations"""
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()


settings = get_settings()
