import random
from abc import ABC

from Model.Strategies.AStrategy import Strategy


class BalancedStrategy(Strategy, ABC):
    def __init__(self, team_budget):
        super().__init__(team_budget)
        self.budget_allocation = {
            'QB1': 0.085 * 200,
            'QB2': 0.075 * 200,
            'WR1': 0.145 * 200,
            'WR2': 0.07 * 200,
            'WR3': 0.095 * 200,
            'RB1': 0.19 * 200,
            'RB2': 0.195 * 200,
            'TE1': 0.02 * 200,
            'Flex': 0.06 * 200,
            'BN1': 0.04 * 200,
            'BN2': 0.005 * 200,
            'BN3': 0.005 * 200,
            'BN4': 0.005 * 200,
            'BN5': 0.005 * 200,
            'BN6': 0.005 * 200
        }

    def bias(self, player, bid_probability, current_bid, team):
        # Retrieve the player's estimated value
        estimated_value = player.get_value()

        # If the current bid is less than the player's estimated value, increase bid probability
        if current_bid < estimated_value:
            return bid_probability * random.uniform(1, 1.2)  # increase by 0% to 20% randomly
        else:
            return bid_probability  # do not increase bid probability
