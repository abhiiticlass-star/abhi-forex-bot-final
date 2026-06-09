from ta.trend import EMAIndicator


def calculate_trend(df):

    close = df["close"]

    ema20 = EMAIndicator(
        close,
        window=20
    ).ema_indicator()

    ema50 = EMAIndicator(
        close,
        window=50
    ).ema_indicator()

    latest_ema20 = ema20.iloc[-1]
    latest_ema50 = ema50.iloc[-1]

    if latest_ema20 > latest_ema50:
        return "Bullish"

    if latest_ema20 < latest_ema50:
        return "Bearish"

    return "Neutral"


def get_multi_timeframe_score(
    current_df,
    higher_df
):

    score = 0

    reasons = []

    current_trend = calculate_trend(
        current_df
    )

    higher_trend = calculate_trend(
        higher_df
    )

    if (
        current_trend == "Bullish"
        and higher_trend == "Bullish"
    ):

        score += 20

        reasons.append(
            "MTF Bullish Alignment"
        )

    elif (
        current_trend == "Bearish"
        and higher_trend == "Bearish"
    ):

        score -= 20

        reasons.append(
            "MTF Bearish Alignment"
        )

    else:

        reasons.append(
            "MTF Conflict"
        )

        if current_trend == "Bullish":
            score -= 10

        elif current_trend == "Bearish":
            score += 10

    return {
        "score": score,
        "current_trend": current_trend,
        "higher_trend": higher_trend,
        "reasons": reasons
    }
