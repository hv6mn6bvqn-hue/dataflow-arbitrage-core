import requests
from datetime import datetime

BINANCE_API = "https://api.binance.com/api/v3/ticker/price"


def fetch_signals():

    signals = []

    try:
        r = requests.get(BINANCE_API, timeout=10)
        data = r.json()
    except Exception as e:
        print("[BINANCE] request error:", e)
        return signals

    for asset in data:

        symbol = asset.get("symbol")

        try:
            price = float(asset.get("price"))
        except:
            continue

        if price <= 0:
            continue

        signal = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "market": "crypto",
            "symbol": symbol,
            "price": price,
            "confidence": 0.5,
            "type": "price_snapshot",
            "source": "binance"
        }

        signals.append(signal)

    print(f"[BINANCE] price snapshots: {len(signals)}")

    return signals