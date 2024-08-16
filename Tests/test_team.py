import unittest
import numpy as np
import random
import math

# Base Strategy class
class Strategy:
    def __init__(self, team_budget):
        self.team_budget = team_budget
        self.budget_allocation = {}
    
    def determine_slot(self, roster, player):
        position = player.pos
        player_value = player.estimated_value
        slot_order = {
            'QB': ['QB1', 'QB2', 'BN1', 'BN2', 'BN3', 'BN4', 'BN5', 'BN6'],
            'RB': ['RB1', 'RB2', 'Flex', 'BN1', 'BN2', 'BN3', 'BN4', 'BN5', 'BN6'],
            'WR': ['WR1', 'WR2', 'WR3', 'Flex', 'BN1', 'BN2', 'BN3', 'BN4', 'BN5', 'BN6'],
            'TE': ['TE1', 'Flex', 'BN1', 'BN2', 'BN3', 'BN4', 'BN5', 'BN6'],
        }

        tolerance = 0.1  # 10% tolerance

        # Iterate through the slots in order for the player's position
        for slot in slot_order.get(position, []):
            budget_allocation = self.budget_allocation.get(slot, 0)
            
            if budget_allocation <= 10:
                threshold = budget_allocation - 1  # $1 tolerance for allocations of $10 or less
            else:
                threshold = budget_allocation - (budget_allocation * tolerance)
            
            threshold = max(0, round(threshold))  # Round to nearest dollar and ensure non-negative

            if not roster.get(slot):  # Check if the slot is empty
                if player_value >= threshold:
                    print(f"Determined Slot: {slot} (Threshold: ${threshold}, Player Value: ${player_value})")
                    return slot

        # If no slot is suitable, return None
        return None

# Player and Team classes
class Player:
    def __init__(self, name, pos, nfl_team, projected_points, estimated_value, positional_rank):
        self.name = name
        self.pos = pos
        self.nfl_team = nfl_team
        self.projected_points = projected_points
        self.estimated_value = estimated_value
        self.positional_rank = positional_rank

class Team:
    def __init__(self, name, strategy=None):
        self.name = name
        self.budget = 200
        self.strategy = strategy
        self.max_bid = 186
        self.roster = {key: None for key in ['QB1', 'QB2', 'RB1', 'RB2', 'WR1', 'WR2', 'WR3', 'TE1', 'Flex', 'BN1', 'BN2', 'BN3', 'BN4', 'BN5', 'BN6']}

# Strategy Implementations
class BalancedStrategy(Strategy):
    def __init__(self, team_budget):
        super().__init__(team_budget)
        self.budget_allocation = {
            'QB1': 0.11 * 200,
            'QB2': 0.07 * 200,
            'WR1': 0.20 * 200,
            'WR2': 0.13 * 200,
            'WR3': 0.05 * 200,
            'RB1': 0.19 * 200,
            'RB2': 0.08 * 200,
            'TE1': 0.02 * 200,
            'Flex': 0.085 * 200,
            'BN1': 0.04 * 200,
            'BN2': 0.005 * 200,
            'BN3': 0.005 * 200,
            'BN4': 0.005 * 200,
            'BN5': 0.005 * 200,
            'BN6': 0.005 * 200
        }

class TopHeavyStrategy(Strategy):
    def __init__(self, team_budget):
        super().__init__(team_budget)
        self.budget_allocation = {
            'QB1': 13.00 * 2,
            'QB2': 1.00 * 2,
            'WR1': 27.00 * 2,
            'WR2': 10.50 * 2,
            'WR3': 6.50 * 2,
            'RB1': 24.00 * 2,
            'RB2': 5.50 * 2,
            'TE1': 0.50 * 2,
            'Flex': 5.50 * 2,
            'BN1': 1.50 * 2,
            'BN2': 1.00 * 2,
            'BN3': 0.50 * 2,
            'BN4': 2.00 * 2,
            'BN5': 1.00 * 2,
            'BN6': 0.50 * 2
        }
