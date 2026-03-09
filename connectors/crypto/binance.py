import requests

URL = "https://api.binance.com/api/v3/ticker/price"


def fetch_prices():

    r = requests.get(URL, timeout=10)
    data = r.json()

    prices = []

    for item in data:
        try:
            prices.append({
                "symbol": item["symbol"],
                "price": float(item["price"])
            })
        except:
            continue

    return prices