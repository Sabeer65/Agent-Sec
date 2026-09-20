import os
import ollama

ollama_host = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
client = ollama.Client(host=ollama_host)

def get_target_response(system_prompt: str, user_input: str) -> str:
    response = client.chat(
        model="qwen3:4b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]
    )
    return response["message"]["content"]