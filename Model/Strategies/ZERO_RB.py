from abc import ABC

from Model.Strategies.AStrategy import Strategy


class ZeroRBStrategy(Strategy, ABC):
    def __init__(self, team_budget):
        super().__init__(team_budget)
        self.budget_allocation = {
            'QB1': 0.10,  # 10%
            'QB2': 0.05,  # 5%
            'RB1': 0.035,  # 3.5%
            'RB2': 0.035,  # 3.5%
            'WR1': 0.25,  # 25%
            'WR2': 0.19,  # 19%
            'WR3': 0.15,  # 15%
            'TE1': 0.02,  # 2%
            'Flex': 0.10,  # 10%
            'Bench': 0.06,  # 6% for all bench slots
        }


