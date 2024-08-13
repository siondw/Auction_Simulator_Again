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
            self.refactor_budget(cost, slot)
            # self.strategy.add_player(self, player, cost)
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
    


    def refactor_budget(self, cost, slot):
        if slot in self.strategy.budget_allocation:
            allocated_budget = self.strategy.budget_allocation[slot]
            remaining_budget = allocated_budget - cost

            if remaining_budget > 0:  # Handle underspend
                position_category = slot[:2]  # e.g., 'WR', 'RB', 'QB'
                related_positions = [pos for pos in self.strategy.budget_allocation.keys() if pos.startswith(position_category) and pos != slot]

                remaining_to_category = round(0.7 * remaining_budget, 2)
                remaining_to_bench = round(0.3 * remaining_budget, 2)

                total_related_allocation = sum(self.strategy.budget_allocation[pos] for pos in related_positions if self.roster[pos] is None)
                
                if total_related_allocation > 0 and remaining_to_category > 0:
                    for position in related_positions:
                        if self.roster[position] is None:
                            additional_budget = round((remaining_to_category * self.strategy.budget_allocation[position]) / total_related_allocation, 2)
                            if self.budget + additional_budget <= 200:
                                self.strategy.budget_allocation[position] += additional_budget
                                remaining_to_category -= additional_budget

                bench_positions = ['BN1', 'BN2', 'BN3', 'BN4', 'BN5', 'BN6']
                total_bench_allocation = sum(self.strategy.budget_allocation[bn] for bn in bench_positions if self.roster[bn] is None)

                if total_bench_allocation > 0 and remaining_to_bench > 0:
                    for bench_position in bench_positions:
                        if self.roster[bench_position] is None:
                            additional_budget = round((remaining_to_bench * self.strategy.budget_allocation[bench_position]) / total_bench_allocation, 2)
                            if self.budget + additional_budget <= 200:
                                self.strategy.budget_allocation[bench_position] += additional_budget
                                remaining_to_bench -= additional_budget

            elif remaining_budget < 0:  # Handle overspend
                overspend = abs(remaining_budget)
                position_category = slot[:2]  # e.g., 'WR', 'RB', 'QB'
                related_positions = [pos for pos in self.strategy.budget_allocation.keys() if pos.startswith(position_category) and pos != slot]

                total_related_allocation = sum(self.strategy.budget_allocation[pos] for pos in related_positions if self.roster[pos] is None)
                
                if total_related_allocation > 0:
                    for position in related_positions:
                        if self.roster[position] is None:
                            subtract_amount = round((overspend * self.strategy.budget_allocation[position]) / total_related_allocation, 2)
                            if self.strategy.budget_allocation[position] - subtract_amount >= 1:  # Ensure not below $1
                                self.strategy.budget_allocation[position] -= subtract_amount
                                overspend -= subtract_amount
                                if overspend <= 0:
                                    break

                if overspend > 0:  # If overspend remains, deduct from other primary positions
                    primary_positions = ['QB1', 'QB2', 'RB1', 'RB2']
                    for primary_position in primary_positions:
                        if self.roster[primary_position] is None:
                            subtract_amount = min(overspend, self.strategy.budget_allocation[primary_position] - 1)
                            if self.strategy.budget_allocation[primary_position] - subtract_amount >= 1:  # Ensure not below $1
                                self.strategy.budget_allocation[primary_position] -= subtract_amount
                                overspend -= subtract_amount
                                if overspend <= 0:
                                    break