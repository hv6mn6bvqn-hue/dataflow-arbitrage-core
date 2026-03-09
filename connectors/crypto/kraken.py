import requests

URL = "https://api.kraken.com/0/public/Ticker?pair=BTCUSD,ETHUSD"


def fetch_prices():

    r = requests.get(URL, timeout=10)
    data = r.json()

    prices = []

    for symbol, info in data.get("result", {}).items():
        try:
            prices.append({
                "symbol": symbol,
                "price": float(info["c"][0])
            })
        except:
            continue

    return prices