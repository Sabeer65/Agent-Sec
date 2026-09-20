from pydantic import BaseModel, Field
from typing import Optional, List, Dict


class GraphState(BaseModel):
    """
    Shared state passed between every node in the Agent-Sec graph.
    Fields start as None until the node responsible for them has run.
    """

    system_prompt: str
    attack_name: Optional[str] = None
    attack_payload: Optional[str] = None
    target_reply: Optional[str] = None
    is_vulnerable: Optional[bool] = None
    confidence_score: Optional[float] = None
    vulnerability_type: Optional[str] = None
    reasoning: Optional[str] = None

    iteration: int = 0
    max_iterations: int = 5  # hard cap on patch/retry attempts, prevents infinite loops
    attempt_history: List[Dict] = Field(default_factory=list)