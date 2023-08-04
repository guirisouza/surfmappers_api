from pathlib import Path
from tempfile import gettempdir
from typing import List

from pydantic_settings import BaseSettings

TEMP_DIR = Path(gettempdir())


class Settings(BaseSettings):
    """Application settings."""

    service_name: str = "api-happy-wedding"

    host: str = "0.0.0.0"
    port: int = "8086"

    # quantity of workers for uvicorn
    workers_count: int = 1

    # Enable uvicorn reloading
    reload: bool = True

    backend_cors_origins: List[str] = ["*"]


    class Config:
        env_file = "../.env"
        env_prefix = "API_HAPPY_WEDDING_"
        env_file_encoding = "utf-8"


settings = Settings()