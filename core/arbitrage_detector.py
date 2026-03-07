import json
from pathlib import Path
from datetime import datetime

FEED_FILE = Path("docs/feed/market_prices.json")
EXPORT_FILE = Path("docs/feed/arbitrage_opportunities.json")


def load_prices():

    if not FEED_FILE.exists():
        return []

    data = json.loads(FEED_FILE.read_text())

    return data.get("prices", [])


def detect_arbitrage(prices):

    opportunities = []

    price_map = {}

    for p in prices:

        symbol = p["symbol"]
        bid = p["bid"]
        ask = p["ask"]

        if symbol not in price_map:
            price_map[symbol] = []

        price_map[symbol].append((bid, ask))

    for symbol, quotes in price_map.items():

        if len(quotes) < 2:
            continue

        bids = [q[0] for q in quotes]
        asks = [q[1] for q in quotes]

        best_bid = max(bids)
        best_ask = min(asks)

        spread = best_bid - best_ask

        if spread <= 0:
            continue

        percent = spread / best_ask

        if percent > 0.002:

            opportunities.append({
                "symbol": symbol,
                "spread": spread,
                "percent": round(percent, 5),
                "timestamp": datetime.utcnow().isoformat() + "Z"
            })

    return opportunities


def save_opportunities(opps):

    EXPORT_FILE.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "count": len(opps),
        "opportunities": opps
    }

    EXPORT_FILE.write_text(json.dumps(payload, indent=2))


def main():

    print("[ARBITRAGE] scanning markets")

    prices = load_prices()

    if not prices:
        print("[ARBITRAGE] no price data")
        return

    opps = detect_arbitrage(prices)

    print(f"[ARBITRAGE] opportunities found: {len(opps)}")

    if opps:
        save_opportunities(opps)


if __name__ == "__main__":
    main()