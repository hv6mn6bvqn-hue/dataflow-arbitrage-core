from pathlib import Path
from datetime import datetime
import json

AUDIT_PATH = Path("docs/audit/index.json")
PERFORMANCE_PATH = Path("docs/performance/index.json")
ENGINE_VERSION = "v1.0.0"


def load_audit():
    if not AUDIT_PATH.exists():
        return []
    return json.loads(AUDIT_PATH.read_text())


def compute_performance(audit):
    total = len(audit)
    executes = [a for a in audit if a.get("action") == "EXECUTE"]

    exec_count = len(executes)
    success = [e for e in executes if e.get("execution", {}).get("result") == "EXECUTED"]

    avg_confidence = (
        sum(e.get("confidence", 0) for e in executes) / exec_count
        if exec_count > 0 else 0
    )

    return {
        "engine_version": ENGINE_VERSION,
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "total_decisions": total,
        "executions": exec_count,
        "execution_rate": round(exec_count / total, 3) if total > 0 else 0,
        "win_rate": round(len(success) / exec_count, 3) if exec_count > 0 else 0,
        "avg_confidence_execute": round(avg_confidence, 3)
    }


def publish_performance(snapshot):
    PERFORMANCE_PATH.parent.mkdir(parents=True, exist_ok=True)
    PERFORMANCE_PATH.write_text(json.dumps(snapshot, indent=2))


def main():
    audit = load_audit()
    snapshot = compute_performance(audit)
    publish_performance(snapshot)
    print("[PERFORMANCE] snapshot published")


if __name__ == "__main__":
    main()