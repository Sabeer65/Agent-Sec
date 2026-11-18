"""Shared, lazily created Groq client."""

from functools import lru_cache

from groq import Groq

from src.core.config import get_settings


@lru_cache
def get_groq_client() -> Groq:
    """Create the Groq client on first use (not at import) and reuse it."""
    return Groq(api_key=get_settings().groq_api_key.get_secret_value())