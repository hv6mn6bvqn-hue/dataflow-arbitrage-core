from pathlib import Path
from datetime import datetime
import json

from core.feed_loader import load_feed
from core.signal_policy import evaluate_signal

BACKTEST_PATH = Path("docs/backtest/index.json")


def run_backtest():
    feed = load_feed()  # <-- теперь это list
    results = []

    for signal in feed:
        decision = evaluate_signal(signal)

        results.append({
            "evaluated_at": datetime.utcnow().isoformat() + "Z",
            "signal": signal,
            "decision": decision
        })

    output = {
        "engine_version": "v1.0.0",
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "total_signals": len(feed),
        "results": results
    }

    BACKTEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    BACKTEST_PATH.write_text(json.dumps(output, indent=2))


if __name__ == "__main__":
    run_backtest()