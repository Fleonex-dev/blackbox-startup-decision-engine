import json
from llm.base import LLMClient

"""Deterministic mock LLM used for tests and local development.

Returns well-formed JSON aligned with the prompts' expected schema so agents
can parse without network dependency.
"""

class MockLLM(LLMClient):
    # Deterministic mock that returns fixed JSON for prompts.
    def generate(self, system: str, user: str) -> str:
        # Workflow Gate Check
        if "Gatekeeper" in system:
            # Deterministic Kills based on keywords in the brief (passed in user prompt)
            if "Tinder for Dogs" in user or "Recipe Generator" in user:
                return json.dumps({
                    "decision": "KILL",
                    "reason": "Mock Gate: Fake problem identified.",
                    "confidence": 0.9
                })
            return json.dumps({
                "decision": "PASS",
                "reason": "Mock Gate: Looks like a workflow.",
                "confidence": 0.8
            })

        if "MARKET" in system:
            # Mock Skeptic
            if "Social Network" in user:
                return json.dumps({
                    "component": "MARKET",
                    "status": "KILL",
                    "confidence": 0.9,
                    "reason": "Mock Skeptic: No specific buying power."
                })
            return json.dumps({
                "component": "MARKET",
                "status": "PASS",
                "confidence": 0.8,
                "reason": "Mock market pass"
            })

        if "BUSINESS" in system:
            if "Blockchain" in user:
                 return json.dumps({
                    "component": "BUSINESS",
                    "status": "KILL",
                    "confidence": 0.9,
                    "reason": "Mock ROI: Blockchain is not a business model."
                })
            return json.dumps({
                "component": "BUSINESS",
                "status": "PASS",
                "confidence": 0.8,
                "reason": "Mock business pass"
            })

        if "TECHNICAL" in system:
            if "Uber for Lawn" in user:
                 return json.dumps({
                    "component": "TECHNICAL",
                    "status": "KILL",
                    "confidence": 0.9,
                    "reason": "Mock Tech: Operational complexity too high."
                })
            return json.dumps({
                "component": "TECHNICAL",
                "status": "PASS",
                "confidence": 0.8,
                "reason": "Mock technical pass"
            })

        # Fallback Generator output (if needed)
        return json.dumps({
            "concept_hook": "Mock startup",
            "target_customer": "Mock customer",
            "core_pain_point": "Mock pain",
            "mechanism": "Mock mechanism",
            "monetization": "Mock monetization",
            "why_now": "Mock why now",
            "distribution_channel": "Mock distribution"
        })
