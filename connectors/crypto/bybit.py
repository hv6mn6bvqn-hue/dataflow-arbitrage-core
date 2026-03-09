import requests

URL = "https://api.bybit.com/v5/market/tickers?category=spot"


def fetch_prices():

    r = requests.get(URL, timeout=10)
    data = r.json()

    prices = []

    for item in data.get("result", {}).get("list", []):
        try:
            prices.append({
                "symbol": item["symbol"],
                "price": float(item["lastPrice"])
            })
        except:
            continue

    return prices