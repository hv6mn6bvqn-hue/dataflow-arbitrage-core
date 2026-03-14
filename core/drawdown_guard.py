import json
import os

INPUT_FILE = "sources/position_sized.json"
OUTPUT_FILE = "sources/risk_approved.json"


def load_signals():

    if not os.path.exists(INPUT_FILE):
        print("[RISK] position file missing")
        return []

    with open(INPUT_FILE) as f:
        return json.load(f)


def approve(signal):

    position = signal.get("position_size", 0)

    if position <= 1000:
        signal["risk_status"] = "approved"
        return signal

    return None


def run():

    print("[RISK] drawdown guard start")

    signals = load_signals()

    approved = []

    for signal in signals:
        result = approve(signal)

        if result:
            approved.append(result)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(approved, f, indent=2)

    print(f"[RISK] signals approved: {len(approved)}")


def main():
    run()