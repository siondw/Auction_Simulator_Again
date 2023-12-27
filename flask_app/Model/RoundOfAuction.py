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
            new_bid_made = False  # Reset the flag for the new round of bidding

            self.notify_observers()  # Notify teams of the current bid

            # Collect and process bids
            for team in self.teams:
                if team != self.highest_bidder:
                    bid = team.calculate_bid(self.player_nominated, self.current_bid)
                    if bid is not None and bid > self.current_bid:
                        self.process_bid(team, bid)
                        new_bid_made = True  # A new bid was made, continue the loop

        self.finalize_round()

    def notify_observers(self):
        for team in self.teams:
            team.notify_of_current_bid(self.current_bid)  # Notify each team of the current bi

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
