import json
from pathlib import Path
from datetime import datetime

EXPORT_DIR = Path("exports")
PUBLIC_DIR = Path("public")

PUBLIC_DIR.mkdir(parents=True, exist_ok=True)

PUBLIC_SIGNAL_FILE = PUBLIC_DIR / "signals.json"


def load_signals():

    signals = []

    if not EXPORT_DIR.exists():
        return signals

    for file in EXPORT_DIR.glob("*.json"):

        try:
            data = json.loads(file.read_text())

            if data.get("type") == "signal":
                signals.append(data)

        except Exception:
            continue

    return signals


def publish(signals):

    payload = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "signal_count": len(signals),
        "signals": signals[-100:]
    }

    PUBLIC_SIGNAL_FILE.write_text(json.dumps(payload, indent=2))


def main():

    print("[EXPORTER] collecting signals")

    signals = load_signals()

    print(f"[EXPORTER] signals found: {len(signals)}")

    publish(signals)

    print("[EXPORTER] public feed updated")


if __name__ == "__main__":
    main()