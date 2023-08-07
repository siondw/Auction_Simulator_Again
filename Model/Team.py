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

    def add_player(self, player, cost):
        position = player.get_position()
        slot = self.find_next_available_slot(position)

        if slot and (cost <= self.max_bid):
            self.roster[slot] = player
            player.mark_as_drafted()
            self.budget -= cost
            self.set_max_bid()
        else:
            raise Exception(f"No available slot for player in position {position}")

    def find_next_available_slot(self, position):
        # Define the order of slots for each position
        slot_order = {
            'QB': ['QB1', 'QB2', 'BN1', 'BN2', 'BN3', 'BN4', 'BN5', 'BN6'],
            'RB': ['RB1', 'RB2', 'Flex', 'BN1', 'BN2', 'BN3', 'BN4', 'BN5', 'BN6'],
            'WR': ['WR1', 'WR2', 'WR3', 'Flex', 'BN1', 'BN2', 'BN3', 'BN4', 'BN5', 'BN6'],
            'TE': ['TE1', 'Flex', 'BN1', 'BN2', 'BN3', 'BN4', 'BN5', 'BN6'],
        }

        for slot in slot_order[position]:
            if not self.roster[slot]:
                return slot
        return None

    def get_qbs(self):
        return self.roster['QB']

    def get_rbs(self):
        return self.roster['RB']

    def get_wrs(self):
        return self.roster['WR']

    def get_tes(self):
        return self.roster['TE']

    def get_flex(self):
        return self.roster['Flex']

    def get_bench(self):
        return self.roster['BN']

    def get_all_players(self):
        all_players = self.get_qbs() + self.get_rbs() + self.get_wrs() + self.get_tes() + self.get_flex() + self.get_bench()
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
        return self.budget - positions_left

