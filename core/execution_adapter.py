from datetime import datetime

PROD_MODE = True  # ← GO LIVE


def execute(action: str, confidence: float, note: str, dry_run: bool = False):
    timestamp = datetime.utcnow().isoformat() + "Z"

    if PROD_MODE and not dry_run:
        # здесь в будущем будет реальное исполнение (trade / api / webhook)
        result = "EXECUTED"
    else:
        result = "SIMULATED"

    return {
        "timestamp": timestamp,
        "action": action,
        "confidence": confidence,
        "note": note,
        "mode": "PROD" if PROD_MODE else "DRY",
        "result": result
    }
