"""
Sports101
Market Consensus Engine
Version 1.2

Each sportsbook is de-vigged independently
before the market probabilities are combined.
"""

from statistics import median


def american_to_probability(odds):
    if odds > 0:
        return 100 / (odds + 100)

    return abs(odds) / (abs(odds) + 100)


def market_consensus(game):
    """
    Calculate a no-vig probability at each sportsbook,
    then use the median across sportsbooks.

    Median is intentionally used instead of average
    because it is less sensitive to strange/outlier prices.
    """

    team_probabilities = {}

    for bookmaker in game.get("bookmakers", []):

        for market in bookmaker.get("markets", []):

            if market.get("key") != "h2h":
                continue

            outcomes = market.get("outcomes", [])

            # MLB moneyline should have two sides.
            if len(outcomes) != 2:
                continue

            first = outcomes[0]
            second = outcomes[1]

            p1 = american_to_probability(first["price"])
            p2 = american_to_probability(second["price"])

            total = p1 + p2

            if total <= 0:
                continue

            fair_p1 = p1 / total
            fair_p2 = p2 / total

            team_probabilities.setdefault(
                first["name"], []
            ).append(fair_p1)

            team_probabilities.setdefault(
                second["name"], []
            ).append(fair_p2)

    consensus = {}

    for team, probabilities in team_probabilities.items():

        consensus[team] = {
            "probability": median(probabilities),
            "book_count": len(probabilities)
        }

    return consensus