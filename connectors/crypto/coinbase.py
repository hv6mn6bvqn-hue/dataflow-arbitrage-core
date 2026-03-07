import requests
from datetime import datetime

COINBASE_API = "https://api.exchange.coinbase.com/products/ticker"


def fetch_signals():

    signals = []

    try:
        r = requests.get(COINBASE_API, timeout=10)
        data = r.json()
    except Exception as e:
        print("[COINBASE] request error:", e)
        return signals

    for asset in data:

        try:
            price = float(asset.get("price", 0))
        except Exception:
            continue

        if price <= 0:
            continue

        symbol = asset.get("product_id", "UNKNOWN")

        signal = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "market": "crypto",
            "symbol": symbol,
            "price": price,
            "confidence": 0.5,
            "type": "price_snapshot",
            "source": "coinbase"
        }

        signals.append(signal)

    print(f"[COINBASE] signals found: {len(signals)}")

    return signals