from abc import ABC

from Model.Strategies.AStrategy import Strategy


class ZeroRBStrategy(Strategy, ABC):
    def __init__(self, team_budget):
        super().__init__(team_budget)
        self.budget_allocation = {
            'QB1': 0.10 * 200,  # 10%
            'QB2': 0.05 * 200,  # 5%
            'RB1': 0.035 * 200,  # 3.5%
            'RB2': 0.035 * 200,  # 3.5%
            'WR1': 0.25 * 200,  # 25%
            'WR2': 0.19 * 200,  # 19%
            'WR3': 0.15 * 200,  # 15%
            'TE1': 0.02 * 200,  # 2%
            'Flex': 0.10 * 200,  # 10%
            'Bench': 0.06 * 200  # 6% for all bench slots
        }

    # Zero-RB bias chases low ranked running-backs
    def bias(self, player, bid_probability, current_bid, team):
        pos = player.get_position()
        rank = player.get_positional_rank()

        if pos == 'WR' and rank < 7:
            # Increase the bid probability by 5%
            bid_probability *= 1.10

            # Ensure the bid probability does not exceed 1
            bid_probability = min(bid_probability, 1)

        return bid_probability



