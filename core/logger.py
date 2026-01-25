import json
import os
from datetime import datetime

LOD_DIR = "logs"

"""Simple file-based shadow logging.

This module writes a per-run JSON snapshot for auditing and debugging.
It is intentionally lightweight; no concurrency guarantees are provided.
"""

def write_shadow_log(state:dict):
    # Ensure logs directory exists.
    os.makedirs(LOD_DIR, exist_ok=True)

    run_id = state.get("run_id", "unknown_run")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Build snapshot payload.
    log_data = {
        "run_id": run_id,
        "timestamp": timestamp,
        "brief": state.get("brief"),
        "market_eval": state.get("market_eval"),
        "business_eval": state.get("business_eval"),
        "technical_eval": state.get("technical_eval"),
        "final_decision": state.get("final_decision")
    }

    file_path = os.path.join(LOD_DIR, f"{run_id}_{timestamp}.json")

    # Write JSON file. If atomicity is needed, write to a temp file then os.replace.
    with open(file_path, "w") as f:
        json.dump(log_data, f, indent=2)
