from flask_socketio import emit
import time

class RoundOfAuction:
    def __init__(self, teams, player_nominated, highest_bidder):
        self.teams = teams  # These are the observers
        self.player_nominated = player_nominated
        self.current_bid = 1
        self.highest_bidder = highest_bidder
        self.human_player =  [team for team in self.teams if team.is_human()][0]
        self.isHumanInterested = True

    def start_bidding(self):
        # Initialize active bidders, excluding the human player
        active_bidders = set(self.teams) - {self.human_player}
        
        for team in active_bidders:
            print("Team Name: ", team.get_name(), "Strategy: ", team.get_strategy())

        new_bid_made = True

        while new_bid_made or self.isHumanInterested:
            # print("Bidder Remaining: " + str(len(active_bidders)))

            new_bid_made = False  # Reset the flag for the new round of bidding

             # Check if only human bidder remains
            if len(active_bidders) == 0:
                break  # End the bidding loop
            
            # Check if only one cpu bidder remains
            if len(active_bidders) == 1 and not self.isHumanInterested:
                break # End the bidding loop

            # Collect and process bids from active bidders only
            for team in list(active_bidders):  # Iterate over a copy of the set
                if team == self.highest_bidder: 
                    continue

                if team.is_human():
                    continue  # Skip the human player

                bid = team.calculate_bid(self.player_nominated, self.current_bid)
                
                if bid is not None and bid > self.current_bid:
                    self.process_bid(team, bid)
                    time.sleep(1)
                    self.highest_bidder = team  # Update the highest bidder
                    new_bid_made = True  # A new bid was made, continue the loop
                else:
                    # Remove the team from active bidders if they choose not to bid
                    active_bidders.remove(team)

           

        self.finalize_round()


    def notify_observers(self):
        for team in self.teams:
            team.notify_of_current_bid(self.current_bid)  # Notify each team of the current bid

    def process_bid(self, team, bid_amount):
        print(f"Processing bid of {bid_amount} from {team.get_name()}")
        self.current_bid = bid_amount
        self.highest_bidder = team
        self.update_auction_state()

    def finalize_round(self):
        winner = self.highest_bidder
        slot = winner.determine_slot(self.player_nominated)
        winner.add_player(self.player_nominated, self.current_bid, slot)
        print("round over")

        emit('round_over', {
        }, broadcast=True)
        

    def summarize_round(self):
        summary = f"Player: {self.player_nominated.name}, Winning Team: {self.highest_bidder.name}, Bid: {self.current_bid}"
        return summary
    
    def set_isHumanInterested(self, value):
        self.isHumanInterested = value
        
    # Emit the new current bid and the highest bidder to all connected clients
    def update_auction_state(self):
        print("Updating auction state")
        emit('auction_update', {
            'current_bid': self.current_bid,
            'highest_bidder': self.highest_bidder.get_name()
        })

    

