import requests
from datetime import datetime

BINANCE_API = "https://api.binance.com/api/v3/ticker/24hr"


def fetch_signals():

    signals = []

    try:
        r = requests.get(BINANCE_API, timeout=10)
        data = r.json()
    except Exception as e:
        print("[BINANCE] request error:", e)
        return signals

    for asset in data:

        try:
            change = float(asset["priceChangePercent"])
        except Exception:
            continue

        confidence = min(abs(change) / 20, 1.0)

        if confidence < 0.30:
            continue

        signal = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "market": "crypto",
            "symbol": asset["symbol"],
            "change_percent": change,
            "confidence": round(confidence, 2),
            "type": "market_divergence",
            "source": "binance"
        }

        signals.append(signal)

    print(f"[BINANCE] signals found: {len(signals)}")

    return signals