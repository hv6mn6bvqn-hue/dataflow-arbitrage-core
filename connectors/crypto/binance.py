import requests
from datetime import datetime

BINANCE_API = "https://api.binance.com/api/v3/ticker/price"


def fetch():

    signals = []

    try:
        r = requests.get(BINANCE_API, timeout=10)
        data = r.json()
    except Exception as e:
        print("[BINANCE] request error:", e)
        return signals

    if not isinstance(data, list):
        print("[BINANCE] unexpected response")
        return signals

    for asset in data:

        if not isinstance(asset, dict):
            continue

        symbol = asset.get("symbol")

        try:
            price = float(asset.get("price"))
        except:
            continue

        if price <= 0:
            continue

        signals.append({
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "market": "crypto",
            "symbol": symbol,
            "price": price,
            "source": "binance"
        })

    print(f"[BINANCE] price snapshots: {len(signals)}")

    return signals