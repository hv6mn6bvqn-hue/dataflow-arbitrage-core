import json
from pathlib import Path
from datetime import datetime

EXPORTS_DIR = Path("core/exports/strong_signals")

INTERNAL_FEED_DIR = Path("core/exports/feed/v1")
PUBLIC_FEED_DIR = Path("feed/v1")

def load_signals():
    signals = []

    if not EXPORTS_DIR.exists():
        return signals

    for file in EXPORTS_DIR.glob("*.json"):
        try:
            data = json.loads(file.read_text())
            if data.get("tier") in ("strong", "critical"):
                signals.append(data)
        except Exception:
            continue

    return signals

def build_feed(signals):
    feed = {
        "feed_version": "v1",
        "schema_version": "1.0",
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "signal_count": len(signals),
        "signals": signals
    }

    INTERNAL_FEED_DIR.mkdir(parents=True, exist_ok=True)
    PUBLIC_FEED_DIR.mkdir(parents=True, exist_ok=True)

    content = json.dumps(feed, indent=2)

    (INTERNAL_FEED_DIR / "index.json").write_text(content)
    (PUBLIC_FEED_DIR / "index.json").write_text(content)

def main():
    signals = load_signals()
    build_feed(signals)

if __name__ == "__main__":
    main()
