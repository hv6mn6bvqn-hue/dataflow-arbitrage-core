from datetime import datetime
from pathlib import Path
import json

from core.feed_loader import load_feed
from core.signal_policy import evaluate_signal

ENGINE_VERSION = "v1.0.0"
OUTPUT_PATH = Path("docs/backtest/index.json")


def run_backtest():
    feed = load_feed()
    results = []

    for signal in feed.get("signals", []):
        decision = evaluate_signal(signal)

        results.append({
            "signal_timestamp": signal["timestamp"],
            "signal_type": signal["type"],
            "confidence": signal["confidence"],
            "decision": decision
        })

    output = {
        "engine_version": ENGINE_VERSION,
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "signal_count": len(results),
        "results": results
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(output, indent=2))

    print("[BACKTEST] completed")
    print(f"[BACKTEST] signals processed: {len(results)}")


if __name__ == "__main__":
    run_backtest()