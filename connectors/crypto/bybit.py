import requests


URL = "https://api.bybit.com/v5/market/tickers?category=spot"


def fetch_prices():

    try:

        r = requests.get(
            URL,
            timeout=10,
            headers={
                "User-Agent": "Mozilla/5.0",
                "Accept": "application/json"
            }
        )

        if r.status_code != 200:
            print("[BYBIT] bad status:", r.status_code)
            return []

        data = r.json()

        if "result" not in data:
            print("[BYBIT] unexpected response:", data)
            return []

        tickers = data["result"]["list"]

        prices = []

        for item in tickers:

            prices.append({
                "exchange": "bybit",
                "symbol": item["symbol"],
                "price": float(item["lastPrice"])
            })

        print("[BYBIT] price snapshots:", len(prices))

        return prices

    except Exception as e:

        print("[BYBIT] request error:", e)
        return []