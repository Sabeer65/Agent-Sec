from langgraph.graph import StateGraph, END
from src.core.state import GraphState
from src.target.target import get_target_response
from src.agents.evaluator import evaluate_response
from src.agents.patcher import generate_patched_prompt
from src.agents.attacker import generate_attack
from reporter import generate_report

# ─── Nodes ───────────────────────────────────────────────
def target_node(state: GraphState) -> dict:
    reply = get_target_response(state.system_prompt, state.attack_payload)
    return {"target_reply": reply}


def evaluator_node(state: GraphState) -> dict:
    result = evaluate_response(state.system_prompt, state.attack_payload, state.target_reply)
    new_history_entry = {
        "attack_payload": state.attack_payload,
        "is_vulnerable": result.is_vulnerable,
        "vulnerability_type": result.vulnerability_type,
    }
    return {
        "is_vulnerable": result.is_vulnerable,
        "confidence_score": result.confidence_score,
        "vulnerability_type": result.vulnerability_type,
        "reasoning": result.reasoning,
        "attempt_history": state.attempt_history + [new_history_entry],
    }


def patcher_node(state: GraphState) -> dict:
    """
    Rewrite the target's system prompt in response to a confirmed vulnerability,
    and advance the retry counter.
    """
    new_prompt = generate_patched_prompt(
        state.system_prompt,
        state.attack_payload,
        state.vulnerability_type,
        state.reasoning
    )
    return {
        "system_prompt": new_prompt,
        "iteration": state.iteration + 1
    }

def attacker_node(state: GraphState) -> dict:
    """Generate the next attack attempt, informed by prior history."""
    payload = generate_attack(state.system_prompt, state.attempt_history)
    return {
        "attack_payload": payload,
        "attack_name": f"AI-Generated Attempt {state.iteration + 1}"
    }

# ─── Routing ─────────────────────────────────────────────
def route_after_evaluation(state: GraphState) -> str:
    """
    Decide what happens after the Evaluator has judged an attack.

    Returns:
        "patch" if the target is vulnerable and retries remain,
        otherwise "end".
    """
    if state.is_vulnerable and state.iteration < state.max_iterations:
        return "patch"
    return "end"


# ─── Graph Construction ──────────────────────────────────
builder = StateGraph(GraphState)

builder.add_node("attacker", attacker_node)
builder.add_node("target", target_node)
builder.add_node("evaluator", evaluator_node)
builder.add_node("patcher", patcher_node)

builder.set_entry_point("attacker")
builder.add_edge("attacker", "target")
builder.add_edge("target", "evaluator")

builder.add_conditional_edges(
    "evaluator",
    route_after_evaluation,
    {
        "patch": "patcher",
        "end": END
    }
)

builder.add_edge("patcher", "attacker")

graph = builder.compile()
