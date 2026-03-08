import requests
from datetime import datetime

COINBASE_PRODUCTS = "https://api.exchange.coinbase.com/products"


def fetch():

    signals = []

    try:
        r = requests.get(COINBASE_PRODUCTS, timeout=10)
        products = r.json()
    except Exception as e:
        print("[COINBASE] request error:", e)
        return signals

    if not isinstance(products, list):
        print("[COINBASE] unexpected response")
        return signals

    for product in products:

        if not isinstance(product, dict):
            continue

        symbol = product.get("id")

        if not symbol:
            continue

        ticker_url = f"https://api.exchange.coinbase.com/products/{symbol}/ticker"

        try:
            r = requests.get(ticker_url, timeout=5)
            ticker = r.json()
        except:
            continue

        if not isinstance(ticker, dict):
            continue

        try:
            price = float(ticker.get("price"))
        except:
            continue

        if price <= 0:
            continue

        signals.append({
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "market": "crypto",
            "symbol": symbol,
            "price": price,
            "source": "coinbase"
        })

    print(f"[COINBASE] price snapshots: {len(signals)}")

    return signals