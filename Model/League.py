import random

from Model import PlayerImporter
from Model.RoundOfAuction import RoundOfAuction
from Model.Strategies.BALANCED import BalancedStrategy
from Model.Strategies.HERO_RB import HeroRBStrategy
from Model.Strategies.HUMAN import HumanStrategy
from Model.Strategies.QB_Heavy import QBHeavyStrategy
from Model.Strategies.TOP_HEAVY import TopHeavyStrategy
from Model.Strategies.UNDER_20 import Under20Strategy
from Model.Strategies.ZERO_RB import ZeroRBStrategy
from Model.Team import Team





# Resources/Player_Data.csv
class League:
    def __init__(self, num_teams=10):
        self.teams = []
        self.players = []
        self.round_summaries = []


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

        # Create the human team as Team 1
        human_team = Team(name="Team 1", strategy=HumanStrategy(team_budget=200))
        self.teams.append(human_team)

        # Create the remaining computer-controlled teams
        for i in range(1, num_teams):
            # Choose a strategy randomly, based on the given weights
            chosen_strategy_class = random.choices(strategies, strategy_weights)[0]
            chosen_strategy = chosen_strategy_class(team_budget=200)

            # Create the team with the chosen strategy
            team = Team(name=f"Team {i + 1}", strategy=chosen_strategy)
            self.teams.append(team)

    def import_players(self):
        self.players = PlayerImporter.import_players_from_csv("Resources\\Player_Data.csv")

    def conduct_auction_round(self, player_nominated, highest_bidder_team):
        round_of_auction = RoundOfAuction(self.teams, player_nominated, highest_bidder_team)
        round_of_auction.start_bidding()
        self.rounds_summaries.append(round_of_auction.summarize_round())

    def start_draft(self):

        # Logic to start the draft, nominate players, and conduct auction rounds.
        # You can use methods like conduct_auction_round in a loop or any other logic you prefer.

    def get_team_roster(self, team_name):
        for team in self.teams:
            if team.name == team_name:
                return team.roster
        return None

