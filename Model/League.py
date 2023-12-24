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


class League:
    def __init__(self, num_teams=10):
        self.teams = []
        self.players = []
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

        self.set_nomination_order()

    def import_players(self):
        self.players = PlayerImporter.import_players_from_csv(r"C:\Users\Ccdwe\PycharmProjects\pythonProject1\Resources\Players.csv")

    def conduct_auction_round(self, player_nominated, highest_bidder_team):
        round_of_auction = RoundOfAuction(self.teams, player_nominated, highest_bidder_team)
        round_of_auction.start_bidding()
        self.round_summaries.append(round_of_auction.summarize_round())

    def get_team_roster(self, team_name):
        for team in self.teams:
            if team.name == team_name:
                return team.roster
        return None

    def set_nomination_order(self):
        # Shuffle the teams to create a random nomination order
        self.nomination_order = self.teams.copy()
        random.shuffle(self.nomination_order)

    # def nominate_player(self, team):
        # if team.name == "Team 1":  # Human team
        #     # Logic to ask the user to select a player to nominate
        #     # You may want to integrate with the view to display the options
        #     player_nominated = get_user_selected_player()
        # else:
        #     # Filter out drafted players
        #     available_players = [player for player in self.players if not player.drafted]
        #
        #     # Consider top 15 players at each position among the available players
        #     top_players = sorted(available_players, key=lambda x: x.positional_rank)[:15]
        #
        #     # Randomly select a player from the list of available players
        #     # with a bias toward the top 15 at each position
        #     player_nominated = random.choices(top_players + available_players,
        #                                       weights=[0.6] * 15 + [0.4] * (len(available_players) - 15), k=1)[0]
        #
        # return player_nominated

    def get_all_players(self):
        return self.players
