import json
import urllib.request
from datetime import datetime

GITHUB_SEARCH_URL = (
    "https://api.github.com/search/repositories"
    "?q=created:>={date}&sort=created&order=desc&per_page=5"
)

def fetch_new_repos():
    today = datetime.utcnow().strftime("%Y-%m-%d")
    url = GITHUB_SEARCH_URL.format(date=today)

    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode())

    return len(data.get("items", []))


def generate_signal():
    count = fetch_new_repos()

    signal = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "source": "github",
        "new_repositories": count,
        "signal_type": "activity_spike" if count > 0 else "none",
        "confidence": min(count / 10, 1.0)
    }

    return signal
