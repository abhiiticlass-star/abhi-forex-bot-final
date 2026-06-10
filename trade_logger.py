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

        "pair": pair,
        
        "timeframe": timeframe,

        "signal": data.get("signal"),

        "entry_price": entry_price,

        "confidence": data.get("confidence"),

        "trend": data.get("trend"),

        "score": data.get("score"),

        "support": data.get("support"),

        "resistance": data.get("resistance"),

        "result": "PENDING"
    })
    with open(LOG_FILE, "w") as f:
        json.dump(history, f, indent=2)
