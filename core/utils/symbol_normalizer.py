import re


BASE_ALIASES = {
    "XBT": "BTC"
}

QUOTE_ALIASES = {
    "USDT": "USD",
    "USDC": "USD"
}


def normalize_symbol(symbol: str) -> str:
    """
    Convert exchange-specific symbol formats to unified format.

    Examples:
        BTCUSDT  -> BTCUSD
        BTC-USDT -> BTCUSD
        BTC/USD  -> BTCUSD
        XBTUSD   -> BTCUSD
    """

    if not symbol:
        return None

    s = symbol.upper()

    # remove separators
    s = s.replace("-", "")
    s = s.replace("_", "")
    s = s.replace("/", "")

    # known quote currencies
    quotes = ["USDT", "USDC", "USD", "BTC", "ETH", "EUR"]

    for q in quotes:
        if s.endswith(q):

            base = s[:-len(q)]
            quote = q

            base = BASE_ALIASES.get(base, base)
            quote = QUOTE_ALIASES.get(quote, quote)

            return base + quote

    return s


def normalize_snapshot(snapshot: dict):

    if "symbol" not in snapshot:
        return snapshot

    normalized = normalize_symbol(snapshot["symbol"])

    snapshot["symbol"] = normalized

    return snapshot