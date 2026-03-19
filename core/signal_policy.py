# core/signal_policy.py
import json
import os

INPUT_FILE = "sources/analyzed_signals.json"
OUTPUT_FILE = "sources/policy_decision.json"

def run():
    if not os.path.exists(INPUT_FILE):
        signals = []
        print("[POLICY] input missing")
    else:
        with open(INPUT_FILE) as f:
            signals = json.load(f)

    for s in signals:
        # Простая политика: WAIT если confidence < 0.6
        s["action"] = "WAIT" if s["confidence"] < 0.6 else "EXECUTE"

    with open(OUTPUT_FILE, "w") as f:
        json.dump(signals, f)

    print(f"[POLICY] decisions evaluated: {len(signals)}")

if __name__ == "__main__":
    print("[POLICY] evaluating signal")
    run()