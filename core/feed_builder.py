import json
import sys
from pathlib import Path
from datetime import datetime

OUTPUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("docs/feed/index.json")
LOG = Path("core/logs/signal.log")

def parse_signals():
    if not LOG.exists():
        return []

    blocks = LOG.read_text().split("---")
    signals = []

    for b in blocks:
        if "confidence:" not in b:
            continue

        conf = float(b.split("confidence:")[1].splitlines()[0].strip())
        if conf < 0.35:
            continue

        signals.append({
            "timestamp": b.split("timestamp:")[1].splitlines()[0].strip(),
            "confidence": conf,
            "type": b.split("signal_type:")[1].splitlines()[0].strip(),
            "source": "dataflow"
        })

    return signals

def main():
    signals = parse_signals()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "feed_version": "v1",
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "signal_count": len(signals),
        "signals": signals
    }

    OUTPUT.write_text(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()
