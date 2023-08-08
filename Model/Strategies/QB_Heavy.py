from abc import ABC

from Model.Strategies.AStrategy import Strategy


class QBHeavyStrategy(Strategy, ABC, ABC):
    def __init__(self, team_budget):
        super().__init__(team_budget)
        self.budget_allocation = {
            'QB1': 0.175,  # 17.5%
            'QB2': 0.125,  # 12.5%
            'RB1': 0.10,  # 10%
            'RB2': 0.11,  # 11%
            'WR1': 0.10,  # 10%
            'WR2': 0.085,  # 8.5%
            'WR3': 0.10,  # 10%
            'TE1': 0.01,  # 1%
            'Flex': 0.09,  # 9%
            'Bench': 0.105,  # 10.5% for all bench slots
        }

    def bias(self, player, bid_probability, current_bid):
        pos = player.get_position()
        rank = player.get_positional_rank()

        # If the player is a top 5 quarterback, increase the bid probability
        if pos == 'QB' and rank <= 5:
            bid_probability *= 1.10  # increase by 10%

        # Ensure the bid probability does not exceed 1
        bid_probability = min(bid_probability, 1)

        return bid_probability

