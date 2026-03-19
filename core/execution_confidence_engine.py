# core/execution_confidence_engine.py
import json
import os

INPUT_FILE = "sources/pnl_tracked.json"
OUTPUT_FILE = "sources/execution_confidence.json"

def run():
    if not os.path.exists(INPUT_FILE):
        signals = []
        print("[EXEC_CONFIDENCE] input missing")
    else:
        with open(INPUT_FILE) as f:
            signals = json.load(f)

    for s in signals:
        # Простая модель confidence: 0.8 если PnL > 0, иначе 0.5
        s["confidence"] = 0.8 if s.get("pnl", 0) > 0 else 0.5

    with open(OUTPUT_FILE, "w") as f:
        json.dump(signals, f)

    print(f"[EXEC_CONFIDENCE] scored: {len(signals)}")

if __name__ == "__main__":
    print("[EXEC_CONFIDENCE] start")
    run()