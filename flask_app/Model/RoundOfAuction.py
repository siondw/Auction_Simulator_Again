class RoundOfAuction:
    def __init__(self, teams, player_nominated, highest_bidder):
        self.teams = teams  # These are the observers
        self.player_nominated = player_nominated
        self.current_bid = 1
        self.highest_bidder = highest_bidder

    def start_bidding(self):
        self.process_bid(self.highest_bidder, self.current_bid)

        new_bid_made = True
        while new_bid_made:
            new_bid_made = False
            self.notify_observers()

            for team in self.teams:
                if team != self.highest_bidder:
                    bid = team.update_bid(self.current_bid)  # Observer update method
                    if bid is not None and bid > self.current_bid:
                        self.process_bid(team, bid)
                        new_bid_made = True

        self.finalize_round()

    def notify_observers(self):
        for team in self.teams:
            team.update_bid(self.current_bid)  # Notify each team of the current bid

    def process_bid(self, team, bid_amount):
        self.current_bid = bid_amount
        self.highest_bidder = team

    def finalize_round(self):
        winner = self.highest_bidder
        slot = winner.determine_slot(self.player_nominated)
        winner.add_player(self.player_nominated, self.current_bid, slot)

    def summarize_round(self):
        summary = f"Player: {self.player_nominated.name}, Winning Team: {self.highest_bidder.name}, Bid: {self.current_bid}"
        return summary
