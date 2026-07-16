"""
Application Configuration

This module loads all application settings from environment variables.
It acts as the single source of truth for configuration used across the project.
"""

from functools import lru_cache

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

# Load .env file
load_dotenv()


class Settings(BaseSettings):
    """Application settings."""

    # ------------------------
    # Server
    # ------------------------
    host: str = Field(default="127.0.0.1", alias="HOST")
    port: int = Field(default=8005, alias="PORT")

    # ------------------------
    # OpenAI
    # ------------------------
    openai_api_key: str = Field(alias="OPENAI_API_KEY")

    openai_model: str = Field(
        default="gpt-4o-mini",
        alias="OPENAI_MODEL",
    )

    # ------------------------
    # Embedding Model
    # ------------------------
    embedding_model: str = Field(
        default="BAAI/bge-small-en-v1.5",
        alias="EMBEDDING_MODEL",
    )

    # ------------------------
    # Vector Store
    # ------------------------
    vector_db_path: str = Field(
        default="vectorstore",
        alias="VECTOR_DB_PATH",
    )

    # ------------------------
    # Database
    # ------------------------
    database_url: str = Field(
        default="sqlite:///hotel.db",
        alias="DATABASE_URL",
    )

    class Config:
        populate_by_name = True
        extra = "ignore"


@lru_cache
def get_settings() -> Settings:
    """
    Returns a cached Settings instance.

    Using lru_cache ensures environment variables
    are loaded only once during application lifetime.
    """
    return Settings()


settings = get_settings()