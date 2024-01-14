from .Strategies.HUMAN import HumanStrategy

class Team:

    def __init__(self, name, strategy=None):
        self.name = name
        self.budget = 200
        self.strategy = strategy
        self.max_bid = 186
        self.roster = {
            'QB1': None,
            'QB2': None,
            'RB1': None,
            'RB2': None,
            'WR1': None,
            'WR2': None,
            'WR3': None,
            'TE1': None,
            'Flex': None,
            'BN1': None,
            'BN2': None,
            'BN3': None,
            'BN4': None,
            'BN5': None,
            'BN6': None
        }

    # This method adds a player to the team in is specified slot, which is calculated
    # in the strategy class
    def add_player(self, player, cost, slot):
        if slot and (cost <= self.max_bid):
            self.roster[slot] = player
            player.mark_as_drafted()
            self.budget -= cost
            self.set_max_bid()
        else:
            raise Exception(f"No available slot for player in slot {slot}")

    def get_qbs(self):
        return [player for slot, player in self.roster.items() if slot.startswith('QB')
                and player is not None]

    def get_rbs(self):
        return [player for slot, player in self.roster.items() if slot.startswith('RB')
                and player is not None]

    def get_wrs(self):
        return [player for slot, player in self.roster.items() if slot.startswith('WR')
                and player is not None]

    def get_tes(self):
        return [player for slot, player in self.roster.items() if slot.startswith('TE')
                and player is not None]

    def get_flex(self):
        return [player for slot, player in self.roster.items() if slot.startswith('Flex')
                and player is not None]

    def get_bench(self):
        return [player for slot, player in self.roster.items() if slot.startswith('BN')
                and player is not None]

    def get_all_players(self):
        all_players = self.get_qbs()\
                      + self.get_rbs()\
                      + self.get_wrs()\
                      + self.get_tes()\
                      + self.get_flex() \
                      + self.get_bench()
        return all_players

    def get_budget(self):
        return self.budget

    def set_strategy(self, strategy):
        self.strategy = strategy

    def get_strategy(self):
        return self.strategy

    def get_max_bid(self):
        return self.max_bid

    def set_max_bid(self):
        positions_left = (sum(1 for slot, player in self.roster.items() if player is None)) - 1
        self.max_bid = self.budget - positions_left

    # gets any player in a given slot
    def get_player_by_slot(self, slot):
        return self.roster.get(slot, None)

    def calculate_bid(self, player, current_bid):
        return self.strategy.calculate_bid(self, player, current_bid)

    def determine_slot(self, player):
        return  self.strategy.determine_slot(self.roster, player)

    def is_human(self):
        return isinstance(self.strategy, HumanStrategy)
    
    def get_name(self):
        return self.name
    
    def get_roster(self):
        return self.roster

