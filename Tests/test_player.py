import unittest

from flask_app.Model.Player import Player


class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.player = Player(
            name="Tom Brady",
            pos="QB",
            nfl_team="TB",
            projected_points=300,
            estimated_value=40,
            positional_rank=1
        )

    def test_initialization(self):
        self.assertEqual(self.player.name, "Tom Brady")
        self.assertEqual(self.player.pos, "QB")
        self.assertEqual(self.player.nfl_team, "TB")
        self.assertEqual(self.player.projected_points, 300)
        self.assertEqual(self.player.estimated_value, 40)
        self.assertEqual(self.player.positional_rank, 1)
        self.assertFalse(self.player.drafted)

    def test_str_representation(self):
        self.assertEqual(str(self.player), "Tom Brady (QB, TB)")

    def test_get_name(self):
        self.assertEqual(self.player.get_name(), "Tom Brady")

    def test_get_position(self):
        self.assertEqual(self.player.get_position(), "QB")

    def test_get_team(self):
        self.assertEqual(self.player.get_team(), "TB")

    def test_get_projected_points(self):
        self.assertEqual(self.player.get_projected_points(), 300)

    def test_mark_as_drafted(self):
        self.player.mark_as_drafted()
        self.assertTrue(self.player.is_drafted())

    def test_get_value(self):
        self.assertEqual(self.player.get_value(), 40)

    def test_get_positional_rank(self):
        self.assertEqual(self.player.get_positional_rank(), 1)

if __name__ == '__main__':
    unittest.main()
