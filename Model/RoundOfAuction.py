class RoundOfAuction:
    def __init__(self, teams, player_nominated, highest_bidder):
        self.teams = teams
        self.player_nominated = player_nominated
        self.current_bid = 1
        self.highest_bidder = highest_bidder

    def start_bidding(self):
        # Start the bidding with the highest bidder (the team nominating the player)
        self.process_bid(self.highest_bidder, self.current_bid)

        # Keep track of whether a new bid was made in the last loop iteration
        new_bid_made = True

        # Continue bidding until no new bids are made
        while new_bid_made:
            new_bid_made = False  # Reset for each loop iteration

            # Loop through each team and ask them to calculate their bid
            for team in self.teams:
                if team != self.highest_bidder:  # Skip the nominating team
                    bid = team.strategy.calculate_bid(team, self.player_nominated, self.current_bid, team.roster)
                    if bid is not None and bid > self.current_bid:
                        self.process_bid(team, bid)
                        new_bid_made = True  # A new bid was made, so continue the loop

        # Finalize the round by updating the winning team's roster
        self.finalize_round()

    def process_bid(self, team, bid_amount):
        # Update the current bid and the highest bidder
        self.current_bid = bid_amount
        self.highest_bidder = team

    def finalize_round(self):
        winner = self.highest_bidder
        slot = winner.determine_slot(self.player_nominated)
        winner.add_player(self.player_nominated, self.current_bid, slot)

    def summarize_round(self):
        summary = f"Player: {self.player_nominated.name}, Winning Team: {self.highest_bidder.name}, Bid: {self.current_bid}"
        return summary



