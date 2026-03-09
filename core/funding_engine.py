import json
import requests
from pathlib import Path
from datetime import datetime

DATA_DIR = Path("sources")
DATA_DIR.mkdir(exist_ok=True)

FUNDING_FILE = DATA_DIR / "funding_rates.json"
OPPORTUNITIES_FILE = DATA_DIR / "funding_opportunities.json"


def fetch_binance():
    url = "https://fapi.binance.com/fapi/v1/premiumIndex"
    try:
        r = requests.get(url, timeout=10)
        data = r.json()

        result = []
        for item in data:
            result.append({
                "exchange": "binance",
                "symbol": item["symbol"],
                "funding": float(item["lastFundingRate"])
            })

        return result
    except Exception as e:
        print("[FUNDING] binance error:", e)
        return []


def fetch_okx():
    url = "https://www.okx.com/api/v5/public/funding-rate?instType=SWAP"
    try:
        r = requests.get(url, timeout=10)
        data = r.json()["data"]

        result = []
        for item in data:
            result.append({
                "exchange": "okx",
                "symbol": item["instId"].replace("-", ""),
                "funding": float(item["fundingRate"])
            })

        return result
    except Exception as e:
        print("[FUNDING] okx error:", e)
        return []


def fetch_bybit():
    url = "https://api.bybit.com/v5/market/tickers?category=linear"
    try:
        r = requests.get(url, timeout=10)
        data = r.json()["result"]["list"]

        result = []
        for item in data:
            result.append({
                "exchange": "bybit",
                "symbol": item["symbol"],
                "funding": float(item["fundingRate"])
            })

        return result
    except Exception as e:
        print("[FUNDING] bybit error:", e)
        return []


def collect_funding():
    print("[FUNDING] collecting funding rates")

    funding = []
    funding += fetch_binance()
    funding += fetch_okx()
    funding += fetch_bybit()

    print("[FUNDING] collected:", len(funding))

    with open(FUNDING_FILE, "w") as f:
        json.dump(funding, f, indent=2)

    return funding


def find_arbitrage(funding):
    print("[FUNDING] searching arbitrage")

    opportunities = []

    symbols = {}

    for item in funding:
        sym = item["symbol"]
        symbols.setdefault(sym, []).append(item)

    for sym, exchanges in symbols.items():

        for i in range(len(exchanges)):
            for j in range(i + 1, len(exchanges)):

                a = exchanges[i]
                b = exchanges[j]

                diff = abs(a["funding"] - b["funding"])

                if diff > 0.0005:  # 0.05%
                    opportunities.append({
                        "symbol": sym,
                        "long_exchange": a["exchange"] if a["funding"] < b["funding"] else b["exchange"],
                        "short_exchange": a["exchange"] if a["funding"] > b["funding"] else b["exchange"],
                        "funding_a": a["funding"],
                        "funding_b": b["funding"],
                        "spread": diff,
                        "timestamp": datetime.utcnow().isoformat()
                    })

    print("[FUNDING] opportunities:", len(opportunities))

    with open(OPPORTUNITIES_FILE, "w") as f:
        json.dump(opportunities, f, indent=2)

    return opportunities


def main():
    print("[FUNDING] engine start")

    funding = collect_funding()

    if not funding:
        print("[FUNDING] no data")
        return

    find_arbitrage(funding)

    print("[FUNDING] engine complete")


if __name__ == "__main__":
    main()