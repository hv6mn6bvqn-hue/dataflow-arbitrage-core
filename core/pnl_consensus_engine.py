# core/pnl_consensus_engine.py
import json
import os

INPUT_FILE = "sources/pnl_tracked.json"
OUTPUT_FILE = "sources/pnl_consensus.json"

def run():
    if not os.path.exists(INPUT_FILE):
        print("[PNL_CONSENSUS] input missing")
        data = {"divergence": 0}
    else:
        with open(INPUT_FILE) as f:
            signals = json.load(f)
        # Консенсус = сумма PnL всех сигналов
        total_pnl = sum(s.get("pnl", 0) for s in signals)
        data = {"divergence": 0, "total_pnl": total_pnl}

    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f)

    print(f"[PNL_CONSENSUS] divergence: {data.get('divergence')}")

if __name__ == "__main__":
    print("[PNL_CONSENSUS] start")
    run()