class Under20Strategy(Strategy):
    def __init__(self, team_budget):
        super().__init__(team_budget)
        self.budget_allocation = {
            'QB1': 10.00 * 2,
            'QB2': 7.50 * 2,
            'WR1': 9.50 * 2,
            'WR2': 8.50 * 2,
            'WR3': 7.50 * 2,
            'RB1': 9.50 * 2,
            'RB2': 6.00 * 2,
            'TE1': 7.50 * 2,
            'Flex': 10.00 * 2,
            'BN1': 6.00 * 2,
            'BN2': 5.00 * 2,
            'BN3': 8.00 * 2,
            'BN4': 2.50 * 2,
            'BN5': 2.00 * 2,
            'BN6': 0.50 * 2
        }

class HeroRBStrategy(Strategy):
    def __init__(self, team_budget):
        super().__init__(team_budget)
        self.budget_allocation = {
            'QB1': 11.00 * 2,
            'QB2': 8.00 * 2,
            'WR1': 22.50 * 2,
            'WR2': 9.50 * 2,
            'WR3': 4.50 * 2,
            'RB1': 28.50 * 2,
            'RB2': 7.50 * 2,
            'TE1': 2.00 * 2,
            'Flex': 3.50 * 2,
            'BN1': 0.50 * 2,
            'BN2': 0.50 * 2,
            'BN3': 0.50 * 2,
            'BN4': 0.50 * 2,
            'BN5': 0.50 * 2,
            'BN6': 0.50 * 2
        }

class ZeroRBStrategy(Strategy):
    def __init__(self, team_budget):
        super().__init__(team_budget)
        self.budget_allocation = {
            'QB1': 0.10 * 200,
            'QB2': 0.05 * 200,
            'RB1': 0.035 * 200,
            'RB2': 0.035 * 200,
            'WR1': 0.25 * 200,
            'WR2': 0.19 * 200,
            'WR3': 0.10 * 200,
            'TE1': 0.07 * 200,
            'Flex': 0.10 * 200,
            'BN1': 0.01 * 200,
            'BN2': 0.01 * 200,
            'BN3': 0.01 * 200,
            'BN4': 0.02 * 200,
            'BN5': 0.05 * 200,
            'BN6': 0.05 * 200
        }

