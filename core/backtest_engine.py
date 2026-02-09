from datetime import datetime
from pathlib import Path
import json

from core.signal_policy import evaluate_signal

FEED_PATH = Path("docs/feed/index.json")
OUTPUT_PATH = Path("docs/backtest/index.json")


def load_signals():
    if not FEED_PATH.exists():
        raise FileNotFoundError("Feed not found for backtest")

    data = json.loads(FEED_PATH.read_text())
    return data.get("signals", [])


def run_backtest():
    signals = load_signals()
    results = []

    for signal in signals:
        decision = evaluate_signal(signal)

        results.append({
            "signal_timestamp": signal.get("timestamp"),
            "signal_type": signal.get("type"),
            "confidence": signal.get("confidence"),
            "decision": decision,
        })

    return {
        "engine_version": "v1.0.0",
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "signal_count": len(signals),
        "results": results,
    }


def main():
    report = run_backtest()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(report, indent=2))
    print("[BACKTEST] completed")


if __name__ == "__main__":
    main()