import random

from .PlayerImporter import PlayerImporter
from .RoundOfAuction import RoundOfAuction
from .Strategies.BALANCED import BalancedStrategy
from .Strategies.HERO_RB import HeroRBStrategy
from .Strategies.HUMAN import HumanStrategy
from .Strategies.QB_Heavy import QBHeavyStrategy
from .Strategies.TOP_HEAVY import TopHeavyStrategy
from .Strategies.UNDER_20 import Under20Strategy
from .Strategies.ZERO_RB import ZeroRBStrategy
from .Strategies.KELCE import KelceStrategy
from .Team import Team
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
        
        # Strategy caps
        strategy_caps = {
            BalancedStrategy: float('inf'),  # No cap
            Under20Strategy: 1,
            QBHeavyStrategy: 2,
            TopHeavyStrategy: 2,
            ZeroRBStrategy: 2,
            HeroRBStrategy: 3,
        }

        # Initialize strategy usage counters
        strategy_usage = {strategy: 0 for strategy in strategy_caps}


        # Define the available strategies and corresponding weights
        strategies = [
            BalancedStrategy,
            Under20Strategy,
            QBHeavyStrategy,
            TopHeavyStrategy,
            ZeroRBStrategy,
            HeroRBStrategy,
        ]
        strategy_weights = [0.5, 0.05, 0.05, 0.05, 0.085, 0.2]

        # Field for the Human Team to make retreival easier
        self.human_team = None

        # Create the human team as Team 1
        human_team = Team(name="Team 1", strategy=HumanStrategy(team_budget=200))
        self.human_team = human_team
        self.teams.append(human_team)

        # Create the remaining computer-controlled teams
        for i in range(1, num_teams):
            # Adjust strategies and weights based on usage
            available_strategies = [s for s in strategies if strategy_usage[s] < strategy_caps[s]]
            adjusted_weights = [strategy_weights[strategies.index(s)] for s in available_strategies]

            # Choose a strategy randomly from the available strategies
            chosen_strategy_class = random.choices(available_strategies, adjusted_weights)[0]
            strategy_usage[chosen_strategy_class] += 1  # Increment

            # Create the team with the chosen strategy
            team_name = f"Team {i + 1}"
            team = Team(name=team_name, strategy=chosen_strategy_class(team_budget=200))
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
            emit('prompt_nomination', {'message': 'Please nominate a player.'})
            # And then exit the method here and wait for the human to nominate a player
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
                return team.get_roster()
        return None

    def set_nomination_order(self):
        random.shuffle(self.teams)
        self.nomination_order = self.teams.copy()
        
        
        

    def nominate_player(self, team):
        """
        Nominate a player from the available players based on the team's name.
        Parameters:
        - team (Team): The team object representing the team making the nomination.
        Returns:
        - player_nominated (Player): The nominated player object.
        Raises:
        - None
        """
        if team.name == "Team 1":  # Human team
            emit('prompt_nomination', {'message': 'Please nominate a player.'})
            print("Waiting for user input")
            # Rest of the logic will be handled after user input
            return None
        else:
                
            available_players = [player for player in self.players if not player.drafted]

            # Filter and take top players based on position
            top_qbs = sorted([player for player in available_players if player.pos == 'QB'], key=lambda x: x.positional_rank)[:20]
            top_wrs = sorted([player for player in available_players if player.pos == 'WR'], key=lambda x: x.positional_rank)[:35]
            top_rbs = sorted([player for player in available_players if player.pos == 'RB'], key=lambda x: x.positional_rank)[:25]
            top_tes = sorted([player for player in available_players if player.pos == 'TE'], key=lambda x: x.positional_rank)[:5]

            # Combine all top players into a single list
            top_players = top_qbs + top_wrs + top_rbs + top_tes

            # Randomly select a player from the top players list
            player_nominated = random.choice(top_players) 

        print(player_nominated)
        return player_nominated

    def get_all_players(self):
        return self.players
    
    def get_team_names(self):
        # Initialize an empty list to store team names
        team_names = []

        # Iterate over each team in the league
        for team in self.teams:
            # Get the name of the team using the get_name() method
            name = team.get_name()

            # Append the team name to the list
            team_names.append(name)

        # Return the list of team names
        return team_names
    
    def get_human(self):
        return self.human_team
        
    def find_player_by_name(self, name):
        return self.player_dict.get(name)
   