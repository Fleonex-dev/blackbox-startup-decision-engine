#core/state.py
from typing import TypedDict, Optional, Dict, Any
from enum import Enum
class Status(str, Enum):
    PASS = "PASS"
    KILL = "KILL"

class EvalResult(TypedDict):
    component: str
    status: Status
    confidence: float
    reason: str


class EngineState(TypedDict):
    run_id: str

    brief:Optional[Dict[str, Any]]

    market_eval: Optional[EvalResult]
    business_eval: Optional[EvalResult]
    technical_eval: Optional[EvalResult]

    final_decision: Optional[str]
