import requests
import json
from pathlib import Path
from datetime import datetime

FEED_PATH = Path("docs/feed/index.json")

BINANCE_API = "https://api.binance.com/api/v3/ticker/24hr"


def fetch_market_data():
    r = requests.get(BINANCE_API, timeout=10)
    data = r.json()
    return data


def detect_anomalies(data):
    signals = []

    for asset in data:

        try:
            change = float(asset["priceChangePercent"])
        except:
            continue

        confidence = min(abs(change) / 20, 1.0)

        if confidence < 0.30:
            continue

        signal = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "confidence": round(confidence, 2),
            "type": "market_divergence",
            "symbol": asset["symbol"],
            "change_percent": change,
            "source": "binance"
        }

        signals.append(signal)

    return signals


def load_feed():

    if not FEED_PATH.exists():
        return {
            "feed_version": "v1",
            "generated_at": "",
            "signal_count": 0,
            "signals": []
        }

    return json.loads(FEED_PATH.read_text())


def save_feed(feed):
    FEED_PATH.parent.mkdir(parents=True, exist_ok=True)
    FEED_PATH.write_text(json.dumps(feed, indent=2))


def main():

    print("[DISCOVERY] fetching market data")

    market = fetch_market_data()

    signals = detect_anomalies(market)

    if not signals:
        print("[DISCOVERY] no anomalies")
        return

    feed = load_feed()

    for s in signals:
        feed["signals"].append(s)

    feed["signal_count"] = len(feed["signals"])
    feed["generated_at"] = datetime.utcnow().isoformat() + "Z"

    save_feed(feed)

    print(f"[DISCOVERY] added {len(signals)} signals")


if __name__ == "__main__":
    main()