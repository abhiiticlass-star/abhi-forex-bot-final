def candle_body_size(candle):

    return abs(
        candle["close"] -
        candle["open"]
    )

def bullish_breakout(
    df,
    resistance
):

    latest = df.iloc[-1]

    body = abs(
        latest["close"] -
        latest["open"]
    )

    atr = latest.get("atr", 0)

    return (

        latest["close"] > resistance

        and

        body > atr * 0.40

    )


def bearish_breakout(
    df,
    support
):

    latest = df.iloc[-1]

    body = abs(
        latest["close"] -
        latest["open"]
    )

    atr = latest.get("atr", 0)

    return (

        latest["close"] < support

        and

        body > atr * 0.40

    )


def fake_bullish_breakout(df, resistance):

    if len(df) < 2:
        return False

    prev = df.iloc[-2]
    latest = df.iloc[-1]

    return (
        prev["close"] > resistance
        and latest["close"] < resistance
    )


def fake_bearish_breakout(df, support):

    if len(df) < 2:
        return False

    prev = df.iloc[-2]
    latest = df.iloc[-1]

    return (
        prev["close"] < support
        and latest["close"] > support
    )


def bullish_retest(df, resistance):

    latest = df.iloc[-1]

    return (
        latest["low"] <= resistance
        and latest["close"] > resistance
    )


def bearish_retest(df, support):

    latest = df.iloc[-1]

    return (
        latest["high"] >= support
        and latest["close"] < support
    )


def get_breakout_score(
    df,
    support,
    resistance
):

    score = 0

    reasons = []

    if bullish_breakout(
        df,
        resistance
    ):

        score += 20

        reasons.append(
            "Bullish Breakout"
        )

    if bearish_breakout(
        df,
        support
    ):

        score -= 20

        reasons.append(
            "Bearish Breakout"
        )

    if fake_bullish_breakout(
        df,
        resistance
    ):

        score -= 25

        reasons.append(
            "Fake Bullish Breakout"
        )

    if fake_bearish_breakout(
        df,
        support
    ):

        score += 25

        reasons.append(
            "Fake Bearish Breakout"
        )

    if bullish_retest(
        df,
        resistance
    ):

        score += 15

        reasons.append(
            "Bullish Retest"
        )

    if bearish_retest(
        df,
        support
    ):

        score -= 15

        reasons.append(
            "Bearish Retest"
        )

    return {
        "score": score,
        "reasons": reasons
    }
