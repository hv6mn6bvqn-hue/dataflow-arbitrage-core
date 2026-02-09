import json
from pathlib import Path
from datetime import datetime

AUDIT_PATH = Path("docs/audit/index.json")
METRICS_PATH = Path("docs/metrics/index.json")

ENGINE_VERSION = "v1.0.0"


def load_audit():
    if not AUDIT_PATH.exists():
        return []
    return json.loads(AUDIT_PATH.read_text())


def calculate_metrics(audit):
    total = len(audit)
    executed = sum(1 for a in audit if a.get("action") == "EXECUTE")

    avg_confidence = (
        round(sum(a.get("confidence", 0) for a in audit) / total, 4)
        if total > 0 else 0
    )

    return {
        "engine_version": ENGINE_VERSION,
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "total_actions": total,
        "executed_actions": executed,
        "execution_rate": round(executed / total, 4) if total > 0 else 0,
        "avg_confidence": avg_confidence,
    }


def publish_metrics(metrics):
    METRICS_PATH.parent.mkdir(parents=True, exist_ok=True)
    METRICS_PATH.write_text(json.dumps(metrics, indent=2))


def main():
    audit = load_audit()
    metrics = calculate_metrics(audit)
    publish_metrics(metrics)
    print("[METRICS] published")


if __name__ == "__main__":
    main()