from datetime import datetime
from pathlib import Path
import json

from core.signal_policy import policy_allows_action

OUTPUT_PATH = Path("docs/actions/index.json")


def main():
    allowed, reason = policy_allows_action()

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    actions = []

    if allowed:
        actions.append({
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "action": "EXECUTE",
            "confidence": 0.85,
            "source": "policy_engine",
            "note": reason
        })
    else:
        actions.append({
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "action": "BLOCKED",
            "confidence": 0.0,
            "source": "policy_engine",
            "note": reason
        })

    payload = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "action_count": len(actions),
        "actions": actions
    }

    OUTPUT_PATH.write_text(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
