import requests


KRAKEN_API = "https://api.kraken.com/0/public/Ticker"


PAIRS = [
    "XBTUSD",
    "ETHUSD",
    "SOLUSD",
    "ADAUSD",
    "DOGEUSD"
]


def fetch():

    prices = []

    try:

        pairs = ",".join(PAIRS)

        r = requests.get(f"{KRAKEN_API}?pair={pairs}", timeout=10)

        data = r.json()

        result = data.get("result", {})

        for pair, info in result.items():

            ask = float(info["a"][0])
            bid = float(info["b"][0])

            symbol = pair.replace("XBT", "BTC")

            prices.append({
                "symbol": symbol,
                "bid": bid,
                "ask": ask,
                "source": "kraken"
            })

    except Exception as e:

        print("[KRAKEN] error:", e)

    print(f"[KRAKEN] price snapshots: {len(prices)}")

    return prices