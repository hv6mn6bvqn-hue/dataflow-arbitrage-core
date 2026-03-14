import json
import os
import random

INPUT_FILE = "sources/slippage_safe.json"
OUTPUT_FILE = "sources/latency_checked.json"


def load_signals():
    if not os.path.exists(INPUT_FILE):
        print("[LATENCY] input missing")
        return []

    with open(INPUT_FILE) as f:
        return json.load(f)


def apply_latency(signal):

    latency = round(random.uniform(0.01, 0.20), 4)

    signal["latency"] = latency

    return signal


def run():

    print("[LATENCY] monitor start")

    signals = load_signals()

    checked = [apply_latency(s) for s in signals]

    with open(OUTPUT_FILE, "w") as f:
        json.dump(checked, f, indent=2)

    print(f"[LATENCY] checked: {len(checked)}")


def main():
    run()