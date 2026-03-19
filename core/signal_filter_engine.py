# core/signal_filter_engine.py
import json

def run():
    try:
        with open("sources/spread_opportunities.json") as f:
            spreads = json.load(f)
    except Exception:
        spreads = []

    filtered = [s for s in spreads if s.get("price", 0) > 0]
    with open("sources/signals.json", "w") as f:
        json.dump(filtered, f)

    print(f"[SIGNAL] spreads loaded: {len(spreads)}")
    print(f"[SIGNAL] spreads after filter: {len(filtered)}")
    print(f"[SIGNAL] signals saved: {len(filtered)}")

if __name__ == "__main__":
    print("[SIGNAL] engine start")
    run()