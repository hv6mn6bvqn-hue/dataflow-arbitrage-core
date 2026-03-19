# core/discovery_engine_v2.py
import requests
import json

EXCHANGES = {
    "okx": "https://www.okx.com/api/spot/v3/instruments/ticker",
    "kraken": "https://api.kraken.com/0/public/Ticker?pair=BTCUSD",
    "coinbase": "https://api.exchange.coinbase.com/products/BTC-USD/ticker",
    "bybit": "https://api.bybit.com/v2/public/tickers",
    "kucoin": "https://api.kucoin.com/api/v1/market/allTickers",
    "binance": "https://api.binance.com/api/v3/ticker/price"
}

def fetch_snapshot(exchange, url):
    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        if not data:
            raise ValueError(f"{exchange} returned empty data")
        return data
    except Exception as e:
        print(f"[{exchange.upper()}] request error: {e}")
        return []

def run():
    all_signals = []
    for ex, url in EXCHANGES.items():
        snapshot = fetch_snapshot(ex, url)
        print(f"[{ex.upper()}] snapshots: {len(snapshot) if snapshot else 0}")
        if isinstance(snapshot, list):
            all_signals.extend(snapshot)
        elif isinstance(snapshot, dict) and "result" in snapshot:
            all_signals.extend(snapshot["result"])
    with open("sources/discovery_signals.json", "w") as f:
        json.dump(all_signals, f)
    print(f"[DISCOVERY] signals saved: {len(all_signals)}")

if __name__ == "__main__":
    print("[DISCOVERY] engine start")
    run()