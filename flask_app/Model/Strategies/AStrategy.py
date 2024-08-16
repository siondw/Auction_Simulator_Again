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

        # TODO: Shift the sigmoid curve to the left
        # Calculate the probability of placing a bid -- SIGMOID!
        probability_of_bidding = 1 / (1 + np.exp(current_bid - max_bid_for_slot))
        

        # add in strategy bias
        bias_bid = self.bias(player, probability_of_bidding, current_bid, team)
        print(team.get_strategy(), "probability of bidding: ", bias_bid)

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
        position = player.get_position()
        player_value = player.get_value()
        slot_order = {
            'QB': ['QB1', 'QB2', 'BN1', 'BN2', 'BN3', 'BN4', 'BN5', 'BN6'],
            'RB': ['RB1', 'RB2', 'Flex', 'BN1', 'BN2', 'BN3', 'BN4', 'BN5', 'BN6'],
            'WR': ['WR1', 'WR2', 'WR3', 'Flex', 'BN1', 'BN2', 'BN3', 'BN4', 'BN5', 'BN6'],
            'TE': ['TE1', 'Flex', 'BN1', 'BN2', 'BN3', 'BN4', 'BN5', 'BN6'],
        }

        tolerance = 0.1  # 10% tolerance

        # Iterate through the slots in order for the player's position
        for slot in slot_order.get(position, []):
            budget_allocation = self.budget_allocation.get(slot, 0)
            
            if budget_allocation <= 10:
                threshold = budget_allocation - 1  # $1 tolerance for allocations of $10 or less
            else:
                threshold = budget_allocation - (budget_allocation * tolerance)
            
            threshold = max(0, round(threshold))  # Round to nearest dollar and ensure non-negative

            if not roster.get(slot):  # Check if the slot is empty
                if player_value >= threshold:
                    print(f"Determined Slot: {slot} (Threshold: ${threshold}, Player Value: ${player_value})")
                    return slot

        # If no slot is suitable, return None
        return None




    @abstractmethod
    def bias(self, player, bid_probability, current_bid, team):
        """
        Adjusts the current bid based on some bias. The bias can depend on the player, the current bid,
        the state of the auction, or anything else relevant.
        This method should be implemented in each subclass.
        """
        pass

# TODO:  Add budget refactoring to the strategies