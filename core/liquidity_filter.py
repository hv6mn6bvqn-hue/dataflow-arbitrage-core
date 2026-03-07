from datetime import datetime

MIN_PRICE = 0.0001
MAX_PRICE = 100000

BLACKLIST = [
    "SCAM",
    "TEST"
]


def valid_symbol(symbol):

    if not symbol:
        return False

    for bad in BLACKLIST:
        if bad in symbol:
            return False

    return True


def valid_price(price):

    try:
        price = float(price)
    except:
        return False

    if price < MIN_PRICE:
        return False

    if price > MAX_PRICE:
        return False

    return True


def filter_signals(signals):

    filtered = []

    for s in signals:

        symbol = s.get("symbol")
        price = s.get("price")

        if not valid_symbol(symbol):
            continue

        if not valid_price(price):
            continue

        s["filtered_at"] = datetime.utcnow().isoformat() + "Z"

        filtered.append(s)

    return filtered