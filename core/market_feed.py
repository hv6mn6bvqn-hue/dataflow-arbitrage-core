import requests
import json
import os
import time

OUTPUT_FILE = "sources/market_feed.json"


def fetch_prices():

    print("[MARKET_FEED] fetching prices from coinbase")

    url = "https://api.exchange.coinbase.com/products"

    try:

        r = requests.get(url, timeout=10)

        products = r.json()

        prices = []

        for p in products:

            symbol = p["id"]

            ticker_url = f"https://api.exchange.coinbase.com/products/{symbol}/ticker"

            try:

                tr = requests.get(ticker_url, timeout=5)
                t = tr.json()

                price = float(t["price"])

                prices.append({
                    "exchange": "coinbase",
                    "symbol": symbol,
                    "price": price,
                    "timestamp": int(time.time())
                })

            except:
                continue

        os.makedirs("sources", exist_ok=True)

        with open(OUTPUT_FILE, "w") as f:
            json.dump(prices, f, indent=2)

        print(f"[MARKET_FEED] stored {len(prices)} prices")

        return prices

    except Exception as e:

        print("[MARKET_FEED] error:", e)

        return []