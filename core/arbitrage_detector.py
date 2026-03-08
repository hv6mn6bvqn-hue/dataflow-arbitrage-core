import json
from pathlib import Path
from datetime import datetime

FEED_PATH = Path("docs/feed/index.json")
EXPORT_DIR = Path("exports")

EXPORT_DIR.mkdir(exist_ok=True)


def load_feed():

    if not FEED_PATH.exists():
        return []

    data = json.loads(FEED_PATH.read_text())

    return data.get("signals", [])


def group_by_symbol(signals):

    markets = {}

    for s in signals:

        symbol = s.get("symbol")

        if not symbol:
            continue

        markets.setdefault(symbol, []).append(s)

    return markets


def detect_arbitrage(markets):

    opportunities = []

    for symbol, entries in markets.items():

        if len(entries) < 2:
            continue

        prices = []

        for e in entries:

            price = e.get("price") or e.get("ask") or e.get("bid")

            if price:
                prices.append((e.get("source"), float(price)))

        if len(prices) < 2:
            continue

        prices.sort(key=lambda x: x[1])

        low_exchange, low_price = prices[0]
        high_exchange, high_price = prices[-1]

        spread = high_price - low_price

        if spread <= 0:
            continue

        opportunities.append({
            "type": "signal",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "symbol": symbol,
            "buy_from": low_exchange,
            "sell_to": high_exchange,
            "buy_price": low_price,
            "sell_price": high_price,
            "spread": spread
        })

    return opportunities


def export(opportunities):

    for i, signal in enumerate(opportunities):

        file = EXPORT_DIR / f"arb_signal_{i}.json"

        file.write_text(json.dumps(signal, indent=2))


def main():

    print("[ARBITRAGE] scanning markets")

    signals = load_feed()

    markets = group_by_symbol(signals)

    opportunities = detect_arbitrage(markets)

    print(f"[ARBITRAGE] opportunities found: {len(opportunities)}")

    if opportunities:
        export(opportunities)


if __name__ == "__main__":
    main()