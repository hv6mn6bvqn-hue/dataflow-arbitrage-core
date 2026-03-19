# core/analyzer.py
import json
import os

SIGNALS_FILE = "sources/pnl_reconciled.json"
OUTPUT_FILE = "sources/analyzed_signals.json"

def run():
    if not os.path.exists(SIGNALS_FILE):
        signals = []
        print("[ANALYZER] no signals to analyze")
    else:
        with open(SIGNALS_FILE) as f:
            signals = json.load(f)

    for s in signals:
        # Анализ силы рынка
        s["market_strength"] = 0.34  # placeholder
        s["confidence"] = 0.55       # placeholder

    with open(OUTPUT_FILE, "w") as f:
        json.dump(signals, f)

    print(f"[ANALYZER] market strength {signals[0]['market_strength'] if signals else 'N/A'}")

if __name__ == "__main__":
    print("[ANALYZER] loading feed")
    run()
