#core/state.py
from typing import TypedDict, Optional, Dict, Any

class EvalResult(TypedDict):
    component: str
    status: str
    confidence: float
    reason: str


class EngineState(TypedDict):
    run_id: str

    brief:Optional[Dict[str, Any]]

    market_eval: Optional[EvalResult]
    business_eval: Optional[EvalResult]
    technical_eval: Optional[EvalResult]

    final_decision: Optional[str]
    