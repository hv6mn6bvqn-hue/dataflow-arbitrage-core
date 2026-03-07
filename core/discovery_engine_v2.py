from pathlib import Path
from datetime import datetime
import json

from core.connector_loader import load_connectors

FEED_PATH = Path("docs/feed/index.json")


def load_feed():

    if not FEED_PATH.exists():
        return {
            "feed_version": "v2",
            "generated_at": "",
            "signal_count": 0,
            "signals": []
        }

    return json.loads(FEED_PATH.read_text())


def save_feed(feed):

    FEED_PATH.parent.mkdir(parents=True, exist_ok=True)
    FEED_PATH.write_text(json.dumps(feed, indent=2))


def main():

    print("[DISCOVERY V2] loading connectors")

    connectors = load_connectors()

    print(f"[DISCOVERY V2] connectors loaded: {len(connectors)}")

    feed = load_feed()

    total_signals = 0

    for connector in connectors:

        try:
            signals = connector.fetch_signals()

            for s in signals:
                feed["signals"].append(s)

            total_signals += len(signals)

        except Exception as e:
            print(f"[DISCOVERY V2] connector error: {e}")

    feed["signal_count"] = len(feed["signals"])
    feed["generated_at"] = datetime.utcnow().isoformat() + "Z"

    save_feed(feed)

    print(f"[DISCOVERY V2] signals added: {total_signals}")


if __name__ == "__main__":
    main()