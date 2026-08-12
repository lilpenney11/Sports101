from engine.model import PennyModel

model = PennyModel()

probability = model.calculate_probability(
    pitching=8,
    form=6,
    home=2,
    offense=-1,
    bullpen=4
)

print()

print("Penny Model")

print("----------------")

print(
    f"Win Probability: {round(probability*100,2)}%"
)