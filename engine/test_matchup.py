from engine.model import PennyModel
from data.mlb_features import MLB_FEATURES


model = PennyModel()


def team_probability(team_name):

    features = MLB_FEATURES[team_name]

    return model.calculate_probability(
        pitching=features["pitching"],
        form=features["form"],
        home=features["home"],
        offense=features["offense"],
        bullpen=features["bullpen"],
    )


braves = team_probability("Atlanta Braves")
mets = team_probability("New York Mets")

total = braves + mets

braves_normalized = braves / total
mets_normalized = mets / total


print("\nSPORTS101 MATCHUP MODEL")
print("-------------------------")

print(
    f"Atlanta Braves: "
    f"{round(braves_normalized * 100, 2)}%"
)

print(
    f"New York Mets: "
    f"{round(mets_normalized * 100, 2)}%"
)