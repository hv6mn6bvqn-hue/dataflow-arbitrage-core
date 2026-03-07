import requests
import json
from datetime import datetime
from pathlib import Path

BINANCE_TICKER = "https://api.binance.com/api/v3/ticker/bookTicker"

FEED_DIR = Path("docs/feed")
FEED_DIR.mkdir(parents=True, exist_ok=True)

FEED_FILE = FEED_DIR / "market_prices.json"


def fetch_prices():

    try:
        r = requests.get(BINANCE_TICKER, timeout=10)
        data = r.json()
    except Exception as e:
        print("[MARKET_FEED] request error:", e)
        return []

    prices = []

    for item in data:

        symbol = item["symbol"]

        if not symbol.endswith("USDT"):
            continue

        bid = float(item["bidPrice"])
        ask = float(item["askPrice"])

        prices.append({
            "symbol": symbol,
            "bid": bid,
            "ask": ask
        })

    return prices


def write_feed(prices):

    payload = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "source": "binance",
        "count": len(prices),
        "prices": prices
    }

    FEED_FILE.write_text(json.dumps(payload, indent=2))


def main():

    print("[MARKET_FEED] fetching prices")

    prices = fetch_prices()

    if not prices:
        print("[MARKET_FEED] no data")
        return

    write_feed(prices)

    print(f"[MARKET_FEED] stored {len(prices)} prices")


if __name__ == "__main__":
    main()