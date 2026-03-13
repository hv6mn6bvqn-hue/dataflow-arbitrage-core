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
    symbol = symbol.replace("/", "-")
    symbol = symbol.replace("_", "-")

    return symbol


def fetch_okx_book(symbol):

    try:

        url = f"https://www.okx.com/api/v5/market/ticker?instId={symbol}"

        r = requests.get(url, timeout=5)

        if r.status_code != 200:
            return None, None

        data = r.json()

        if "data" not in data or len(data["data"]) == 0:
            return None, None

        bid = float(data["data"][0]["bidPx"])
        ask = float(data["data"][0]["askPx"])

        return bid, ask

    except Exception:
        return None, None


def fetch_kucoin_book(symbol):

    try:

        kucoin_symbol = symbol.replace("-", "")

        url = f"https://api.kucoin.com/api/v1/market/orderbook/level1?symbol={symbol}"

        r = requests.get(url, timeout=5)

        if r.status_code != 200:
            return None, None

        data = r.json()

        if "data" not in data:
            return None, None

        bid = float(data["data"]["bestBid"])
        ask = float(data["data"]["bestAsk"])

        return bid, ask

    except Exception:
        return None, None


def enrich(signals):

    enriched = []

    for s in signals:

        symbol = normalize_symbol(s.get("symbol"))

        bid, ask = fetch_okx_book(symbol)

        if bid is None:
            bid, ask = fetch_kucoin_book(symbol)

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