import json
import os
import requests

INPUT_FILE = "sources/arbitrage_after_fees.json"
OUTPUT_FILE = "sources/orderbook_data.json"


def load_signals():

    if not os.path.exists(INPUT_FILE):
        print("[ORDERBOOK] signals file missing")
        return []

    with open(INPUT_FILE) as f:
        data = json.load(f)

    print("[ORDERBOOK] signals loaded:", len(data))
    return data


def normalize_symbol(symbol):

    if symbol is None:
        return None

    symbol = symbol.upper()
    symbol = symbol.replace("/", "")
    symbol = symbol.replace("-", "")
    symbol = symbol.replace("_", "")

    return symbol


def fetch_all_books():

    try:

        url = "https://api.binance.com/api/v3/ticker/bookTicker"

        r = requests.get(url, timeout=10)

        if r.status_code != 200:
            print("[ORDERBOOK] api blocked")
            return {}

        data = r.json()

        books = {}

        for item in data:

            books[item["symbol"]] = {
                "bid": float(item["bidPrice"]),
                "ask": float(item["askPrice"])
            }

        print("[ORDERBOOK] books loaded:", len(books))

        return books

    except Exception as e:

        print("[ORDERBOOK] request error:", e)

        return {}


def enrich(signals, books):

    enriched = []

    for s in signals:

        symbol = normalize_symbol(s.get("symbol"))

        if symbol not in books:
            continue

        s["bid"] = books[symbol]["bid"]
        s["ask"] = books[symbol]["ask"]
        s["volume"] = s.get("volume", 1000)

        enriched.append(s)

    return enriched


def save(data):

    os.makedirs("sources", exist_ok=True)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, indent=2)

    print("[ORDERBOOK] signals saved:", len(data))


def run():

    print("[ORDERBOOK] orderbook engine start")

    signals = load_signals()

    books = fetch_all_books()

    enriched = enrich(signals, books)

    print("[ORDERBOOK] signals enriched:", len(enriched))

    save(enriched)


def main():
    run()