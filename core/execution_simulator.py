import json
import os

INPUT_FILE = "sources/arbitrage_liquid.json"
OUTPUT_FILE = "sources/execution_validated.json"


def load_signals():

    if not os.path.exists(INPUT_FILE):
        print("[EXECUTION] input missing")
        return []

    with open(INPUT_FILE) as f:
        return json.load(f)


def extract_spread(signal):

    candidates = [
        signal.get("spread_pct"),
        signal.get("spread"),
        signal.get("profit"),
        signal.get("net_spread"),
        signal.get("margin")
    ]

    for value in candidates:
        if isinstance(value, (int, float)):
            return value

    return 0


def validate(signal):

    spread = extract_spread(signal)

    if spread > 0:

        signal["execution_valid"] = True
        signal["execution_spread"] = spread

        if "slippage" not in signal:
            signal["slippage"] = 0.12

        return signal

    return None


def run():

    print("[EXECUTION] execution simulator start")

    signals = load_signals()

    print(f"[EXECUTION] signals loaded: {len(signals)}")

    validated = []

    for signal in signals:
        result = validate(signal)

        if result:
            validated.append(result)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(validated, f, indent=2)

    print(f"[EXECUTION] execution-valid signals: {len(validated)}")
    print("[EXECUTION] signals saved")


def main():
    run()