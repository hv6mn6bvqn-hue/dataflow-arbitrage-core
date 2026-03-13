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


def fetch_orderbook(symbol):

    try:

        symbol = normalize_symbol(symbol)

        if symbol is None:
            return None, None

        url = f"https://api.binance.com/api/v3/ticker/bookTicker?symbol={symbol}"

        r = requests.get(url, timeout=5)

        if r.status_code != 200:
            return None, None

        data = r.json()

        if "bidPrice" not in data:
            return None, None

        bid = float(data["bidPrice"])
        ask = float(data["askPrice"])

        return bid, ask

    except Exception:

        return None, None


def enrich(signals):

    enriched = []

    for s in signals:

        symbol = s.get("symbol")

        bid, ask = fetch_orderbook(symbol)

        if bid is None:
            continue

        s["bid"] = bid
        s["ask"] = ask
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

    enriched = enrich(signals)

    print("[ORDERBOOK] signals enriched:", len(enriched))

    save(enriched)


def main():
    run()