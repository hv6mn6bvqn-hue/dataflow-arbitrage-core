import requests

URL = "https://api.exchange.coinbase.com/products"


def fetch_prices():

    products = requests.get(URL, timeout=10).json()

    prices = []

    for p in products:

        try:
            ticker = requests.get(
                f"https://api.exchange.coinbase.com/products/{p['id']}/ticker",
                timeout=10
            ).json()

            prices.append({
                "symbol": p["id"],
                "price": float(ticker["price"])
            })

        except:
            continue

    return prices