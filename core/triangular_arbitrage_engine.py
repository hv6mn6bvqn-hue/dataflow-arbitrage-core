# core/triangular_arbitrage_engine.py
import json
import os

INPUT_FILE = "sources/orderbook_signals.json"
OUTPUT_FILE = "sources/triangular_opportunities.json"

def run():
    if not os.path.exists(INPUT_FILE):
        signals = []
        print("[TRIANGULAR] input missing")
    else:
        with open(INPUT_FILE) as f:
            signals = json.load(f)

    opportunities = []
    for s in signals:
        if s.get("price", 0) > 0:
            # простая генерация треугольной возможности
            opp = s.copy()
            opp["tri_arb"] = True
            opportunities.append(opp)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(opportunities, f)

    print(f"[MATRIX] signals loaded: {len(signals)}")
    print(f"[MATRIX] opportunities found: {len(opportunities)}")
    print(f"[MATRIX] opportunities saved: {len(opportunities)}")

if __name__ == "__main__":
    print("[MATRIX] engine start")
    run()