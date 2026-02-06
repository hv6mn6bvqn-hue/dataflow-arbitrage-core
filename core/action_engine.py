from pathlib import Path
from datetime import datetime
import json

OUTPUT_PATH = Path("public/actions/index.json")

def main():
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    actions = [
        {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "action": "monitor",
            "confidence": 0.75,
            "source": "action_engine"
        }
    ]

    payload = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "action_count": len(actions),
        "actions": actions
    }

    OUTPUT_PATH.write_text(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()
