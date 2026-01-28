#core/state.py
from typing import TypedDict, Optional, Dict, Any
from enum import Enum

"""State definitions used across the evaluation graph.

This module defines the canonical EngineState shape and EvalResult type that
agents and the arbiter rely on. Keep these types stable: downstream logic
assumes these keys exist (or are Optional) and that status values match the
Status enum.
"""

# Accepted evaluation outcomes.
class Status(str, Enum):
    PASS = "PASS"
    KILL = "KILL"
    INSUFFICIENT_INFO = "INSUFFICIENT_INFO"

# Evaluator result shape.
class EvalResult(TypedDict):
    component: str
    status: Status
    confidence: float
    reason: str

# Engine state passed through the graph.
class EngineState(TypedDict):
    run_id: str
    brief: Optional[Dict[str, Any]]
    workflow_gate_result: Optional[Dict[str, Any]]
    market_eval: Optional[EvalResult]
    business_eval: Optional[EvalResult]
    technical_eval: Optional[EvalResult]
    final_decision: Optional[str]
    judgment_status: Optional[Status]
