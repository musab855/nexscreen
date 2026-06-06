from pydantic_settings import BaseSettings # type: ignore
from functools import lru_cache


class Settings(BaseSettings):
    gemini_api_key: str
    database_url: str
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    chroma_persist_dir: str = "./chroma_db"
    app_env: str = "development"
    log_level: str = "INFO"
    max_upload_size_mb: int = 5
    questions_per_session: int = 5

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()