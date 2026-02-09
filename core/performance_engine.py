from pathlib import Path
from datetime import datetime
import json

ENGINE_VERSION = "v1.0.0"

AUDIT_PATH = Path("docs/audit/index.json")
METRICS_PATH = Path("docs/metrics/index.json")
OUTPUT_PATH = Path("docs/performance/index.json")


def load_json(path):
    if not path.exists():
        return None
    return json.loads(path.read_text())


def run_performance_snapshot():
    audit = load_json(AUDIT_PATH) or []
    metrics = load_json(METRICS_PATH) or {}

    executions = [
        a for a in audit
        if a.get("action") == "EXECUTE"
        and a.get("execution", {}).get("result") == "EXECUTED"
    ]

    snapshot = {
        "engine_version": ENGINE_VERSION,
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "total_decisions": metrics.get("total_decisions", len(audit)),
        "executions": len(executions),
        "execution_rate": (
            len(executions) / len(audit) if audit else 0
        ),
        "avg_confidence_execute": (
            sum(e["confidence"] for e in executions) / len(executions)
            if executions else 0
        )
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(snapshot, indent=2))

    print("[PERFORMANCE] snapshot published")


if __name__ == "__main__":
    run_performance_snapshot()