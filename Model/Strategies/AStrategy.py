from abc import ABC, abstractmethod
import numpy as np
import random


class Strategy(ABC):

    def __init__(self):
        self.budget_allocation = {
            'QB1': 0,
            'QB2': 0,
            'RB1': 0,
            'RB2': 0,
            'WR1': 0,
            'WR2': 0,
            'WR3': 0,
            'TE1': 0,
            'Flex': 0,
            'BN1': 0,
            'BN2': 0,
            'BN3': 0,
            'BN4': 0,
            'BN5': 0,
            'BN6': 0
        }

    def calculate_bid(self, team, player, current_bid, roster):
        # Determine the appropriate slot for the player
        slot = self.determine_slot(roster, player.get_position())

        # Get the maximum budget for the slot
        max_bid = self.budget_allocation[slot] * team.budget

        # Calculate the probability of placing a bid
        probability_of_bidding = 1 / (1 + np.exp(current_bid - max_bid))

        # Decide whether to place a bid
        if random.random() <= probability_of_bidding:
            # Bid slightly higher than the current bid
            return current_bid + 1
        else:
            return None  # Not willing to bid

    @abstractmethod
    def determine_slot(self, roster, position):
        pass
