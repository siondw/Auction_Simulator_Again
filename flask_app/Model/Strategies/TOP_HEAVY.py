from abc import ABC
from .AStrategy import Strategy

class TopHeavyStrategy(Strategy, ABC):
    def __init__(self, team_budget):
        super().__init__(team_budget)
        self.budget_allocation = {
            'QB1': 13.00 * 2,
            'QB2': 1.00 * 2,
            'WR1': 27.00 * 2,
            'WR2': 10.50 * 2,
            'WR3': 6.50 * 2,
            'RB1': 24.00 * 2,
            'RB2': 5.50 * 2,
            'TE1': 0.50 * 2,
            'Flex': 5.50 * 2,
            'BN1': 1.50 * 2,
            'BN2': 1.00 * 2,
            'BN3': 0.50 * 2,
            'BN4': 2.00 * 2,
            'BN5': 1.00 * 2,
            'BN6': 0.50 * 2
        }

    def bias(self, player, bid_probability, current_bid, team):
        pos = player.get_position()
        rank = player.get_positional_rank()

        # Increase the bid probability for top 5 players in QB, WR, and RB positions
        if pos in ['QB', 'WR', 'RB'] and rank <= 5:
            bid_probability *= 1.15  # Increase by 15%
        else:
            bid_probability *= 0.85  # Decrease by 15%

        # Ensure the bid probability does not exceed 1 or fall below 0
        bid_probability = max(0, min(bid_probability, 1))

        return bid_probability
