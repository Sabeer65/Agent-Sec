from src.core.state import GraphState


def test_graph_state_defaults():
    """A freshly created GraphState should start with sensible defaults."""
    state = GraphState(system_prompt="test prompt")

    assert state.iteration == 0
    assert state.max_iterations == 5
    assert state.attempt_history == []
    assert state.target_reply is None