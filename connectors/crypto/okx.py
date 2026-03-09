import requests

URL = "https://www.okx.com/api/v5/market/tickers?instType=SPOT"


def fetch_prices():

    r = requests.get(URL, timeout=10)
    data = r.json()

    prices = []

    for item in data.get("data", []):
        try:
            prices.append({
                "symbol": item["instId"],
                "price": float(item["last"])
            })
        except:
            continue

    return prices