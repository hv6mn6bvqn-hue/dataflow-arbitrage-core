import requests

URL = "https://api.kucoin.com/api/v1/market/allTickers"


def fetch_prices():

    r = requests.get(URL, timeout=10)
    data = r.json()

    prices = []

    for item in data.get("data", {}).get("ticker", []):
        try:
            prices.append({
                "symbol": item["symbol"],
                "price": float(item["last"])
            })
        except:
            continue

    return prices