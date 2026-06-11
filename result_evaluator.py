import json
import os

LOG_FILE = "data/signals_history.json"


def evaluate_signals(latest_close):

    if not os.path.exists(LOG_FILE):
        return

    with open(LOG_FILE, "r") as f:
        history = json.load(f)

    updated = False

    for item in history:

        if item.get("result") != "PENDING":
            continue

        signal = item.get("signal")
        entry = item.get("entry_price")

        if signal == "CALL":

            if latest_close > entry:
                item["result"] = "WIN"
            else:
                item["result"] = "LOSS"

            updated = True

        elif signal == "PUT":

            if latest_close < entry:
                item["result"] = "WIN"
            else:
                item["result"] = "LOSS"

            updated = True

    if updated:

        with open(LOG_FILE, "w") as f:
            json.dump(history, f, indent=2)
