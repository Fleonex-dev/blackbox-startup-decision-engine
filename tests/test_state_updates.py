# tests/test_state_updates.py
def test_partial_state_update_does_not_override():
    original_state = {
        "run_id": "run_123",
        "brief": {"idea": "x"},
    }

    update = {
        "market_eval": {"status": "PASS"}
    }

    merged = {**original_state, **update}

    assert merged["run_id"] == "run_123"
    assert merged["market_eval"]["status"] == "PASS"
