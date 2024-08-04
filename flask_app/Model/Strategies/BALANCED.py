import random
import math
from abc import ABC

from .AStrategy import Strategy


class BalancedStrategy(Strategy, ABC):
    def __init__(self, team_budget):
        super().__init__(team_budget)
        self.budget_allocation = {
            'QB1': 0.11 * 200,
            'QB2': 0.07 * 200,
            'WR1': 0.20 * 200,
            'WR2': 0.13 * 200,
            'WR3': 0.05 * 200,
            'RB1': 0.19 * 200,
            'RB2': 0.08 * 200,
            'TE1': 0.02 * 200,
            'Flex': 0.085 * 200,
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

        #TODO: Fix the Bias Probaibltiy to be addition instead of subtraction
        # If the current bid is less than the player's estimated value, increase bid probability
        if current_bid < estimated_value:
            return bid_probability * random.uniform(1.1, 1.4)  # increase by 0% to 40% randomly
        else:
            return bid_probability  # do not increase bid probability
