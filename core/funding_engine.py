# core/funding_engine.py
import json

EXCHANGES = ["binance", "bybit"]

def fetch_funding(exchange):
    try:
        # заглушка на реальный API
        return {"BTCUSD": 0.0001}
    except Exception as e:
        print(f"[FUNDING] {exchange} error: {e}")
        return {}

def run():
    collected = {}
    for ex in EXCHANGES:
        data = fetch_funding(ex)
        collected[ex] = data
        if not data:
            print(f"[FUNDING] {ex} blocked or invalid")
    total = sum(len(d) for d in collected.values())
    print(f"[FUNDING] collected: {total}")
    print("[FUNDING] no data" if total == 0 else "[FUNDING] data ok")
    with open("sources/funding.json", "w") as f:
        json.dump(collected, f)

if __name__ == "__main__":
    print("[FUNDING] engine start")
    run()