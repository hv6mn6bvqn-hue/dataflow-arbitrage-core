import requests
from datetime import datetime
from pathlib import Path
import json

FEED_PATH = Path("docs/feed/index.json")

CONNECTORS = {
    "coinbase": "https://api.exchange.coinbase.com/products"
}


def fetch_coinbase_prices():

    signals = []

    try:
        r = requests.get(CONNECTORS["coinbase"], timeout=10)
        products = r.json()
    except Exception as e:
        print("[DISCOVERY] coinbase error:", e)
        return signals

    for product in products:

        symbol = product.get("id")

        if not symbol.endswith("-USD"):
            continue

        try:
            ticker = requests.get(
                f"https://api.exchange.coinbase.com/products/{symbol}/ticker",
                timeout=5
            ).json()

            price = float(ticker.get("price", 0))

            if price <= 0:
                continue

            signals.append({
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "symbol": symbol.replace("-USD", "USDT"),
                "price": price,
                "source": "coinbase",
                "confidence": 0.5,
                "type": "price_snapshot"
            })

        except Exception:
            continue

    return signals


def load_feed():

    if not FEED_PATH.exists():
        return {
            "feed_version": "v2",
            "generated_at": "",
            "signal_count": 0,
            "signals": []
        }

    return json.loads(FEED_PATH.read_text())


def save_feed(feed):

    FEED_PATH.parent.mkdir(parents=True, exist_ok=True)
    FEED_PATH.write_text(json.dumps(feed, indent=2))


def main():

    print("[DISCOVERY V2] loading connectors")

    signals = fetch_coinbase_prices()

    print(f"[DISCOVERY V2] raw signals: {len(signals)}")

    if not signals:
        return

    feed = load_feed()

    feed["signals"].extend(signals)
    feed["signal_count"] = len(feed["signals"])
    feed["generated_at"] = datetime.utcnow().isoformat() + "Z"

    save_feed(feed)

    print(f"[DISCOVERY V2] signals added: {len(signals)}")


if __name__ == "__main__":
    main()