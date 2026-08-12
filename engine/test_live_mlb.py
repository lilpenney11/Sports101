import os
import sys
import requests
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from engine.ranking import rank_live_games


load_dotenv()

API_KEY = os.getenv("ODDS_API_KEY")

url = "https://api.the-odds-api.com/v4/sports/baseball_mlb/odds"

params = {
    "apiKey": API_KEY,
    "regions": "us",
    "markets": "h2h",
    "oddsFormat": "american"
}

response = requests.get(url, params=params, timeout=15)
response.raise_for_status()

games = response.json()
print(f"\nGames returned by Odds API: {len(games)}")

print([f'{game.get("away_team")} @ {game.get("home_team")}' for game in games])

ranked = rank_live_games(games)
print(f"Opportunities created by Sports101: {len(ranked)}")

print("\nSPORTS101 - TOP LIVE MLB OPPORTUNITIES\n")

print("\nSPORTS101 - TOP LIVE MLB OPPORTUNITIES\n")

for item in ranked[:10]:

    price = item["price"]

    if price > 0:
        price = f"+{price}"

    print(
        f'{item["icon"]} '
        f'{item["away_team"]} @ {item["home_team"]} | '
        f'Pick: {item["team"]} | '
        f'{price} | '
        f'{item["book"]} | '
        f'Books: {item["book_count"]} | '
        f'Penny Score: {item["green_light"]} | '
        f'EV: {item["expected_value"]}% | '
        f'{item["rating"]}'
    )