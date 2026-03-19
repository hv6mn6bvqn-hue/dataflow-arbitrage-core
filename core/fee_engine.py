# core/fee_engine.py
import json
from sources import get_arbitrage_signals  # ваш источник сигналов

FEE_FILE = "sources/fee_filtered_signals.json"

def apply_fees(signal):
    # примерная логика расчета комиссии для разных бирж
    fee_map = {
        "binance": 0.00075,
        "kucoin": 0.001,
        "okx": 0.0008,
        "kraken": 0.001,
        "coinbase": 0.001,
        "bybit": 0.0005
    }
    exchange = signal.get("venue")
    fee = fee_map.get(exchange, 0.001)
    signal["net_profit"] = signal.get("profit", 0) - fee
    return signal

def main():
    signals = get_arbitrage_signals()  # реальные сигналы
    if not signals:
        print("[FEES] no signals from arbitrage_detector")
        return

    processed = [apply_fees(s) for s in signals if s.get("profit", 0) > 0]
    with open(FEE_FILE, "w") as f:
        json.dump(processed, f, indent=2)

    print(f"[FEES] signals saved: {len(processed)}")

if __name__ == "__main__":
    main()