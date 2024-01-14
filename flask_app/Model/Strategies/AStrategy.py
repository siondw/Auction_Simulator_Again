from abc import ABC, abstractmethod
import numpy as np
import random
import math


class Strategy(ABC):

    def __init__(self, team_budget):
        self.team_budget = team_budget
        self.budget_allocation = {
            'QB1': 0 * 200,
            'QB2': 0 * 200,
            'RB1': 0 * 200,
            'RB2': 0 * 200,
            'WR1': 0 * 200,
            'WR2': 0 * 200,
            'WR3': 0 * 200,
            'TE1': 0 * 200,
            'Flex': 0 * 200,
            'BN1': 0 * 200,
            'BN2': 0 * 200,
            'BN3': 0 * 200,
            'BN4': 0 * 200,
            'BN5': 0 * 200,
            'BN6': 0 * 200,
        }

    def calculate_bid(self, team, player, current_bid):
        roster = team.roster
        # Determine the appropriate slot for the player
        slot = self.determine_slot(roster, player)

        # If there's no available slot, do not place a bid
        if slot is None:
            return None

        # Get the maximum budget for the slot
        max_bid_for_slot = self.budget_allocation[slot]

        if max_bid_for_slot == 1:
            if current_bid > 1:
                return None

        max_bid_allowed = team.get_max_bid()

        # Calculate the probability of placing a bid
        probability_of_bidding = 1 / (1 + np.exp(current_bid - max_bid_for_slot))

        # add in strategy bias
        bias_bid = self.bias(player, probability_of_bidding, current_bid, team)

        # Decide whether to place a bid
        if random.random() <= bias_bid and current_bid + 1 < max_bid_allowed:
            # Bid slightly higher than the current bid
            if current_bid < (math.floor(player.get_value() / 2)):
                return math.floor(player.get_value() / 2)
            else:
                return math.floor(current_bid + 1)
        else:
            return None  # Not willing to bid

    def determine_slot(self, roster, player):

        # Retrieve the player's position and value
        position = player.get_position()
        player_value = player.get_value()

        # Define the order of slots for each position
        slot_order = {
            'QB': ['QB1', 'QB2', 'BN1', 'BN2', 'BN3', 'BN4', 'BN5', 'BN6'],
            'RB': ['RB1', 'RB2', 'Flex', 'BN1', 'BN2', 'BN3', 'BN4', 'BN5', 'BN6'],
            'WR': ['WR1', 'WR2', 'WR3', 'Flex', 'BN1', 'BN2', 'BN3', 'BN4', 'BN5', 'BN6'],
            'TE': ['TE1', 'Flex', 'BN1', 'BN2', 'BN3', 'BN4', 'BN5', 'BN6'],
        }

        # Set a 20% tolerance on the expected value
        tolerance = 0.2  # 20% tolerance

        # Iterate through the slots in order for the player's position
        for slot in slot_order[position]:
            # Calculate the expected value for the slot based on the budget allocation
            ev = self.budget_allocation[slot]

            # Check if the slot is empty
            if not roster[slot]:
                # Check if the player's value is above the minimum tolerance for the slot
                if player_value >= (ev - ev * tolerance):
                    return slot  # Assign to this slot

        # Fallback: find the first empty slot regardless of value
        for slot in slot_order[position]:
            if not roster[slot]:
                return slot

        # If no empty slot is found, return None
        return None

    @abstractmethod
    def bias(self, player, bid_probability, current_bid, team):
        """
        Adjusts the current bid based on some bias. The bias can depend on the player, the current bid,
        the state of the auction, or anything else relevant.
        This method should be implemented in each subclass.
        """
        pass
