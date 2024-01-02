from flask_socketio import emit

class RoundOfAuction:
    def __init__(self, teams, player_nominated, highest_bidder):
        self.teams = teams  # These are the observers
        self.player_nominated = player_nominated
        self.current_bid = 1
        self.highest_bidder = highest_bidder
        self.human_player =  [team for team in self.teams if team.is_human][0]

    def start_bidding(self):
        # Initialize active bidders, excluding the human player
        active_bidders = set(self.teams) - {self.human_player}

        new_bid_made = True

        while new_bid_made:
            new_bid_made = False  # Reset the flag for the new round of bidding

            self.notify_observers()  # Notify teams of the current bid

            # Collect and process bids from active bidders only
            for team in list(active_bidders):  # Iterate over a copy of the set
                bid = team.calculate_bid(self.player_nominated, self.current_bid)
                if bid is not None and bid > self.current_bid:
                    self.process_bid(team, bid)
                    self.highest_bidder = team  # Update the highest bidder
                    new_bid_made = True  # A new bid was made, continue the loop
                else:
                    # Remove the team from active bidders if they choose not to bid
                    active_bidders.remove(team)

            # Check if only one bidder remains
            if len(active_bidders) == 1:
                # Process the final bid from the remaining bidder
                remaining_team = active_bidders.pop()
                bid = remaining_team.calculate_bid(self.player_nominated, self.current_bid)
                if bid is not None and bid > self.current_bid:
                    self.process_bid(remaining_team, bid)
                break  # End the bidding loop

        self.finalize_round()


    def notify_observers(self):
        for team in self.teams:
            team.notify_of_current_bid(self.current_bid)  # Notify each team of the current bid

    def process_bid(self, team, bid_amount):
        self.current_bid = bid_amount
        self.highest_bidder = team
        self.update_auction_state()

    def finalize_round(self):
        winner = self.highest_bidder
        slot = winner.determine_slot(self.player_nominated)
        winner.add_player(self.player_nominated, self.current_bid, slot)

    def summarize_round(self):
        summary = f"Player: {self.player_nominated.name}, Winning Team: {self.highest_bidder.name}, Bid: {self.current_bid}"
        return summary
    
        
    # Emit the new current bid and the highest bidder to all connected clients
    def update_auction_state(self):
        emit('auction_update', {
            'current_bid': self.current_bid,
            'highest_bidder': self.highest_bidder.get_name()
        })

