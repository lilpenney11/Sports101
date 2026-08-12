"""
Sports101
Penny Intelligence Engine
Version 1.0
"""


class PennyModel:

    def __init__(self):

        self.weights = {
            "pitching": 0.35,
            "form": 0.20,
            "home": 0.10,
            "offense": 0.15,
            "bullpen": 0.20
        }

    def calculate_probability(
        self,
        pitching,
        form,
        home,
        offense,
        bullpen
    ):

        score = (

            pitching * self.weights["pitching"]

            +

            form * self.weights["form"]

            +

            home * self.weights["home"]

            +

            offense * self.weights["offense"]

            +

            bullpen * self.weights["bullpen"]

        )

        probability = 0.50 + (score / 100)

        probability = max(
            0.05,
            min(probability, 0.95)
        )

        return probability