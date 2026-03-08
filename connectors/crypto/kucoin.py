import requests
from datetime import datetime

KUCOIN_API = "https://api.kucoin.com/api/v1/market/allTickers"


def fetch():

    signals = []

    try:
        r = requests.get(KUCOIN_API, timeout=10)
        data = r.json()
    except Exception as e:
        print("[KUCOIN] request error:", e)
        return signals

    ticker_data = data.get("data", {})
    tickers = ticker_data.get("ticker", [])

    if not isinstance(tickers, list):
        print("[KUCOIN] unexpected response")
        return signals

    for asset in tickers:

        symbol = asset.get("symbol")

        try:
            price = float(asset.get("last"))
        except:
            continue

        if price <= 0:
            continue

        signals.append({
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "market": "crypto",
            "symbol": symbol,
            "price": price,
            "source": "kucoin"
        })

    print(f"[KUCOIN] price snapshots: {len(signals)}")

    return signals