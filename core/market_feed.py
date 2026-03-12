import requests
import json
import os

OUTPUT_FILE = "sources/market_feed.json"


def fetch_prices():

    print("[MARKET_FEED] fetching prices from coinbase")

    url = "https://api.exchange.coinbase.com/products"

    try:

        r = requests.get(url, timeout=10)
        products = r.json()

        prices = []

        for p in products:

            if p.get("quote_currency") == "USD":

                prices.append({
                    "exchange": "coinbase",
                    "symbol": p["id"]
                })

        return prices

    except Exception as e:

        print("[MARKET_FEED] error:", e)
        return []


def save_prices(prices):

    os.makedirs("sources", exist_ok=True)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(prices, f, indent=2)

    print("[MARKET_FEED] stored", len(prices), "prices")


def run():

    prices = fetch_prices()
    save_prices(prices)


def main():
    run()