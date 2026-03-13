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


def fetch_orderbook(symbol):

    # пример запроса к публичному API (можно расширять под другие биржи)
    try:
        url = f"https://api.binance.com/api/v3/ticker/bookTicker?symbol={symbol.replace('/', '')}"
        r = requests.get(url, timeout=5)
        data = r.json()

        bid = float(data["bidPrice"])
        ask = float(data["askPrice"])

        return bid, ask

    except Exception:
        return None, None


def enrich_with_orderbook(signals):

    enriched = []

    for s in signals:

        symbol = s.get("symbol")

        bid, ask = fetch_orderbook(symbol)

        if bid is None:
            continue

        s["bid"] = bid
        s["ask"] = ask

        # условная оценка объёма
        s["volume"] = s.get("volume", 1000)

        enriched.append(s)

    return enriched


def save(signals):

    os.makedirs("sources", exist_ok=True)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(signals, f, indent=2)

    print("[ORDERBOOK] signals saved:", len(signals))


def run():

    print("[ORDERBOOK] orderbook engine start")

    signals = load_signals()

    enriched = enrich_with_orderbook(signals)

    print("[ORDERBOOK] signals enriched:", len(enriched))

    save(enriched)


def main():
    run()