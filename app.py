import os
import requests
import streamlit as st
from datetime import datetime
from dotenv import load_dotenv
from engine.ranking import rank_live_games


# -----------------------------
# SPORTS101 SETUP
# -----------------------------

load_dotenv()

API_KEY = os.getenv("ODDS_API_KEY")

st.set_page_config(
    page_title="Sports101",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# -----------------------------
# DESIGN
# -----------------------------

st.markdown("""
<style>

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}

[data-testid="stSidebar"] {
    background-color: #11151b;
}

.game-card {
    background-color: #161b22;
    border: 1px solid #2a313b;
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 16px;
}

.game-title {
    font-size: 22px;
    font-weight: 700;
}

.game-time {
    color: #9ca3af;
    font-size: 14px;
    margin-bottom: 18px;
}

.odds-label {
    color: #9ca3af;
    font-size: 13px;
}

.odds-number {
    font-size: 22px;
    font-weight: 700;
}

.sportsbook {
    color: #7dd3fc;
    font-size: 13px;
}

.penny-box {
    background-color: #152238;
    border-radius: 14px;
    padding: 18px;
    margin-top: 12px;
}

</style>
""", unsafe_allow_html=True)


# -----------------------------
# ODDS API
# -----------------------------

def get_mlb_games():

    if not API_KEY:
        return [], "API key missing"

    url = (
        "https://api.the-odds-api.com/v4/"
        "sports/baseball_mlb/odds"
    )

    params = {
        "apiKey": API_KEY,
        "regions": "us",
        "markets": "h2h",
        "oddsFormat": "american"
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=15
        )

        response.raise_for_status()

        remaining = response.headers.get(
            "x-requests-remaining",
            "Unknown"
        )

        return response.json(), remaining

    except Exception as error:

        return [], str(error)


# -----------------------------
# BEST PRICE FINDER
# -----------------------------

def get_best_moneylines(game):

    prices = {}

    for book in game.get("bookmakers", []):

        book_name = book.get("title", "Unknown")

        for market in book.get("markets", []):

            if market.get("key") != "h2h":
                continue

            for outcome in market.get("outcomes", []):

                team = outcome.get("name")
                price = outcome.get("price")

                if team not in prices:
                    prices[team] = {
                        "price": price,
                        "book": book_name
                    }

                else:

                    current_price = prices[team]["price"]

                    if price > current_price:

                        prices[team] = {
                            "price": price,
                            "book": book_name
                        }

    return prices


def format_odds(price):

    if price is None:
        return "N/A"

    if price > 0:
        return f"+{price}"

    return str(price)


# -----------------------------
# SIDEBAR
# -----------------------------

st.sidebar.title("SPORTS101")
st.sidebar.caption("Powered by Penny")

st.sidebar.divider()

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "⚾ MLB",
        "🏈 NFL",
        "🏀 NBA",
        "💰 Bankroll",
        "📊 Results"
    ]
)

st.sidebar.divider()

st.sidebar.caption("Sports101 v0.3")
st.sidebar.caption("Dashboard Alpha")


# -----------------------------
# LOAD DATA
# -----------------------------

mlb_games, api_status = get_mlb_games()
ranked_mlb = rank_live_games(mlb_games) if mlb_games else []

top_mlb = [
    item
    for item in ranked_mlb
    if not item.get("data_warning")
    and item["expected_value"] > 0
][:3]


# -----------------------------
# DASHBOARD
# -----------------------------

