import os
from datetime import datetime

import requests
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv("ODDS_API_KEY")
SPORT = "baseball_mlb"

URL = f"https://api.the-odds-api.com/v4/sports/{SPORT}/odds"


def get_live_odds():
    if not API_KEY:
        print("ERROR: Sports101 could not find your API key.")
        print("Check that the file is named .env and contains:")
        print("ODDS_API_KEY=your_actual_key")
        return

    parameters = {
        "apiKey": API_KEY,
        "regions": "us",
        "markets": "h2h,spreads,totals",
        "oddsFormat": "american",
    }

    try:
        response = requests.get(URL, params=parameters, timeout=15)
        response.raise_for_status()
        games = response.json()

    except requests.exceptions.RequestException as error:
        print("Sports101 could not retrieve the odds.")
        print(error)
        return

    today = datetime.now().strftime("%B %d, %Y")

    print("\n========================================")
    print("SPORTS101 LIVE ODDS")
    print(today)
    print("========================================")

    if not games:
        print("\nNo MLB games with available odds were found.")
        return

    for game in games:
        away_team = game.get("away_team", "Away Team")
        home_team = game.get("home_team", "Home Team")
        start_time = game.get("commence_time", "Unknown time")
        bookmakers = game.get("bookmakers", [])

        print(f"\n{away_team} at {home_team}")
        print(f"Start time: {start_time}")

        if not bookmakers:
            print("No sportsbook odds available.")
            continue

        bookmaker = bookmakers[0]
        print(f"Sportsbook: {bookmaker.get('title', 'Unknown')}")

        for market in bookmaker.get("markets", []):
            market_name = market.get("key")

            if market_name == "h2h":
                print("Moneyline:")

            elif market_name == "spreads":
                print("Spread:")

            elif market_name == "totals":
                print("Total:")

            for outcome in market.get("outcomes", []):
                name = outcome.get("name")
                price = outcome.get("price")
                point = outcome.get("point")

                if point is None:
                    print(f"  {name}: {price}")
                else:
                    print(f"  {name}: {point} ({price})")

    remaining = response.headers.get("x-requests-remaining")
    used = response.headers.get("x-requests-used")

    print("\n========================================")
    print(f"API requests used: {used}")
    print(f"API requests remaining: {remaining}")
    print("========================================")


get_live_odds()
