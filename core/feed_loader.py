import json
from pathlib import Path

FEED_PATH = Path("docs/feed/index.json")


def load_latest_signal():
    if not FEED_PATH.exists():
        print("[FEED] feed/index.json not found")
        return None

    data = json.loads(FEED_PATH.read_text())

    signals = data.get("signals", [])
    if not signals:
        print("[FEED] no signals in feed")
        return None

    return signals[-1]  # последний сигнал — самый свежий