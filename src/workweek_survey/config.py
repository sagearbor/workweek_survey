from __future__ import annotations

from pydantic import ValidationError, field_validator
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    storage_path: str
    output_format: str = "json"

    @field_validator("output_format")
    def validate_format(cls, v: str) -> str:
        lv = v.lower()
        if lv not in {"json", "yaml"}:
            raise ValueError("OUTPUT_FORMAT must be 'json' or 'yaml'")
        return lv

    class Config:
        env_prefix = ""
        env_file = ".env"


def get_settings() -> Settings:
    """Load settings from the environment."""
    try:
        return Settings()
    except ValidationError as exc:
        raise RuntimeError(f"Invalid configuration: {exc}") from exc
