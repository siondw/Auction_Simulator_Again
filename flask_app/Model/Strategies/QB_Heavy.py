from abc import ABC

from Model.Strategies.AStrategy import Strategy


class QBHeavyStrategy(Strategy, ABC):
    def __init__(self, team_budget):
        super().__init__(team_budget)
        self.budget_allocation = {
            'QB1': 0.175 * 200,  # 17.5%
            'QB2': 0.125 * 200,  # 12.5%
            'RB1': 0.10 * 200,  # 10%
            'RB2': 0.11 * 200,  # 11%
            'WR1': 0.10 * 200,  # 10%
            'WR2': 0.085 * 200,  # 8.5%
            'WR3': 0.10 * 200,  # 10%
            'TE1': 0.01 * 200,  # 1%
            'Flex': 0.09 * 200,  # 9%
            'BN1': 0.0175 * 200,  # 1.75%
            'BN2': 0.0175 * 200,  # 1.75%
            'BN3': 0.0175 * 200,  # 1.75%
            'BN4': 0.0175 * 200,  # 1.75%
            'BN5': 0.0175 * 200,  # 1.75%
            'BN6': 0.0175 * 200,  # 1.75%
        }

    def bias(self, player, bid_probability, current_bid, team):
        pos = player.get_position()
        rank = player.get_positional_rank()

        # If the player is a top 5 quarterback, increase the bid probability
        if pos == 'QB' and rank <= 5:
            bid_probability *= 1.15  # increase by 15%

        # Ensure the bid probability does not exceed 1
        bid_probability = min(bid_probability, 1)

        return bid_probability

