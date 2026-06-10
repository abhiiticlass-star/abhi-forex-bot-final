import json
import os
from datetime import datetime

LOG_FILE = "data/signals_history.json"


def log_signal(
    data,
    pair,
    timeframe,
    entry_price
):

    if not os.path.exists(LOG_FILE):

        with open(LOG_FILE, "w") as f:
            json.dump([], f)

    with open(LOG_FILE, "r") as f:
        history = json.load(f)

    history.append({

        "time": datetime.utcnow().isoformat(),

        "signal": data.get("signal"),

        "confidence": data.get("confidence"),

        "trend": data.get("trend"),

        "score": data.get("score"),

        "support": data.get("support"),

        "resistance": data.get("resistance")
    })

    with open(LOG_FILE, "w") as f:
        json.dump(history, f, indent=2)
