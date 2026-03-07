import requests
import json
from datetime import datetime
from pathlib import Path

COINBASE_PRODUCTS = "https://api.exchange.coinbase.com/products"

FEED_DIR = Path("docs/feed")
FEED_DIR.mkdir(parents=True, exist_ok=True)

FEED_FILE = FEED_DIR / "market_prices.json"


def fetch_coinbase():

    try:
        r = requests.get(COINBASE_PRODUCTS, timeout=10)
        products = r.json()
    except Exception as e:
        print("[MARKET_FEED] coinbase request error:", e)
        return []

    prices = []

    for p in products:

        try:
            symbol = p["id"]

            if not symbol.endswith("-USD"):
                continue

            ticker_url = f"https://api.exchange.coinbase.com/products/{symbol}/ticker"
            tr = requests.get(ticker_url, timeout=5)
            t = tr.json()

            bid = float(t["bid"])
            ask = float(t["ask"])

            prices.append({
                "symbol": symbol.replace("-USD", "USDT"),
                "bid": bid,
                "ask": ask,
                "source": "coinbase"
            })

        except Exception:
            continue

    return prices


def write_feed(prices):

    payload = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "source": "coinbase",
        "count": len(prices),
        "prices": prices
    }

    FEED_FILE.write_text(json.dumps(payload, indent=2))


def main():

    print("[MARKET_FEED] fetching prices from coinbase")

    prices = fetch_coinbase()

    if not prices:
        print("[MARKET_FEED] no valid price data")
        return

    write_feed(prices)

    print(f"[MARKET_FEED] stored {len(prices)} prices")


if __name__ == "__main__":
    main()