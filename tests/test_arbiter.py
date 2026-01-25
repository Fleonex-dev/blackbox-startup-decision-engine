# tests/test_arbiter.py
from agents.arbiter import final_arbiter


def test_all_pass_build():
    state = {
        "market_eval": {"status": "PASS"},
        "business_eval": {"status": "PASS"},
        "technical_eval": {"status": "PASS"},
    }

    result = final_arbiter(state)
    assert result["final_decision"] == "BUILD"


def test_any_kill_skip():
    state = {
        "market_eval": {"status": "KILL"},
        "business_eval": {"status": "PASS"},
        "technical_eval": {"status": "PASS"},
    }

    result = final_arbiter(state)
    assert result["final_decision"] == "KILL"
