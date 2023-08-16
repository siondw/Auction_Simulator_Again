from abc import ABC
from Model.Strategies.AStrategy import Strategy

class ManualStrategy(Strategy, ABC):
    def __init__(self, team_budget):
        super().__init__(team_budget)

    def calculate_bid(self, team, player, current_bid, roster):
        # Prompt the user for a bid
        user_bid = int(input(f"Enter your bid for {player.name} (current bid: {current_bid}): "))

        # Validate the bid, if necessary
        if team.get_budget() >= user_bid > current_bid:
            return user_bid
        else:
            return None  # Not willing to bid or invalid bid

    def bias(self, player, bid_probability, current_bid, team):
        # The manual strategy doesn't have any automatic bias
        return bid_probability
