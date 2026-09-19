import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.environ["GROQ_API_KEY"])

def generate_patched_prompt(current_prompt: str, attack_payload: str, vulnerability_type: str, reasoning: str) -> str:
    """
    Rewrite a compromised system prompt to defend against a specific attack.

    Args:
        current_prompt: The system prompt that was just successfully attacked.
        attack_payload: The exact input that broke it.
        vulnerability_type: The category of weakness the Evaluator identified.
        reasoning: The Evaluator's explanation of why the attack succeeded.

    Returns:
        A new, hardened system prompt as a plain string.
    """
    patch_prompt = f"""You are a prompt security engineer. The following system prompt was
successfully attacked:

CURRENT SYSTEM PROMPT:
"{current_prompt}"

ATTACK THAT SUCCEEDED: "{attack_payload}"
VULNERABILITY TYPE: {vulnerability_type}
WHY IT SUCCEEDED: {reasoning}

Rewrite the system prompt to close this specific hole. Apply these defenses:
1. Wrap any reference to user input in <user_input> XML tags so the model can distinguish
   instructions from untrusted user text.
2. Add an explicit negative constraint directly forbidding the behavior that was exploited.
3. Preserve the original bot's purpose and tone - do not change what it's supposed to help with.

Respond with ONLY the new system prompt text. No explanation, no markdown, just the prompt itself."""

    completion = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": patch_prompt}]
    )

    return completion.choices[0].message.content