import numpy as np


LOOKBACK = 20


def get_recent_support(df):

    lows = df["low"].tail(LOOKBACK)

    return float(lows.min())


def get_recent_resistance(df):

    highs = df["high"].tail(LOOKBACK)

    return float(highs.max())


def distance_from_support(price, support):

    return abs(price - support)


def distance_from_resistance(price, resistance):

    return abs(price - resistance)


def near_support(price, support, atr):

    return (
        distance_from_support(
            price,
            support
        ) <= atr
    )


def near_resistance(price, resistance, atr):

    return (
        distance_from_resistance(
            price,
            resistance
        ) <= atr
    )


def support_bounce(price, support, atr):

    return (
        price > support
        and near_support(
            price,
            support,
            atr
        )
    )


def resistance_rejection(
    price,
    resistance,
    atr
):

    return (
        price < resistance
        and near_resistance(
            price,
            resistance,
            atr
        )
    )


def get_sr_score(df):

    latest = df.iloc[-1]

    current_price = latest["close"]

    atr = latest["atr"]

    support = get_recent_support(df)

    resistance = get_recent_resistance(df)

    score = 0

    reasons = []

    if support_bounce(
        current_price,
        support,
        atr
    ):

        score += 15

        reasons.append(
            "Support Bounce"
        )

    if resistance_rejection(
        current_price,
        resistance,
        atr
    ):

        score -= 15

        reasons.append(
            "Resistance Rejection"
        )

    return {
        "score": score,
        "support": support,
        "resistance": resistance,
        "reasons": reasons
    }
