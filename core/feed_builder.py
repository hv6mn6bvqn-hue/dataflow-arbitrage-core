import json
import sys
from pathlib import Path
from datetime import datetime

BASE_OUTPUT = Path("docs/feed")
LOG = Path("core/logs/signal.log")

STRONG_THRESHOLD = 0.7

def parse_signals():
    if not LOG.exists():
        return [], []

    blocks = LOG.read_text().split("---")
    all_signals = []
    strong_signals = []

    for b in blocks:
        if "confidence:" not in b:
            continue

        try:
            conf = float(b.split("confidence:")[1].splitlines()[0].strip())
            signal = {
                "timestamp": b.split("timestamp:")[1].splitlines()[0].strip(),
                "type": b.split("signal_type:")[1].splitlines()[0].strip(),
                "confidence": conf,
                "source": "dataflow"
            }

            all_signals.append(signal)
            if conf >= STRONG_THRESHOLD:
                strong_signals.append(signal)

        except Exception:
            continue

    return all_signals, strong_signals

def write_feed(path, signals):
    payload = {
        "feed_version": "v1",
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "signal_count": len(signals),
        "signals": signals
    }
    path.write_text(json.dumps(payload, indent=2))

def main():
    BASE_OUTPUT.mkdir(parents=True, exist_ok=True)

    all_signals, strong_signals = parse_signals()

    write_feed(BASE_OUTPUT / "index.json", all_signals)
    write_feed(BASE_OUTPUT / "strong.json", strong_signals)

if __name__ == "__main__":
    main()
