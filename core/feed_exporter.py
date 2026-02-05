from pathlib import Path
import json

STRONG_SIGNALS_DIR = Path("core/exports/strong_signals")
FEED_DIR = Path("core/exports/feed")
FEED_STRONG_DIR = FEED_DIR / "strong_signals"

FEED_STRONG_DIR.mkdir(parents=True, exist_ok=True)


def build_feed():
    feed_index = []

    for signal_file in sorted(STRONG_SIGNALS_DIR.glob("signal_*.json")):
        signal = json.loads(signal_file.read_text())

        public_signal = {
            "timestamp": signal["timestamp"],
            "signal_type": signal["signal_type"],
            "confidence": signal["confidence"],
            "confirmed": signal.get("confirmed", False)
        }

        target = FEED_STRONG_DIR / signal_file.name
        target.write_text(json.dumps(public_signal, indent=2))

        feed_index.append({
            "file": f"strong_signals/{signal_file.name}",
            "timestamp": signal["timestamp"],
            "confidence": signal["confidence"]
        })

    index_path = FEED_DIR / "index.json"
    index_path.write_text(json.dumps({
        "version": "1.0",
        "signal_count": len(feed_index),
        "signals": feed_index[-20:]
    }, indent=2))


if __name__ == "__main__":
    build_feed()
