import requests
from datetime import datetime

BYBIT_API = "https://api.bybit.com/v5/market/tickers?category=spot"


def fetch():

    signals = []

    try:
        r = requests.get(BYBIT_API, timeout=10)
        data = r.json()
    except Exception as e:
        print("[BYBIT] request error:", e)
        return signals

    result = data.get("result", {})
    tickers = result.get("list", [])

    if not isinstance(tickers, list):
        print("[BYBIT] unexpected response")
        return signals

    for asset in tickers:

        symbol = asset.get("symbol")

        try:
            price = float(asset.get("lastPrice"))
        except:
            continue

        if price <= 0:
            continue

        signals.append({
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "market": "crypto",
            "symbol": symbol,
            "price": price,
            "source": "bybit"
        })

    print(f"[BYBIT] price snapshots: {len(signals)}")

    return signals