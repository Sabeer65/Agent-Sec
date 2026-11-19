from functools import lru_cache
import ollama
from src.core.config import get_settings

@lru_cache
def get_ollama_client() -> ollama.Client:
    """Create the Ollama client on first use (not at import) and reuse it."""
    return ollama.Client(host=get_settings().ollama_base_url)

def get_target_response(system_prompt: str, user_input: str) -> str:
    """
  Send a system prompt and user input to the local Target model and
    return its raw reply.

    Args:
        system_prompt: The target's current (possibly patched) instructions.
        user_input: The attack payload or ordinary user message to send.

    Returns:
        The target model's reply as plain text.

    """
    client = get_ollama_client()
    response = client.chat(
        model=get_settings().target_model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]
    )
    return response["message"]["content"]