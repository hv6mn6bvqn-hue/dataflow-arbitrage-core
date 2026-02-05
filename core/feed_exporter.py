from pathlib import Path
import json
import shutil
from datetime import datetime

SOURCE_DIR = Path("core/exports/strong_signals")
FEED_DIR = Path("feed/strong_signals")
INDEX_FILE = Path("feed/index.json")


def export_feed():
    if not SOURCE_DIR.exists():
        return

    FEED_DIR.mkdir(parents=True, exist_ok=True)

    exported = []

    for file in SOURCE_DIR.glob("*.json"):
        target = FEED_DIR / file.name
        shutil.copyfile(file, target)

        data = json.loads(file.read_text())
        exported.append({
            "file": file.name,
            "signal_type": data.get("signal_type"),
            "confidence": data.get("confidence")
        })

    index = {
        "updated_at": datetime.utcnow().isoformat() + "Z",
        "count": len(exported),
        "signals": exported[-20:]
    }

    INDEX_FILE.parent.mkdir(parents=True, exist_ok=True)
    INDEX_FILE.write_text(json.dumps(index, indent=2))


if __name__ == "__main__":
    export_feed()
