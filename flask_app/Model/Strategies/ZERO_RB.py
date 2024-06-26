from abc import ABC

from .AStrategy import Strategy


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
            'WR3': 0.10 * 200,  # 10%
            'TE1': 0.07 * 200,  # 2%
            'Flex': 0.10 * 200,  # 10%
            'BN1': 0.01 * 200,  # 1%
            'BN2': 0.01 * 200,  # 1%
            'BN3': 0.01 * 200,  # 1%
            'BN4': 0.02 * 200,  # 2%
            'BN5': 0.05 * 200,  # .5%
            'BN6': 0.05 * 200   # .5%
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



