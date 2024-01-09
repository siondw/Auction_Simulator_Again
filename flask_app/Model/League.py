import random

from Model.PlayerImporter import PlayerImporter
from Model.RoundOfAuction import RoundOfAuction
from Model.Strategies.BALANCED import BalancedStrategy
from Model.Strategies.HERO_RB import HeroRBStrategy
from Model.Strategies.HUMAN import HumanStrategy
from Model.Strategies.QB_Heavy import QBHeavyStrategy
from Model.Strategies.TOP_HEAVY import TopHeavyStrategy
from Model.Strategies.UNDER_20 import Under20Strategy
from Model.Strategies.ZERO_RB import ZeroRBStrategy
from Model.Team import Team
from flask import current_app
from flask_socketio import emit



class League:
    def __init__(self, num_teams=10):
        self.teams = []
        self.players = []
        self.player_dict = {}
        self.import_players()
        self.round_summaries = []
        self.nomination_order = []
        

        # Define the available strategies and corresponding weights
        strategies = [
            BalancedStrategy,
            Under20Strategy,
            QBHeavyStrategy,
            TopHeavyStrategy,
            ZeroRBStrategy,
            HeroRBStrategy
        ]
        strategy_weights = [0.5, 0.05, 0.05, 0.085, 0.085, 0.2]

        # Field for the Human Team to make retreival easier
        self.human_team = None

        # Create the human team as Team 1
        human_team = Team(name="Team 1", strategy=HumanStrategy(team_budget=200))
        self.human_team = human_team
        self.teams.append(human_team)

        # Create the remaining computer-controlled teams
        for i in range(1, num_teams):
            # Choose a strategy randomly, based on the given weights
            chosen_strategy_class = random.choices(strategies, strategy_weights)[0]
            chosen_strategy = chosen_strategy_class(team_budget=200)

            # Create the team with the chosen strategy
            team = Team(name=f"Team {i + 1}", strategy=chosen_strategy)
            self.teams.append(team)

        self.set_nomination_order()

    def import_players(self):
        self.players = PlayerImporter.import_players_from_csv("flask_app/Resources/Players.csv")
        self.player_dict = {player.name: player for player in self.players}


    # def conduct_auction_round(self, player_nominated):
    #     # Set the nominating team as the first team in the order
    #     nominating_team = self.teams[0]

    #     # Get Player from Player Nominate method
    #     player_nominated = self.nominate_player(nominating_team)

    #     # Conduct the auction round with the nominating team as the highest bidder initially
    #     round_of_auction = RoundOfAuction(self.teams, player_nominated, nominating_team)
       
    #     emit('new_round', {
    #     'player': player_nominated.get_name(),  # Name or details of the player up for auction
    #     'user_max': self.human_team.get_max_bid(), # Max bid of the human player for this round
    #     'nominator': nominating_team.get_name()
    # }, broadcast=True)
        
    #     current_app.current_auction_round = round_of_auction
    #     round_of_auction.start_bidding()
        
    #     # Add the round summary to the list of summaries
    #     self.round_summaries.append(round_of_auction.summarize_round())

    #     # Move the nominating team to the end of the list
    #     self.teams.append(self.teams.pop(0))


    # Begins the auction round by calling on either the human or cpu to choose a player
    def initiate_auction_round(self):
        # Set the nominating team as the first team in the order
        nominating_team = self.teams[0]

        if nominating_team.name == "Team 1":  # Human team
            # For the human team, the round will continue after user input
            # So, exit the method here
            return

        # Get Player from Player Nominate method
        player_nominated = self.nominate_player(nominating_team)

        # For AI teams, continue as usual
        self.continue_auction_round(player_nominated)
    
    def continue_auction_round(self, player_nominated):
    # Assuming player_nominated is the player object or None
        if player_nominated is None:
            # Handle the case where no player is nominated (if necessary)
            return

        nominating_team = self.teams[0]

        # Conduct the auction round with the nominating team as the highest bidder initially
        round_of_auction = RoundOfAuction(self.teams, player_nominated, nominating_team)
    
     
        emit('new_round', {
        'player': player_nominated.get_name(),  # Name or details of the player up for auction
        'user_max': self.human_team.get_max_bid(), # Max bid of the human player for this round
        'nominator': nominating_team.get_name()
    }, broadcast=True)

        current_app.current_auction_round = round_of_auction
        round_of_auction.start_bidding()
        
        # Add the round summary to the list of summaries
        self.round_summaries.append(round_of_auction.summarize_round())

        # Move the nominating team to the end of the list
        self.teams.append(self.teams.pop(0))

    def get_team_roster(self, team_name):
        for team in self.teams:
            if team.name == team_name:
                return team.roster
        return None

    def set_nomination_order(self):
        self.nomination_order = random.shuffle(self.teams)
        
        

    def nominate_player(self, team):
        if team.name == "Team 1":  # Human team
            emit('prompt_nomination', {'message': 'Please nominate a player.'})
            # Rest of the logic will be handled after user input
            return None
        else:
            # Filter out drafted players
            available_players = [player for player in self.players if not player.drafted]
            
            # Consider top 15 players at each position among the available players
            top_players_count = min(15, len(available_players))  # Ensures we do not exceed the available players count
            top_players = sorted(available_players, key=lambda x: x.positional_rank)[:top_players_count]
            
            # The weights must correspond to the total number of available players
            # The top players get higher weight
            weights = [0.9] * top_players_count + [0.1] * (len(available_players) - top_players_count)

            # Randomly select a player from the list of available players
            # with a bias toward the top players at each position
            player_nominated = random.choices(available_players, weights=weights, k=1)[0]
            
        print(player_nominated)
        return player_nominated



    def get_all_players(self):
        return self.players
    
    def get_team_names(self):
        team_names = []

        for team in self.teams:
            name = team.get_name()
            team_names.append(name)

        return team_names
    
    def get_human(self):
        return self.human_team
        
    def find_player_by_name(self, name):
        return self.player_dict.get(name)
   