# Test suite
class TestStrategyDeterminations(unittest.TestCase):
    def setUp(self):
        self.balanced_team = Team("Balanced Team", BalancedStrategy(200))
        self.top_heavy_team = Team("Top Heavy Team", TopHeavyStrategy(200))
        self.under20_team = Team("Under20 Team", Under20Strategy(200))
        self.hero_rb_team = Team("HeroRB Team", HeroRBStrategy(200))
        self.zero_rb_team = Team("ZeroRB Team", ZeroRBStrategy(200))

    def test_empty_balanced_high_qb(self):
        player = Player("Tom Brady", "QB", "Buccaneers", 300, 55, 1)
        slot = self.balanced_team.strategy.determine_slot(self.balanced_team.roster, player)
        self.assertEqual(slot, 'QB1')

    def test_empty_balanced_low_qb(self):
        player = Player("Backup QB", "QB", "Jets", 100, 5, 30)
        slot = self.balanced_team.strategy.determine_slot(self.balanced_team.roster, player)
        self.assertEqual(slot, 'BN2')

    def test_empty_balanced_high_rb(self):
        player = Player("Derrick Henry", "RB", "Titans", 280, 55, 1)
        slot = self.balanced_team.strategy.determine_slot(self.balanced_team.roster, player)
        self.assertEqual(slot, 'RB1')

    def test_empty_balanced_mid_rb(self):
        player = Player("Mid RB", "RB", "Dolphins", 200, 30, 15)
        slot = self.balanced_team.strategy.determine_slot(self.balanced_team.roster, player)
        self.assertEqual(slot, 'RB2')

    def test_empty_balanced_low_rb(self):
        player = Player("Low RB", "RB", "Broncos", 100, 5, 40)
        slot = self.balanced_team.strategy.determine_slot(self.balanced_team.roster, player)
        self.assertEqual(slot, 'BN2')

    def test_empty_balanced_high_wr(self):
        player = Player("Davante Adams", "WR", "Raiders", 280, 75, 1)
        slot = self.balanced_team.strategy.determine_slot(self.balanced_team.roster, player)
        self.assertEqual(slot, 'WR1')

    def test_empty_balanced_mid_wr(self):
        player = Player("Mid WR", "WR", "Seahawks", 220, 40, 15)
        slot = self.balanced_team.strategy.determine_slot(self.balanced_team.roster, player)
        self.assertEqual(slot, 'WR1')

    def test_empty_balanced_low_wr(self):
        player = Player("Low WR", "WR", "Bears", 150, 15, 40)
        slot = self.balanced_team.strategy.determine_slot(self.balanced_team.roster, player)
        self.assertEqual(slot, 'WR3')

    def test_empty_balanced_te(self):
        player = Player("George Kittle", "TE", "49ers", 200, 30, 3)
        slot = self.balanced_team.strategy.determine_slot(self.balanced_team.roster, player)
        self.assertEqual(slot, 'TE1')

    def test_empty_top_heavy_high_qb(self):
        player = Player("Patrick Mahomes", "QB", "Chiefs", 350, 60, 1)
        slot = self.top_heavy_team.strategy.determine_slot(self.top_heavy_team.roster, player)
        self.assertEqual(slot, 'QB1')

    def test_empty_top_heavy_low_qb(self):
        player = Player("Backup QB", "QB", "Colts", 80, 2, 35)
        slot = self.top_heavy_team.strategy.determine_slot(self.top_heavy_team.roster, player)
        self.assertEqual(slot, 'QB2')

    def test_empty_top_heavy_high_rb(self):
        player = Player("Christian McCaffrey", "RB", "Panthers", 300, 80, 1)
        slot = self.top_heavy_team.strategy.determine_slot(self.top_heavy_team.roster, player)
        self.assertEqual(slot, 'RB1')

    def test_empty_top_heavy_low_rb(self):
        player = Player("Low RB", "RB", "Bills", 120, 8, 35)
        slot = self.top_heavy_team.strategy.determine_slot(self.top_heavy_team.roster, player)
        self.assertEqual(slot, 'BN1')

    def test_empty_top_heavy_high_wr(self):
        player = Player("Cooper Kupp", "WR", "Rams", 320, 90, 1)
        slot = self.top_heavy_team.strategy.determine_slot(self.top_heavy_team.roster, player)
        self.assertEqual(slot, 'WR1')

    def test_empty_top_heavy_mid_wr(self):
        player = Player("Mid WR", "WR", "Packers", 200, 35, 20)
        slot = self.top_heavy_team.strategy.determine_slot(self.top_heavy_team.roster, player)
        self.assertEqual(slot, 'WR2')

    def test_empty_top_heavy_low_wr(self):
        player = Player("Low WR", "WR", "Jaguars", 140, 12, 45)
        slot = self.top_heavy_team.strategy.determine_slot(self.top_heavy_team.roster, player)
        self.assertEqual(slot, 'WR3')

    def test_empty_top_heavy_te(self):
        player = Player("Travis Kelce", "TE", "Chiefs", 240, 50, 1)
        slot = self.top_heavy_team.strategy.determine_slot(self.top_heavy_team.roster, player)
        self.assertEqual(slot, 'TE1')

    def test_filled_balanced_team(self):
        self.balanced_team.roster['QB1'] = Player("QB1", "QB", "Team1", 300, 50, 1)
        self.balanced_team.roster['RB1'] = Player("RB1", "RB", "Team2", 280, 60, 1)
        player = Player("New QB", "QB", "Team3", 290, 48, 2)
        slot = self.balanced_team.strategy.determine_slot(self.balanced_team.roster, player)
        self.assertEqual(slot, 'QB2')

    def test_filled_top_heavy_team(self):
        self.top_heavy_team.roster['WR1'] = Player("WR1", "WR", "Team1", 320, 80, 1)
        self.top_heavy_team.roster['WR2'] = Player("WR2", "WR", "Team2", 280, 60, 5)
        player = Player("New WR", "WR", "Team3", 250, 40, 15)
        slot = self.top_heavy_team.strategy.determine_slot(self.top_heavy_team.roster, player)
        self.assertEqual(slot, 'WR3')

    def test_filled_qb1_balanced(self):
        self.balanced_team.roster['QB1'] = Player("Existing QB1", "QB", "Team1", 300, 50, 1)
        player = Player("New QB", "QB", "Team2", 290, 48, 2)
        slot = self.balanced_team.strategy.determine_slot(self.balanced_team.roster, player)
        self.assertEqual(slot, 'QB2')

    def test_filled_qb1_qb2_balanced(self):
        self.balanced_team.roster['QB1'] = Player("Existing QB1", "QB", "Team1", 300, 50, 1)
        self.balanced_team.roster['QB2'] = Player("Existing QB2", "QB", "Team2", 250, 30, 10)
        player = Player("New QB", "QB", "Team3", 280, 45, 5)
        slot = self.balanced_team.strategy.determine_slot(self.balanced_team.roster, player)
        self.assertEqual(slot, 'BN1')

    def test_filled_rb1_balanced(self):
        self.balanced_team.roster['RB1'] = Player("Existing RB1", "RB", "Team1", 280, 60, 1)
        player = Player("New RB", "RB", "Team2", 270, 58, 2)
        slot = self.balanced_team.strategy.determine_slot(self.balanced_team.roster, player)
        self.assertEqual(slot, 'RB2')

    def test_filled_rb1_rb2_balanced(self):
        self.balanced_team.roster['RB1'] = Player("Existing RB1", "RB", "Team1", 280, 60, 1)
        self.balanced_team.roster['RB2'] = Player("Existing RB2", "RB", "Team2", 250, 40, 10)
        player = Player("New RB", "RB", "Team3", 260, 50, 5)
        slot = self.balanced_team.strategy.determine_slot(self.balanced_team.roster, player)
        self.assertEqual(slot, 'Flex')

    def test_filled_wr1_balanced(self):
        self.balanced_team.roster['WR1'] = Player("Existing WR1", "WR", "Team1", 300, 70, 1)
        player = Player("New WR", "WR", "Team2", 290, 65, 2)
        slot = self.balanced_team.strategy.determine_slot(self.balanced_team.roster, player)
        self.assertEqual(slot, 'WR2')

    def test_filled_wr1_wr2_balanced(self):
        self.balanced_team.roster['WR1'] = Player("Existing WR1", "WR", "Team1", 300, 70, 1)
        self.balanced_team.roster['WR2'] = Player("Existing WR2", "WR", "Team2", 270, 55, 5)
        player = Player("New WR", "WR", "Team3", 280, 60, 3)
        slot = self.balanced_team.strategy.determine_slot(self.balanced_team.roster, player)
        self.assertEqual(slot, 'WR3')

    def test_filled_wr1_wr2_wr3_balanced(self):
        self.balanced_team.roster['WR1'] = Player("Existing WR1", "WR", "Team1", 300, 70, 1)
        self.balanced_team.roster['WR2'] = Player("Existing WR2", "WR", "Team2", 270, 55, 5)
        self.balanced_team.roster['WR3'] = Player("Existing WR3", "WR", "Team3", 250, 40, 15)
        player = Player("New WR", "WR", "Team4", 260, 45, 10)
        slot = self.balanced_team.strategy.determine_slot(self.balanced_team.roster, player)
        self.assertEqual(slot, 'Flex')

    def test_filled_te1_balanced(self):
        self.balanced_team.roster['TE1'] = Player("Existing TE1", "TE", "Team1", 220, 35, 1)
        player = Player("New TE", "TE", "Team2", 210, 30, 2)
        slot = self.balanced_team.strategy.determine_slot(self.balanced_team.roster, player)
        self.assertEqual(slot, 'Flex')

    def test_filled_qb1_top_heavy(self):
        self.top_heavy_team.roster['QB1'] = Player("Existing QB1", "QB", "Team1", 350, 60, 1)
        player = Player("New QB", "QB", "Team2", 340, 58, 2)
        slot = self.top_heavy_team.strategy.determine_slot(self.top_heavy_team.roster, player)
        self.assertEqual(slot, 'QB2')

    def test_filled_rb1_top_heavy(self):
        self.top_heavy_team.roster['RB1'] = Player("Existing RB1", "RB", "Team1", 300, 80, 1)
        player = Player("New RB", "RB", "Team2", 290, 75, 2)
        slot = self.top_heavy_team.strategy.determine_slot(self.top_heavy_team.roster, player)
        self.assertEqual(slot, 'RB2')

    def test_filled_wr1_wr2_top_heavy(self):
        self.top_heavy_team.roster['WR1'] = Player("Existing WR1", "WR", "Team1", 320, 90, 1)
        self.top_heavy_team.roster['WR2'] = Player("Existing WR2", "WR", "Team2", 290, 70, 3)
        player = Player("New WR", "WR", "Team3", 300, 75, 2)
        slot = self.top_heavy_team.strategy.determine_slot(self.top_heavy_team.roster, player)
        self.assertEqual(slot, 'WR3')

    def test_all_positions_filled_balanced(self):
        positions = ['QB1', 'QB2', 'RB1', 'RB2', 'WR1', 'WR2', 'WR3', 'TE1', 'Flex']
        for pos in positions:
            self.balanced_team.roster[pos] = Player(f"Existing {pos}", pos.rstrip('123'), f"Team{pos}", 200, 30, 1)
        player = Player("New Player", "RB", "NewTeam", 250, 40, 5)
        slot = self.balanced_team.strategy.determine_slot(self.balanced_team.roster, player)
        self.assertEqual(slot, 'BN1')

    def test_all_positions_filled_top_heavy(self):
        positions = ['QB1', 'QB2', 'RB1', 'RB2', 'WR1', 'WR2', 'WR3', 'TE1', 'Flex']
        for pos in positions:
            self.top_heavy_team.roster[pos] = Player(f"Existing {pos}", pos.rstrip('123'), f"Team{pos}", 200, 30, 1)
        player = Player("New Player", "WR", "NewTeam", 280, 60, 5)
        slot = self.top_heavy_team.strategy.determine_slot(self.top_heavy_team.roster, player)
        self.assertEqual(slot, 'BN1')

    # Under20 Strategy Tests
    def test_under20_qb_allocation(self):
        player = Player("Good QB", "QB", "Team1", 280, 19, 5)
        slot = self.under20_team.strategy.determine_slot(self.under20_team.roster, player)
        self.assertEqual(slot, 'QB1')

    def test_under20_rb_allocation(self):
        player = Player("Decent RB", "RB", "Team2", 220, 18, 15)
        slot = self.under20_team.strategy.determine_slot(self.under20_team.roster, player)
        self.assertEqual(slot, 'RB1')

    def test_under20_wr_allocation(self):
        player = Player("Solid WR", "WR", "Team3", 240, 17, 20)
        slot = self.under20_team.strategy.determine_slot(self.under20_team.roster, player)
        self.assertEqual(slot, 'WR1')

    def test_under20_te_allocation(self):
        player = Player("Good TE", "TE", "Team4", 200, 14, 5)
        slot = self.under20_team.strategy.determine_slot(self.under20_team.roster, player)
        self.assertEqual(slot, 'TE1')

    # HeroRB Strategy Tests
    def test_hero_rb_rb1_allocation(self):
        player = Player("Star RB", "RB", "Team1", 320, 55, 1)
        slot = self.hero_rb_team.strategy.determine_slot(self.hero_rb_team.roster, player)
        self.assertEqual(slot, 'RB1')

    def test_hero_rb_wr1_allocation(self):
        player = Player("Top WR", "WR", "Team2", 300, 44, 2)
        slot = self.hero_rb_team.strategy.determine_slot(self.hero_rb_team.roster, player)
        self.assertEqual(slot, 'WR1')

    def test_hero_rb_qb_allocation(self):
        player = Player("Solid QB", "QB", "Team3", 270, 21, 8)
        slot = self.hero_rb_team.strategy.determine_slot(self.hero_rb_team.roster, player)
        self.assertEqual(slot, 'QB1')

    def test_hero_rb_te_allocation(self):
        player = Player("Budget TE", "TE", "Team4", 180, 3, 15)
        slot = self.hero_rb_team.strategy.determine_slot(self.hero_rb_team.roster, player)
        self.assertEqual(slot, 'TE1')

    # ZeroRB Strategy Tests
    def test_zero_rb_wr1_allocation(self):
        player = Player("Elite WR", "WR", "Team1", 320, 49, 1)
        slot = self.zero_rb_team.strategy.determine_slot(self.zero_rb_team.roster, player)
        self.assertEqual(slot, 'WR1')

    def test_zero_rb_wr2_allocation(self):
        player = Player("Great WR", "WR", "Team2", 290, 37, 5)
        slot = self.zero_rb_team.strategy.determine_slot(self.zero_rb_team.roster, player)
        self.assertEqual(slot, 'WR2')

    def test_zero_rb_rb_allocation(self):
        player = Player("Budget RB", "RB", "Team3", 200, 6, 30)
        slot = self.zero_rb_team.strategy.determine_slot(self.zero_rb_team.roster, player)
        self.assertEqual(slot, 'RB1')

    def test_zero_rb_qb_allocation(self):
        player = Player("Good QB", "QB", "Team4", 260, 19, 10)
        slot = self.zero_rb_team.strategy.determine_slot(self.zero_rb_team.roster, player)
        self.assertEqual(slot, 'QB1')

    # Additional tests for filled positions
    def test_under20_filled_positions(self):
        self.under20_team.roster['QB1'] = Player("Existing QB1", "QB", "Team1", 270, 18, 7)
        player = Player("New QB", "QB", "Team2", 265, 17, 8)
        slot = self.under20_team.strategy.determine_slot(self.under20_team.roster, player)
        self.assertEqual(slot, 'QB2')

    def test_hero_rb_filled_rb1(self):
        self.hero_rb_team.roster['RB1'] = Player("Star RB", "RB", "Team1", 320, 55, 1)
        player = Player("Good RB", "RB", "Team2", 280, 40, 5)
        slot = self.hero_rb_team.strategy.determine_slot(self.hero_rb_team.roster, player)
        self.assertEqual(slot, 'RB2')

    def test_zero_rb_filled_wr_positions(self):
        self.zero_rb_team.roster['WR1'] = Player("Elite WR", "WR", "Team1", 320, 49, 1)
        self.zero_rb_team.roster['WR2'] = Player("Great WR", "WR", "Team2", 290, 37, 5)
        player = Player("Good WR", "WR", "Team3", 260, 30, 15)
        slot = self.zero_rb_team.strategy.determine_slot(self.zero_rb_team.roster, player)
        self.assertEqual(slot, 'WR3')

if __name__ == '__main__':
    unittest.main()