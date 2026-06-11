import requests
import pandas as pd
from datetime import datetime

from config import (
    API_KEY,
    CANDLE_LIMIT
)

BASE_URL = (
    "https://api.twelvedata.com/time_series"
)

cache_5m = {
    "data": None,
    "time": None
}

def fetch_candles(
    symbol,
    interval
):

    params = {
        "symbol": symbol,
        "interval": interval,
        "outputsize": CANDLE_LIMIT,
        "apikey": API_KEY,
        "format": "JSON"
    }

    response = requests.get(
        BASE_URL,
        params=params,
        timeout=20
    )

    response.raise_for_status()

    data = response.json()

    if "values" not in data:

        raise Exception(
            f"Invalid API Response: {data}"
        )

    df = pd.DataFrame(
        data["values"]
    )

    df = df.rename(
        columns={
            "datetime": "time"
        }
    )

    numeric_columns = [
        "open",
        "high",
        "low",
        "close"
    ]

    for col in numeric_columns:

        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )

    df = df.sort_values(
        "time"
    )

    df.reset_index(
        drop=True,
        inplace=True
    )

    return df


def get_market_data(
    pair,
    timeframe
):

    current_df = fetch_candles(
        pair,
        timeframe
    )

    global cache_5m

    if timeframe == "1min":

        now = datetime.utcnow()

        use_cache = False

        if (
            cache_5m["data"] is not None
            and cache_5m["time"] is not None
        ):

            age = (
                now -
                cache_5m["time"]
            ).total_seconds()

            if age < 240:
                use_cache = True

        if use_cache:

            higher_df = cache_5m["data"]

        else:

            higher_df = fetch_candles(
                    pair,
                    "5min"
            )

            cache_5m["data"] = higher_df

            cache_5m["time"] = now

    else:

        higher_df = current_df

    return {
        "current": current_df,
        "higher": higher_df
    }
