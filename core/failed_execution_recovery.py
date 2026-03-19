# core/failed_execution_recovery.py
import json
import os

INPUT_FILE = "sources/fill_signals.json"
OUTPUT_FILE = "sources/recovered_signals.json"

def run():
    if not os.path.exists(INPUT_FILE):
        signals = []
        print("[RECOVERY] input missing")
    else:
        with open(INPUT_FILE) as f:
            signals = json.load(f)

    recovered = []
    for s in signals:
        if s.get("fill_prob", 0) < 1.0:
            s["retry"] = True
        recovered.append(s)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(recovered, f)

    print(f"[RECOVERY] ready: {len(recovered)}")

if __name__ == "__main__":
    print("[RECOVERY] start")
    run()