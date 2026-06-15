from ta.trend import EMAIndicator, MACD
from ta.momentum import RSIIndicator
from ta.volatility import AverageTrueRange

from psychology import get_psychology_score
from session_filter import get_session_score
from support_resistance import get_sr_score
from breakout import get_breakout_score
from multi_timeframe import get_multi_timeframe_score

from config import (
    CONFIDENCE_MIN,
    CONFIDENCE_MAX
)


def detect_bullish_engulfing(df):

    if len(df) < 2:
        return False

    prev = df.iloc[-2]
    curr = df.iloc[-1]

    return (
        prev["close"] < prev["open"]
        and curr["close"] > curr["open"]
        and curr["close"] > prev["open"]
    )


def detect_bearish_engulfing(df):

    if len(df) < 2:
        return False

    prev = df.iloc[-2]
    curr = df.iloc[-1]

    return (
        prev["close"] > prev["open"]
        and curr["close"] < curr["open"]
        and curr["close"] < prev["open"]
    )


def prepare_indicators(df):

    close = df["close"]

    df["ema20"] = EMAIndicator(
        close,
        window=20
    ).ema_indicator()

    df["ema50"] = EMAIndicator(
        close,
        window=50
    ).ema_indicator()

    df["ema200"] = EMAIndicator(
        close,
        window=200
    ).ema_indicator()

    df["rsi"] = RSIIndicator(
        close,
        window=14
    ).rsi()

    macd = MACD(close)

    df["macd"] = macd.macd()

    df["macd_signal"] = (
        macd.macd_signal()
    )

    atr = AverageTrueRange(
        df["high"],
        df["low"],
        close,
        window=14
    )

    df["atr"] = (
        atr.average_true_range()
    )

    return df


def generate_signal(
    current_df,
    higher_df
):

    current_df = prepare_indicators(
        current_df
    )

    latest = current_df.iloc[-1]

    score = 0

    reasons = []

    trend = "Neutral"

    # EMA Trend

    if (
        latest["ema20"]
        > latest["ema50"]
        > latest["ema200"]
    ):

        score += 25

        trend = "Bullish"

        reasons.append(
            "Strong Uptrend"
        )

    elif (
        latest["ema20"]
        < latest["ema50"]
        < latest["ema200"]
    ):

        score -= 25

        trend = "Bearish"

        reasons.append(
            "Strong Downtrend"
        )

    # RSI

    if latest["rsi"] > 60:

        score += 15

        reasons.append(
            "RSI Bullish"
        )

    elif latest["rsi"] < 40:

        score -= 15

        reasons.append(
            "RSI Bearish"
        )

    # MACD

    if (
        latest["macd"]
        > latest["macd_signal"]
    ):

        score += 15

        reasons.append(
            "MACD Bullish"
        )

    else:

        score -= 15

        reasons.append(
            "MACD Bearish"
        )

    # Candlestick Patterns

    if detect_bullish_engulfing(
        current_df
    ):

        score += 20

        reasons.append(
            "Bullish Engulfing"
        )

    if detect_bearish_engulfing(
        current_df
    ):

        score -= 20

        reasons.append(
            "Bearish Engulfing"
        )

    # Psychology

    psychology = (
        get_psychology_score(
            current_df
        )
    )

    score += psychology["score"]

    reasons.extend(
        psychology["reasons"]
    )

    # Candle Exhaustion Filter

    last6 = current_df.tail(6)

    bullish_count = 0
    bearish_count = 0

    for _, row in last6.iterrows():

        if row["close"] > row["open"]:
            bullish_count += 1

        elif row["close"] < row["open"]:
            bearish_count += 1

    if bullish_count >= 5:

        score -= 20

        reasons.append(
            "Bullish Exhaustion"
        )

    if bearish_count >= 5:

        score += 20

        reasons.append(
            "Bearish Exhaustion"
        )

    # Session Filter

    session = get_session_score()

    score += session["score"]

    reasons.extend(
        session["reasons"]
    )

    # Support Resistance

    sr = get_sr_score(
        current_df
    )

    score += sr["score"]

    reasons.extend(
        sr["reasons"]
    )

    price = latest["close"]

    distance_to_resistance = abs(
        sr["resistance"] - price
    )

    distance_to_support = abs(
        price - sr["support"]
    )

    if (
        trend == "Bullish"
        and distance_to_resistance < latest["atr"] * 0.5
    ):
        score -= 30
        reasons.append(
            "Near Resistance Rejection"
        )

    if (
        trend == "Bearish"
        and distance_to_support < latest["atr"] * 0.5
    ):
        score += 30
        reasons.append(
            "Near Support Rejection"
        )

    # Breakout

    breakout = (
        get_breakout_score(
            current_df,
            sr["support"],
            sr["resistance"]
        )
    )

    score += breakout["score"]

    reasons.extend(
        breakout["reasons"]
    )

    # Multi Timeframe

    mtf = (
        get_multi_timeframe_score(
            current_df,
            higher_df
        )
    )

    score += mtf["score"]

    reasons.extend(
        mtf["reasons"]
    )

    higher_df = prepare_indicators(higher_df)

    higher_latest = higher_df.iloc[-1]

    trend_higher = "Neutral"

    if (
        higher_latest["ema20"]
        > higher_latest["ema50"]
        > higher_latest["ema200"]
    ):
        trend_higher = "Bullish"

    elif (
        higher_latest["ema20"]
        < higher_latest["ema50"]
        < higher_latest["ema200"]
    ):
        trend_higher = "Bearish"

    # Volatility Filter

    recent_atr = (
        current_df["atr"]
        .tail(20)
        .mean()
    )

    if latest["atr"] < recent_atr * 0.70:

        score -= 25

        reasons.append(
            "Low Volatility Market"
        )

    # Final Signal

    mtf_block = False

    if score >= 30 and trend_higher != "Bullish":
        mtf_block = True

    if score <= -30 and trend_higher != "Bearish":
        mtf_block = True

    if mtf_block:

        signal = "AVOID"

    elif score >= 30:

        signal = "CALL"

    elif score <= -30:

        signal = "PUT"

    else:

        signal = "AVOID"

    confidence = min(
        CONFIDENCE_MAX,
        max(
            CONFIDENCE_MIN,
            abs(score)
        )
    )

    return {
        "signal": signal,
        "confidence": confidence,
        "trend": trend,
        "score": score,
        "support": sr["support"],
        "resistance": sr["resistance"],
        "reasons": reasons[:10]
    }
