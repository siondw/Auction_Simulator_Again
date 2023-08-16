from abc import ABC

from Model.Strategies.AStrategy import Strategy


class HeroRBStrategy(Strategy, ABC):
    def __init__(self, team_budget):
        super().__init__(team_budget)
        self.budget_allocation = {
            'QB1': 11.00 * 2,
            'QB2': 8.00 * 2,
            'WR1': 22.50 * 2,
            'WR2': 9.50 * 2,
            'WR3': 4.50 * 2,
            'RB1': 28.50 * 2,
            'RB2': 7.50 * 2,
            'TE1': 2.00 * 2,
            'Flex': 3.50 * 2,
            'BN1': 0.50 * 2,
            'BN2': 0.50 * 2,
            'BN3': 0.50 * 2,
            'BN4': 0.50 * 2,
            'BN5': 0.50 * 2,
            'BN6': 0.50 * 2
        }

    def bias(self, player, bid_probability, current_bid, team):
        pos = player.get_position()
        rank = player.get_positional_rank()
        rb1_player = team.get_player_from_slot('RB1')

        if rb1_player is None and pos == 'RB' and rank >= 3:
            # Increase the bid probability by 10%
            bid_probability *= 1.10

            # Ensure the bid probability does not exceed 1
            bid_probability = min(bid_probability, 1)

        return bid_probability
