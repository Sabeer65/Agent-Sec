from src.agents.attacker import generate_attack


def test_generate_attack_returns_a_string():
    """The Attacker should always return plain text, never None or another type."""
    result = generate_attack(
        system_prompt="You are a helpful assistant.",
        attempt_history=[]
    )
    assert isinstance(result, str)
    assert len(result) > 0