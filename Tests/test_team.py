import unittest
from flask_app.Model.Strategies.HUMAN import HumanStrategy
from flask_app.Model.Strategies.BALANCED import BalancedStrategy
from flask_app.Model.Team import Team
from flask_app.Model.Player import Player

class TestTeam(unittest.TestCase):
    def setUp(self):
        self.team = Team("Testers", BalancedStrategy(200))

        self.player1 = Player(
            name="Tom Brady",
            pos="QB",
            nfl_team="TB",
            projected_points=300,
            estimated_value=40,
            positional_rank=1
        )
        self.player2 = Player(
            name="Aaron Rodgers",
            pos="QB",
            nfl_team="GB",
            projected_points=280,
            estimated_value=35,
            positional_rank=2
        )
        self.player3 = Player(
            name="John Metchie",
            pos="WR",
            nfl_team="HOU",
            projected_points=43,
            estimated_value=2,
            positional_rank=56
        )
        self.player4 = Player(
            name="Jaylen Waddle",
            pos="WR",
            nfl_team="MIA",
            projected_points=231,
            estimated_value=23,
            positional_rank=16
        )
        self.player5 = Player(
            name="Brandon Aiyuk",
            pos="WR",
            nfl_team="SF",
            projected_points=231,
            estimated_value=6,
            positional_rank=22
        )


    def test_add_player(self):
        self.team.add_player(self.player1, 50, 'QB1')
        self.assertEqual(self.team.get_player_by_slot('QB1'), self.player1)
        self.assertEqual(self.team.get_budget(), 150)

    def test_add_second_player(self):
        self.team.add_player(self.player1, 50, 'QB1')
        self.team.add_player(self.player2, 45, 'QB2')
        self.assertEqual(self.team.get_player_by_slot('QB2'), self.player2)
        self.assertEqual(self.team.get_budget(), 105)


    def test_get_player_by_slot(self):
        self.team.add_player(self.player1, 50, 'QB1')
        self.assertEqual(self.team.get_player_by_slot('QB1'), self.player1)

    def test_determine_slot(self):
        slot = self.team.determine_slot(self.player1)
        self.assertEqual(slot, 'QB1')
        slot = self.team.determine_slot(self.player3)
        self.assertEqual(slot, 'BN1')
        slot = self.team.determine_slot(self.player4)
        self.assertEqual(slot, 'WR2')
        slot = self.team.determine_slot(self.player5)
        slot.assertEqual(slot, 'BN1')

    def test_set_strategy(self):
        new_strategy = HumanStrategy(100)
        self.team.set_strategy(new_strategy)
        self.assertEqual(self.team.get_strategy(), new_strategy)

    def test_get_name(self):
        self.assertEqual(self.team.get_name(), "Testers")

    def test_get_budget(self):
        self.assertEqual(self.team.get_budget(), 200)

    def test_get_max_bid(self):
        self.assertEqual(self.team.get_max_bid(), 186)

    def test_get_all_players(self):
        self.team.add_player(self.player1, 50, 'QB1')
        self.assertEqual(self.team.get_all_players(), [self.player1])

if __name__ == '__main__':
    unittest.main()