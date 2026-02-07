from datetime import datetime


def execute(action, confidence, note, dry_run=True):
    payload = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "action": action,
        "confidence": confidence,
        "note": note,
        "dry_run": dry_run
    }

    if dry_run:
        print("[DRY-RUN] Execution skipped:", payload)
        return payload

    # future: real execution hook
    print("[EXECUTE]", payload)
    return payload
