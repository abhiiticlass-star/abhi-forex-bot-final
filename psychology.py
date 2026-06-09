def candle_body_size(candle):

    return abs(
        candle["close"] - candle["open"]
    )


def candle_range(candle):

    return (
        candle["high"] - candle["low"]
    )


def upper_wick(candle):

    return (
        candle["high"]
        - max(
            candle["open"],
            candle["close"]
        )
    )


def lower_wick(candle):

    return (
        min(
            candle["open"],
            candle["close"]
        )
        - candle["low"]
    )


def bullish_strength(candle):

    body = candle_body_size(candle)
    rng = candle_range(candle)

    if rng == 0:
        return 0

    return (body / rng) * 100


def bearish_strength(candle):

    body = candle_body_size(candle)
    rng = candle_range(candle)

    if rng == 0:
        return 0

    return (body / rng) * 100


def is_bullish_momentum(candle):

    if candle["close"] <= candle["open"]:
        return False

    body = candle_body_size(candle)
    rng = candle_range(candle)

    if rng == 0:
        return False

    return (body / rng) >= 0.70


def is_bearish_momentum(candle):

    if candle["close"] >= candle["open"]:
        return False

    body = candle_body_size(candle)
    rng = candle_range(candle)

    if rng == 0:
        return False

    return (body / rng) >= 0.70


def is_bullish_rejection(candle):

    lw = lower_wick(candle)
    body = candle_body_size(candle)

    return lw > body * 2


def is_bearish_rejection(candle):

    uw = upper_wick(candle)
    body = candle_body_size(candle)

    return uw > body * 2


def is_exhaustion_candle(candle):

    rng = candle_range(candle)

    if rng == 0:
        return False

    body = candle_body_size(candle)

    return (
        body / rng
    ) < 0.15


def get_psychology_score(df):

    latest = df.iloc[-1]

    score = 0

    reasons = []

    if is_bullish_momentum(latest):

        score += 20

        reasons.append(
            "Bullish Momentum"
        )

    if is_bearish_momentum(latest):

        score -= 20

        reasons.append(
            "Bearish Momentum"
        )

    if is_bullish_rejection(latest):

        score += 15

        reasons.append(
            "Bullish Rejection"
        )

    if is_bearish_rejection(latest):

        score -= 15

        reasons.append(
            "Bearish Rejection"
        )

    if is_exhaustion_candle(latest):

        score -= 10

        reasons.append(
            "Exhaustion Candle"
        )

    return {
        "score": score,
        "reasons": reasons
    }
