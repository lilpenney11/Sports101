"""
=========================================
Sports101
Green Light Engine
Version 1.1
=========================================

Purpose:
Evaluate a betting opportunity using
basic betting math.

Outputs:
• Implied Probability
• Model Probability
• Edge
• Expected Value
• Green Light Score
• Rating
"""


def american_to_probability(odds):
    if odds > 0:
        return 100 / (odds + 100)

    return abs(odds) / (abs(odds) + 100)


def american_to_decimal(odds):
    if odds > 0:
        return 1 + (odds / 100)

    return 1 + (100 / abs(odds))


def calculate_edge(model_probability, implied_probability):
    return model_probability - implied_probability


def calculate_expected_value(odds, model_probability):
    decimal_odds = american_to_decimal(odds)

    return (model_probability * decimal_odds) - 1


def green_light_score(edge, expected_value):

    if expected_value <= 0:
        return 50

    if edge >= 0.06:
        return 79

    elif edge >= 0.04:
        return 75

    elif edge >= 0.02:
        return 70

    elif edge > 0:
        return 60

    return 50


def get_rating(score):
    if score >= 90:
        return "Elite", "🟢"

    elif score >= 80:
        return "Strong", "🟢"

    elif score >= 70:
        return "Worth Reviewing", "🟡"

    elif score >= 60:
        return "Small Edge", "🟠"

    return "Pass", "🔴"


def analyze_bet(american_odds, model_probability):
    implied = american_to_probability(
        american_odds
    )

    edge = calculate_edge(
        model_probability,
        implied
    )

    expected_value = calculate_expected_value(
        american_odds,
        model_probability
    )

    score = green_light_score(
        edge,
        expected_value
    )

    rating, icon = get_rating(score)

    return {
        "odds": american_odds,
        "implied_probability": round(implied * 100, 2),
        "model_probability": round(model_probability * 100, 2),
        "edge": round(edge * 100, 2),
        "expected_value": round(expected_value * 100, 2),
        "green_light": score,
        "rating": rating,
        "icon": icon,
    }


if __name__ == "__main__":

    result = analyze_bet(
        american_odds=-110,
        model_probability=0.58
    )

    print(result)