from engine.market import market_consensus
from engine.green_light import analyze_bet


MIN_BOOKS = 3
MAX_AUTO_EV = 15.0


from statistics import median


def american_to_probability(odds):
    if odds > 0:
        return 100 / (odds + 100)

    return abs(odds) / (abs(odds) + 100)


def find_best_price(game, team_name):
    """
    Find the best credible sportsbook price.

    Prices that are dramatically different
    from the rest of the market are excluded.
    """

    prices = []

    for bookmaker in game.get("bookmakers", []):

        book_name = bookmaker.get(
            "title",
            "Unknown"
        )

        for market in bookmaker.get("markets", []):

            if market.get("key") != "h2h":
                continue

            for outcome in market.get("outcomes", []):

                if outcome.get("name") == team_name:

                    odds = outcome.get("price")

                    prices.append({
                        "price": odds,
                        "book": book_name,
                        "implied": american_to_probability(odds)
                    })

    if not prices:
        return None, None

    market_implied = median(
        item["implied"]
        for item in prices
    )

    credible_prices = []

    for item in prices:

        difference = abs(
            item["implied"] - market_implied
        )

        # Reject quotes more than
        # 7 percentage points away
        # from the median market price.
        if difference <= 0.07:
            credible_prices.append(item)

    if not credible_prices:
        return None, None

    best = max(
        credible_prices,
        key=lambda item: item["price"]
    )

    return best["price"], best["book"]


def rank_live_games(games):

    opportunities = []

    for game in games:

        consensus = market_consensus(game)

        for team, market_data in consensus.items():

            fair_probability = market_data["probability"]
            book_count = market_data["book_count"]

            # Don't trust thin markets.
            if book_count < MIN_BOOKS:
                continue

            best_price, best_book = find_best_price(
                game,
                team
            )

            if best_price is None:
                continue

            analysis = analyze_bet(
                american_odds=best_price,
                model_probability=fair_probability
            )

            data_warning = False

            # Huge market-only EV requires manual validation.
            if analysis["expected_value"] > MAX_AUTO_EV:
                data_warning = True

            opportunities.append({
                "team": team,
                "home_team": game.get("home_team"),
                "away_team": game.get("away_team"),
                "book": best_book,
                "price": best_price,
                "book_count": book_count,
                "green_light": (
                    50
                    if data_warning
                    else analysis["green_light"]
                ),
                "rating": (
                    "Data Check"
                    if data_warning
                    else analysis["rating"]
                ),
                "icon": (
                    "⚠️"
                    if data_warning
                    else analysis["icon"]
                ),
                "edge": analysis["edge"],
                "expected_value": analysis["expected_value"],
                "data_warning": data_warning
            })

    return sorted(
        opportunities,
        key=lambda x: x["expected_value"],
        reverse=True
    )