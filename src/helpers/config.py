from pydantic_settings import BaseSettings
from pathlib import Path
from typing import Optional

ENV_FILE = Path(__file__).parent.parent / ".env"


class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str

    FILE_ALLOWED_TYPES: list[str]
    FILE_MAX_SIZE: int
    FILE_DEFAULT_CHUNK_SIZE: int

    MONGODB_URL: str
    MONGODB_DATABASE: str

    GENERATION_BACKEND: str
    EMBEDDING_BACKEND: str

    OPENAI_API_KEY: Optional[str] = ""
    OPENAI_API_URL: Optional[str] = ""
    COHERE_API_KEY: Optional[str] = ""

    GENERATION_MODEL_ID: str
    EMBEDDING_MODEL_ID: str
    EMBEDDING_MODEL_SIZE: int

    DEFAULT_INPUT_MAX_CHARACTERS: int
    DEFAULT_OUTPUT_MAX_CHARACTERS: int
    DEFAULT_GENERATION_TEMPERATURE: float

    VECTOR_DB_BACKEND: str
    VECTOR_DB_PATH: str
    VECTOR_DB_DISTANCE_METHOD: str = "cosine"

    PRIMARY_LANGUAGE: str = "en"
    DEFAULT_LANGUAGE: str = "en"

    class Config:
        env_file = ENV_FILE


def get_settings():
    return Settings()
