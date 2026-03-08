import json
from pathlib import Path
from datetime import datetime

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

    signals = []

    for connector in connectors:

        if hasattr(connector, "fetch"):

            data = connector.fetch()

            print(f"[DISCOVERY] {connector.__name__} → {len(data)} prices")

            signals.extend(data)

    print(f"[DISCOVERY V2] raw signals: {len(signals)}")

    if not signals:
        return

    feed = load_feed()

    feed["signals"].extend(signals)

    feed["signal_count"] = len(feed["signals"])

    feed["generated_at"] = datetime.utcnow().isoformat() + "Z"

    save_feed(feed)

    print(f"[DISCOVERY V2] signals added: {len(signals)}")


if __name__ == "__main__":
    main()