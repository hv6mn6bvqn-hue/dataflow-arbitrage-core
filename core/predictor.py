from datetime import datetime
import random

def generate_presignal():
    """
    Генерирует предварительный сигнал.
    Вероятность strong-состояния искусственно занижена — это контроль.
    """

    roll = random.random()

    if roll > 0.97:
        return {
            "signal_type": "potential_strong",
            "confidence": 0.82,
            "note": "rare high-confidence pattern detected"
        }

    elif roll > 0.85:
        return {
            "signal_type": "weak_activity",
            "confidence": 0.45,
            "note": "weak correlated movement"
        }

    else:
        return {
            "signal_type": "noise",
            "confidence": 0.10,
            "note": "background noise"
        }


def run():
    ts = datetime.utcnow().isoformat() + "Z"
    presignal = generate_presignal()
    presignal["timestamp"] = ts
    presignal["source"] = "predictor"
    return presignal


if __name__ == "__main__":
    print(run())
