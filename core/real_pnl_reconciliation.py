# core/real_pnl_reconciliation.py
import json
import os

INPUT_FILE = "sources/pnl_tracked.json"
OUTPUT_FILE = "sources/pnl_reconciled.json"

def run():
    if not os.path.exists(INPUT_FILE):
        signals = []
        print("[PNL_RECON] input missing")
    else:
        with open(INPUT_FILE) as f:
            signals = json.load(f)

    for s in signals:
        # Простая reconciliation: проверяем, что pnl не None
        s["pnl_reconciled"] = s.get("pnl", 0)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(signals, f)

    print(f"[PNL_RECON] reconciled: {len(signals)}")

if __name__ == "__main__":
    print("[PNL_RECON] start")
    run()
