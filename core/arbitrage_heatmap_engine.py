# core/arbitrage_heatmap_engine.py
import json
import os

INPUT_FILE = "sources/venue_rotation.json"
OUTPUT_FILE = "sources/heatmap.json"

def run():
    if not os.path.exists(INPUT_FILE):
        zones = []
        print("[HEATMAP] input missing")
    else:
        with open(INPUT_FILE) as f:
            signals = json.load(f)
        # Простая зона heatmap: делим на bins по size
        zones = [{"signal_id": i, "zone": s.get("size", 0)//10} for i, s in enumerate(signals)]

    with open(OUTPUT_FILE, "w") as f:
        json.dump(zones, f)

    print(f"[HEATMAP] zones: {len(zones)}")

if __name__ == "__main__":
    print("[HEATMAP] start")
    run()