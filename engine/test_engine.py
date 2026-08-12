print("Penny test is running!")
from market import market_consensus, remove_vig
from green_light import analyze_bet


sample_game = {
    "bookmakers": [
        {
            "markets": [
                {
                    "key": "h2h",
                    "outcomes": [
                        {
                            "name": "Team A",
                            "price": -120
                        },
                        {
                            "name": "Team B",
                            "price": +110
                        }
                    ]
                }
            ]
        },
        {
            "markets": [
                {
                    "key": "h2h",
                    "outcomes": [
                        {
                            "name": "Team A",
                            "price": -125
                        },
                        {
                            "name": "Team B",
                            "price": +115
                        }
                    ]
                }
            ]
        }
    ]
}


consensus = market_consensus(sample_game)

fair_probabilities = remove_vig(consensus)

print("Market Consensus:")
print(consensus)

print("\nNo-Vig Probabilities:")
print(fair_probabilities)

team_a_probability = fair_probabilities["Team A"]

analysis = analyze_bet(
    american_odds=-120,
    model_probability=team_a_probability
)

print("\nBet Analysis:")
print(analysis)