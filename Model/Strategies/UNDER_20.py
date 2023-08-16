from abc import ABC
from Model.Strategies.AStrategy import Strategy


class Under20Strategy(Strategy, ABC):
    def __init__(self, team_budget):
        super().__init__(team_budget)
        self.budget_allocation = {
            'QB1': 10.00 * 2,
            'QB2': 7.50 * 2,
            'WR1': 9.50 * 2,
            'WR2': 8.50 * 2,
            'WR3': 7.50 * 2,
            'RB1': 9.50 * 2,
            'RB2': 6.00 * 2,
            'TE1': 7.50 * 2,
            'Flex': 10.00 * 2,
            'BN1': 6.00 * 2,
            'BN2': 5.00 * 2,
            'BN3': 8.00 * 2,
            'BN4': 1.50 * 2,
            'BN5': 2.50 * 2,
            'BN6': 1.00 * 2
        }

    def bias(self, player, bid_probability, current_bid, team):
        pass
