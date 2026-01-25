# tests/test_mock_llm.py
import json
from llm.factory import get_llm

#test for market schema

def test_mock_llm_market_output_schema():
    llm = get_llm()

    output = llm.generate(
        system="MARKET",
        user="{}"
    )

    data = json.loads(output)

    assert "status" in data
    assert data["status"] in {"PASS", "KILL"}

# test for business schema

def test_mock_llm_business_output_schema():
    llm = get_llm()

    output = llm.generate(
        system="BUSINESS",
        user="{}"
    )

    data = json.loads(output)

    assert "status" in data
    assert data["status"] in {"PASS", "KILL"}


# test for technical schema

def test_mock_llm_technical_output_schema():
    llm = get_llm()

    output = llm.generate(
        system="TECHNICAL",
        user="{}"
    )

    data = json.loads(output)

    assert "status" in data
    assert data["status"] in {"PASS", "KILL"}
