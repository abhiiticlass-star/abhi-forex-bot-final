import json

LOG_FILE = "data/signals_history.json"


def get_stats():

    try:

        with open(LOG_FILE, "r") as f:
            data = json.load(f)

    except:

        return {
            "wins": 0,
            "losses": 0,
            "accuracy": 0
        }

    wins = 0
    losses = 0

    for item in data:

        if item.get("result") == "WIN":
            wins += 1

        elif item.get("result") == "LOSS":
            losses += 1

    total = wins + losses

    accuracy = 0

    if total > 0:

        accuracy = round(
            wins * 100 / total,
            2
        )

    return {
        "wins": wins,
        "losses": losses,
        "accuracy": accuracy
    }
