from .AStrategy import Strategy


class HumanStrategy(Strategy):
    def __init__(self, team_budget):
        super().__init__(team_budget)
        # Additional initialization if needed

    def calculate_bid(self, team, player, current_bid):
        raise NotImplementedError("The calculate_bid method for human players is handled in the view.")



    def bias(self, player, bid_probability, current_bid, team):
        raise NotImplementedError("The calculate_bid method for human players is handled in the view.")
