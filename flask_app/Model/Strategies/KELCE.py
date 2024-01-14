from abc import ABC

from Model.Strategies.AStrategy import Strategy

class KelceStrategy(Strategy, ABC):
    def __init__(self, team_budget):
        super().__init__(team_budget)
        self.budget_allocation = {
            'QB1': 0.175 * 200,
            'QB2': 0.045 * 200,
            'WR1': 0.125 * 200,
            'WR2': 0.09 * 200,
            'WR3': 0.07 * 200,
            'RB1': 0.12 * 200,
            'RB2': 0.07 * 200,
            'TE1': 0.20 * 200,
            'Flex': 0.03 * 200,
            'BN1': 0.03 * 200,
            'BN2': 0.02 * 200,
            'BN3': 0.01 * 200,
            'BN4': 0.005 * 200,
            'BN5': 0.005 * 200,
            'BN6': 0.005 * 200
        }

    def bias(self, player, bid_probability, current_bid, team):
        pos = player.get_position()
        rank = player.get_positional_rank()

        # If the player is discounted, increase the bid probability
        if  player.get_value() < current_bid:
            bid_probability *= 1.15

        if player.get_position == 'TE' and player.positional_rank <= 2:
            bid_probability *= 1.15

        # Ensure the bid probability does not exceed 1
        bid_probability = min(bid_probability, 1)

        return bid_probability
