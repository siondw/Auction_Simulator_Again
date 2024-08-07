import random
from math import exp
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
        estimated_value = player.get_value()
        
        # Calculate the percentage difference between current bid and estimated value
        percentage_diff = (current_bid - estimated_value) / estimated_value
        
        # Generate a random initial boost between 0.0 and 0.6
        initial_boost = random.uniform(0.0, 0.6)
        
        # Apply the adjusted sigmoid function to modulate the boost
        adjustment_factor = 1 / (1 + exp(4 * (percentage_diff + 0.25)))
        
        # Calculate the new bid probability by adding the adjusted initial boost
        new_bid_probability = bid_probability + initial_boost * adjustment_factor
        
        # Ensure the new bid probability does not exceed 1
        new_bid_probability = min(new_bid_probability, 1)
        
        return new_bid_probability
