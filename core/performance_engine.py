import json
from pathlib import Path
from datetime import datetime

AUDIT_PATH = Path("docs/audit/index.json")
PERFORMANCE_PATH = Path("docs/performance/index.json")

ENGINE_VERSION = "v1.0.0"


def load_audit():
    if not AUDIT_PATH.exists():
        return []
    with open(AUDIT_PATH, "r") as f:
        return json.load(f)


def compute_performance(audit):
    total = len(audit)
    executions = [a for a in audit if a.get("action") == "EXECUTE"]

    execution_count = len(executions)
    execution_rate = execution_count / total if total > 0 else 0

    avg_conf = (
        sum(a.get("confidence", 0) for a in executions) / execution_count
        if execution_count > 0
        else 0
    )

    return {
        "engine_version": ENGINE_VERSION,
        "last_updated": datetime.utcnow().isoformat() + "Z",
        "total_decisions": total,
        "executions": execution_count,
        "execution_rate": round(execution_rate, 4),
        "avg_confidence_execute": round(avg_conf, 4),
    }


def publish_performance(data):
    PERFORMANCE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(PERFORMANCE_PATH, "w") as f:
        json.dump(data, f, indent=2)


def main():
    audit = load_audit()
    performance = compute_performance(audit)
    publish_performance(performance)
    print("[PERFORMANCE] updated")


if __name__ == "__main__":
    main()