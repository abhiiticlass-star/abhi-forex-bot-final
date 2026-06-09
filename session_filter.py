from datetime import datetime
import pytz


UTC = pytz.utc


def get_utc_hour():

    now = datetime.now(UTC)

    return now.hour


def is_london_session():

    hour = get_utc_hour()

    return 8 <= hour < 17


def is_newyork_session():

    hour = get_utc_hour()

    return 13 <= hour < 22


def is_overlap_session():

    hour = get_utc_hour()

    return 13 <= hour < 17


def is_low_liquidity():

    hour = get_utc_hour()

    # Asian late hours + weekend-like quiet periods

    if 0 <= hour < 6:
        return True

    if 22 <= hour <= 23:
        return True

    return False


def get_session_score():

    score = 0
    reasons = []

    if is_overlap_session():

        score += 20
        reasons.append(
            "London-NewYork Overlap"
        )

    elif is_london_session():

        score += 10
        reasons.append(
            "London Session"
        )

    elif is_newyork_session():

        score += 10
        reasons.append(
            "NewYork Session"
        )

    if is_low_liquidity():

        score -= 20
        reasons.append(
            "Low Liquidity"
        )

    return {
        "score": score,
        "reasons": reasons
    }
