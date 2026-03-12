import re


BASE_ALIASES = {
    "XBT": "BTC",
    "BCC": "BCH"
}

QUOTE_ALIASES = {
    "USD": "USD",
    "USDT": "USDT",
    "USDC": "USDC"
}


def normalize(symbol: str):

    if not symbol:
        return None

    s = symbol.upper()

    # replace separators
    s = s.replace("-", "/")
    s = s.replace("_", "/")

    parts = None

    if "/" in s:
        parts = s.split("/")
    else:

        # try detect common quotes
        for q in ["USDT", "USDC", "USD", "BTC", "ETH"]:
            if s.endswith(q):
                base = s[:-len(q)]
                quote = q
                parts = [base, quote]
                break

    if not parts or len(parts) != 2:
        return None

    base = parts[0]
    quote = parts[1]

    base = BASE_ALIASES.get(base, base)
    quote = QUOTE_ALIASES.get(quote, quote)

    return f"{base}_{quote}"