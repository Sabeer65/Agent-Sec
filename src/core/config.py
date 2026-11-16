"""Central configuration for Agent-Sec, read from environment variables / .env."""

from functools import lru_cache

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # unknown names in .env are not errors
    )

    groq_api_key: SecretStr  # required; no default on purpose

    attacker_model: str = "qwen/qwen3.8-27b"
    judge_model: str = "openai/gpt-oss-120b"
    patcher_model: str = "openai/gpt-oss-120b"
    target_model: str = "qwen3:4b"
    ollama_base_url: str = "http://localhost:11434"

    max_iterations: int = Field(default=5, ge=1, le=10)
    reports_dir: str = "reports"
    log_level: str = "INFO"


@lru_cache
def get_settings() -> Settings:
    """Load settings on first use, not at import time, and reuse them after."""
    return Settings()