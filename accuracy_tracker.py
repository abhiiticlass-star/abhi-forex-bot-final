import json
import os

FILE = "data/accuracy.json"


def init_accuracy():

    if not os.path.exists(FILE):

        with open(FILE, "w") as f:

            json.dump({
                "wins": 0,
                "losses": 0
            }, f)


def record_result(result):

    init_accuracy()

    with open(FILE, "r") as f:

        data = json.load(f)

    if result == "WIN":

        data["wins"] += 1

    elif result == "LOSS":

        data["losses"] += 1

    with open(FILE, "w") as f:

        json.dump(data, f, indent=2)


def get_accuracy():

    init_accuracy()

    with open(FILE, "r") as f:

        data = json.load(f)

    total = (
        data["wins"]
        +
        data["losses"]
    )

    accuracy = 0

    if total > 0:

        accuracy = round(
            data["wins"] * 100 / total,
            2
        )

    return {
        "wins": data["wins"],
        "losses": data["losses"],
        "accuracy": accuracy
    }
