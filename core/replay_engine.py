import json
from pathlib import Path

from core.signal_policy import evaluate_signal

EVENTS_PATH = Path("core/events/events.jsonl")


def load_events():
    if not EVENTS_PATH.exists():
        raise FileNotFoundError("No events history found")

    with EVENTS_PATH.open("r", encoding="utf-8") as f:
        for line in f:
            yield json.loads(line)


def replay(decision_filter=None):
    results = []

    for event in load_events():
        if event["type"] != "signal_loaded":
            continue

        signal = event["payload"]
        decision = evaluate_signal(signal)

        if decision_filter and not decision_filter(decision):
            continue

        results.append({
            "signal_timestamp": signal.get("timestamp"),
            "confidence": decision["confidence"],
            "action": decision["action"],
            "allow": decision["allow"],
            "note": decision["note"]
        })

    return results


if __name__ == "__main__":
    output = replay()
    print(json.dumps(output, indent=2))