import json
from llm.base import LLMClient

class MockLLM(LLMClient):
    def generate(self, system: str, user: str) -> str:
        if "MARKET" in system:
            return json.dumps({
                "component": "MARKET",
                "status": "PASS",
                "confidence": 0.8,
                "reason": "Mock market pass"
            })

        if "BUSINESS" in system:
            return json.dumps({
                "component": "BUSINESS",
                "status": "PASS",
                "confidence": 0.8,
                "reason": "Mock business pass"
            })

        if "TECHNICAL" in system:
            return json.dumps({
                "component": "TECHNICAL",
                "status": "PASS",
                "confidence": 0.8,
                "reason": "Mock technical pass"
            })

        # Generator output
        return json.dumps({
            "concept_hook": "Mock startup",
            "target_customer": "Mock customer",
            "core_pain_point": "Mock pain",
            "mechanism": "Mock mechanism",
            "monetization": "Mock monetization",
            "why_now": "Mock why now",
            "distribution_channel": "Mock distribution"
        })