if page == "🏠 Dashboard":

    st.title("SPORTS101")
    st.caption("Powered by Penny")

    today = datetime.now().strftime(
        "%A, %B %d, %Y"
    )

    st.write(today)

    st.divider()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Bankroll",
        "$1,000"
    )

    col2.metric(
        "MLB Games",
        len(mlb_games)
    )

    col3.metric(
        "Today's Plays",
        "0"
    )

    col4.metric(
        "ROI",
        "0.0%"
    )

    st.divider()

    st.subheader("🏆 Today's Top 3 Market Opportunities")

    if not top_mlb:

        st.info(
            "No positive market-value opportunities qualify right now."
        )

    else:

        columns = st.columns(3)

        for index, item in enumerate(top_mlb):

            with columns[index]:

                price = item["price"]

                if price > 0:
                    price_display = f"+{price}"
                else:
                    price_display = str(price)

                with st.container(border=True):

                    st.caption(
                        f'#{index + 1} MARKET OPPORTUNITY'
                    )

                    st.subheader(item["team"])

                    st.write(
                        f'{item["away_team"]} @ '
                        f'{item["home_team"]}'
                    )

                    st.metric(
                        "Best Price",
                        price_display
                    )

                    st.caption(
                        f'Best at {item["book"]}'
                    )

                    st.metric(
                        "Penny Score",
                        item["green_light"]
                    )

                    st.metric(
                        "Estimated Market EV",
                        f'{item["expected_value"]}%'
                    )

                    st.write(
                        f'{item["icon"]} '
                        f'{item["rating"]}'
                    )

    st.subheader("Today's Market")

    if not mlb_games:

        st.warning(
            "No MLB odds are available right now."
        )

    else:

        for game in mlb_games[:5]:

            away = game.get(
                "away_team",
                "Away Team"
            )

            home = game.get(
                "home_team",
                "Home Team"
            )

            best_prices = get_best_moneylines(game)

            away_info = best_prices.get(away, {})
            home_info = best_prices.get(home, {})

            

            c1, c2, c3 = st.columns(
                [2, 2, 1]
            )

            with c1:

                st.caption(away)

                st.metric(
                    "Best Moneyline",
                    format_odds(
                        away_info.get("price")
                    )
                )

                st.caption(
                    away_info.get(
                        "book",
                        "No sportsbook"
                    )
                )

            with c2:

                st.caption(home)

                st.metric(
                    "Best Moneyline",
                    format_odds(
                        home_info.get("price")
                    )
                )

                st.caption(
                    home_info.get(
                        "book",
                        "No sportsbook"
                    )
                )

            with c3:

                st.caption(
                    "Green Light"
                )

                st.metric(
                    "Score",
                    "—"
                )

                st.caption(
                    "Coming next"
                )

            st.divider()

    st.subheader("Penny's Notes")

    if mlb_games:

        st.markdown(
            f"""
            <div class="penny-box">

            I found <b>{len(mlb_games)}</b>
            MLB games with sportsbook odds.

            I'm currently comparing prices
            across sportsbooks.

            <br><br>

            <b>No bets have been recommended yet.</b>

            The Green Light Engine is the next
            feature we'll build.

            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.info(
            "Penny is waiting for available games."
        )

    st.caption(
        f"Odds API requests remaining: {api_status}"
    )


# -----------------------------
# MLB PAGE
# -----------------------------

elif page == "⚾ MLB":

    st.title("⚾ MLB")

    st.caption(
        "Live sportsbook moneylines"
    )

    st.divider()

    if not mlb_games:

        st.warning(
            "No MLB games available."
        )

    for game in mlb_games:

        away = game.get("away_team")
        home = game.get("home_team")

        prices = get_best_moneylines(game)

        with st.expander(
            f"{away} @ {home}"
        ):

            col1, col2 = st.columns(2)

            away_price = prices.get(
                away,
                {}
            )

            home_price = prices.get(
                home,
                {}
            )

            with col1:

                st.subheader(away)

                st.metric(
                    "Best Moneyline",
                    format_odds(
                        away_price.get("price")
                    )
                )

                st.write(
                    "Sportsbook:",
                    away_price.get(
                        "book",
                        "N/A"
                    )
                )

            with col2:

                st.subheader(home)

                st.metric(
                    "Best Moneyline",
                    format_odds(
                        home_price.get("price")
                    )
                )

                st.write(
                    "Sportsbook:",
                    home_price.get(
                        "book",
                        "N/A"
                    )
                )


# -----------------------------
# NFL
# -----------------------------

elif page == "🏈 NFL":

    st.title("🏈 NFL")

    st.info(
        "NFL odds integration is coming next."
    )


# -----------------------------
# NBA
# -----------------------------

elif page == "🏀 NBA":

    st.title("🏀 NBA")

    st.info(
        "NBA odds integration will activate "
        "when games become available."
    )


# -----------------------------
# BANKROLL
# -----------------------------

elif page == "💰 Bankroll":

    st.title("💰 Bankroll")

    st.metric(
        "Starting Bankroll",
        "$1,000"
    )

    st.metric(
        "Current Bankroll",
        "$1,000"
    )

    st.metric(
        "Profit / Loss",
        "$0"
    )

    st.info(
        "Automatic bankroll tracking "
        "will be added shortly."
    )


# -----------------------------
# RESULTS
# -----------------------------

elif page == "📊 Results":

    st.title("📊 Results")

    st.metric(
        "Record",
        "0-0"
    )

    st.metric(
        "Units",
        "0.00"
    )

    st.metric(
        "ROI",
        "0.0%"
    )

    st.info(
        "Sports101 will automatically "
        "track recommendations and results."
    )
