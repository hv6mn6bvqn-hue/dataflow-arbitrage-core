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


def validate(signal):

    spread = signal.get("spread_pct", 0)

    if spread > 0.05:
        signal["execution_valid"] = True

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