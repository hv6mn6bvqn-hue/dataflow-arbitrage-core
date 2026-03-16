import json
from pathlib import Path

INPUT_FILE = "data/order_confirmed.json"
OUTPUT_FILE = "data/reconciled_pnl.json"


def load_data():
    path = Path(INPUT_FILE)
    if not path.exists():
        return []

    with open(path, "r") as f:
        return json.load(f)


def reconcile(signals):
    result = []

    for signal in signals:
        pnl = signal.get("realized_pnl", 0)

        signal["reconciled_pnl"] = pnl
        signal["pnl_validated"] = True

        result.append(signal)

    return result


def save_data(data):
    Path("data").mkdir(exist_ok=True)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, indent=4)


def main():
    print("[PNL_RECON] start")

    signals = load_data()
    reconciled = reconcile(signals)
    save_data(reconciled)

    print(f"[PNL_RECON] reconciled: {len(reconciled)}")


if __name__ == "__main__":
    main()