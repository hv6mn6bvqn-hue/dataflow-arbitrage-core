import requests
from datetime import datetime

COINBASE_PRODUCTS = "https://api.exchange.coinbase.com/products"


def fetch_prices():

    signals = []

    try:
        r = requests.get(COINBASE_PRODUCTS, timeout=10)
        products = r.json()
    except Exception as e:
        print("[COINBASE] request error:", e)
        return signals

    for product in products:

        symbol = product.get("id")

        if not symbol:
            continue

        ticker_url = f"https://api.exchange.coinbase.com/products/{symbol}/ticker"

        try:
            r = requests.get(ticker_url, timeout=5)
            ticker = r.json()
            price = float(ticker.get("price", 0))
        except Exception:
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
            "source": "coinbase"
        }

        signals.append(signal)

    print(f"[COINBASE] price snapshots: {len(signals)}")

    return signals