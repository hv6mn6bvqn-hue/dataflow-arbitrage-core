import requests

BASE_URLS = [
    "https://api.binance.com/api/v3/ticker/price",
    "https://api1.binance.com/api/v3/ticker/price",
    "https://api2.binance.com/api/v3/ticker/price"
]


def fetch_prices():

    for url in BASE_URLS:

        try:

            r = requests.get(
                url,
                timeout=10,
                headers={
                    "User-Agent": "Mozilla/5.0"
                }
            )

            data = r.json()

            if isinstance(data, list):

                prices = []

                for item in data:
                    prices.append({
                        "exchange": "binance",
                        "symbol": item["symbol"],
                        "price": float(item["price"])
                    })

                print("[BINANCE] price snapshots:", len(prices))

                return prices

            else:

                print("[BINANCE] unexpected response:", data)

        except Exception as e:

            print("[BINANCE] request error:", e)

    return []