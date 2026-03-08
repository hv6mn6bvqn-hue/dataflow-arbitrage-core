import requests
from datetime import datetime

OKX_API = "https://www.okx.com/api/v5/market/tickers?instType=SPOT"


def fetch():

    signals = []

    try:
        r = requests.get(OKX_API, timeout=10)
        data = r.json()
    except Exception as e:
        print("[OKX] request error:", e)
        return signals

    if "data" not in data:
        print("[OKX] unexpected response")
        return signals

    for asset in data["data"]:

        if not isinstance(asset, dict):
            continue

        symbol = asset.get("instId")

        try:
            price = float(asset.get("last"))
        except:
            continue

        if price <= 0:
            continue

        signals.append({
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "market": "crypto",
            "symbol": symbol,
            "price": price,
            "source": "okx"
        })

    print(f"[OKX] price snapshots: {len(signals)}")

    return signals