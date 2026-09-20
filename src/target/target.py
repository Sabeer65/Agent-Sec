import os
import ollama

# Falls back to localhost for normal local runs; Docker overrides this via
# OLLAMA_HOST so the container can reach the host machine's Ollama instance
# (see docker-compose.yml).
ollama_host = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
client = ollama.Client(host=ollama_host)


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
    response = client.chat(
        model="qwen3:4b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]
    )
    return response["message"]["content"]