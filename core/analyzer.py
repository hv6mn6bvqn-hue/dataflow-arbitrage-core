from pathlib import Path
import json
from datetime import datetime

FEED_PATH = Path("docs/feed/index.json")
EXPORT_DIR = Path("core/exports/strong_signals")

EXPORT_DIR.mkdir(parents=True, exist_ok=True)


def load_feed():

    if not FEED_PATH.exists():
        return []

    data = json.loads(FEED_PATH.read_text())
    return data.get("signals", [])


def calculate_market_strength(signals):

    if not signals:
        return 0.1

    confidences = [s.get("confidence", 0.1) for s in signals]

    return sum(confidences) / len(confidences)


def classify_tier(conf):

    if conf >= 0.85:
        return "critical"
    if conf >= 0.65:
        return "strong"
    if conf >= 0.40:
        return "medium"

    return "weak"


def write_export(signal):

    ts = signal["timestamp"].replace(":", "").replace("-", "")
    fname = f"signal_{ts}.json"

    (EXPORT_DIR / fname).write_text(
        json.dumps(signal, indent=2)
    )


def main():

    print("[ANALYZER] loading feed")

    signals = load_feed()

    market_strength = calculate_market_strength(signals)

    tier = classify_tier(market_strength)

    signal = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "signal_type": "market_strength",
        "confidence": round(market_strength, 4),
        "tier": tier,
        "confirmed": tier in ("strong", "critical"),
        "signal_count": len(signals)
    }

    write_export(signal)

    print(f"[ANALYZER] market strength {market_strength}")


if __name__ == "__main__":
    main()