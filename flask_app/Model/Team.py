from .Strategies.HUMAN import HumanStrategy

import logging

# Set up basic configuration for logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Create a function to log messages in red for critical issues
def log_red(message):
    logging.error(f'\033[91m{message}\033[0m')  # ANSI escape codes for red text


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
        if self.is_human():
            return
        if slot not in self.strategy.budget_allocation:
            return

        allocated_budget = self.strategy.budget_allocation[slot]
        remaining_budget = allocated_budget - cost
        self.strategy.budget_allocation[slot] = cost
        self.roster[slot] = "Filled"

        if remaining_budget > 0:
            self._handle_underspend(remaining_budget, slot)
        elif remaining_budget < 0:
            self._handle_overspend(abs(remaining_budget), slot)

        self._ensure_budget_constraint()
        self.budget = sum(self.strategy.budget_allocation.values())

    def _handle_underspend(self, remaining_budget, slot):
        remaining_to_related = round(0.7 * remaining_budget, 2)
        remaining_to_flex = round(0.3 * remaining_budget, 2)

        remaining_to_related = self._redistribute_to_related(remaining_to_related, slot)
        remaining_to_flex += remaining_to_related
        
        remaining_to_flex = self._redistribute_to_flex(remaining_to_flex)
        self._redistribute_to_skill_or_bench(remaining_to_flex)

    def _redistribute_to_related(self, amount, slot):
        related_positions = self._get_open_related_positions(slot)
        return self._redistribute_budget(related_positions, amount)

    def _redistribute_to_flex(self, amount):
        if self.roster['Flex'] is None:
            self.strategy.budget_allocation['Flex'] += amount
            return 0
        return amount

    def _redistribute_to_skill_or_bench(self, amount):
        skill_positions = self._get_open_skill_positions()
        if skill_positions:
            self._redistribute_budget(skill_positions, amount, evenly=True)
        else:
            bench_positions = self._get_open_bench_positions()
            self._redistribute_budget(bench_positions, amount)

    def _handle_overspend(self, overspend, slot):
        overspend = self._reduce_from_related(overspend, slot)
        overspend = self._reduce_from_bench(overspend)
        overspend = self._reduce_from_skill(overspend, slot)
        return overspend

    def _reduce_from_related(self, amount, slot):
        related_positions = self._get_open_related_positions(slot)
        return self._reduce_budget(related_positions, amount)

    def _reduce_from_bench(self, amount):
        bench_positions = self._get_open_bench_positions()
        return self._reduce_budget(bench_positions, amount)

    def _reduce_from_skill(self, amount, slot):
        skill_positions = [pos for pos in self._get_open_skill_positions() 
                           if not pos.startswith(slot[:2])]
        return self._reduce_budget(skill_positions, amount, evenly=True)

    def _ensure_budget_constraint(self):
        total_budget = sum(self.strategy.budget_allocation.values())
        if total_budget > 200:
            excess = total_budget - 200
            all_positions = list(self.strategy.budget_allocation.keys())
            self._reduce_budget(all_positions, excess)

    def _get_open_related_positions(self, slot):
        return [pos for pos in self.strategy.budget_allocation.keys() 
                if pos.startswith(slot[:2]) and pos != slot and self.roster[pos] is None]

    def _get_open_skill_positions(self):
        return [pos for pos in ['QB1', 'QB2', 'WR1', 'WR2', 'WR3', 'RB1', 'RB2', 'TE1'] 
                if self.roster[pos] is None]

    def _get_open_bench_positions(self):
        return [pos for pos in ['BN1', 'BN2', 'BN3', 'BN4', 'BN5', 'BN6'] 
                if self.roster[pos] is None]

    def _redistribute_budget(self, positions, amount, evenly=False):
        if not positions:
            return amount
        if evenly:
            per_position = round(amount / len(positions), 2)
            for position in positions:
                self.strategy.budget_allocation[position] += per_position
                amount -= per_position
        else:
            total_allocation = sum(self.strategy.budget_allocation[pos] for pos in positions)
            for position in positions:
                additional_budget = round((amount * self.strategy.budget_allocation[position]) / total_allocation, 2)
                self.strategy.budget_allocation[position] += additional_budget
                amount -= additional_budget
        return amount

    def _reduce_budget(self, positions, amount, evenly=False):
        try:
            if not positions:
                return amount
            total_allocation = sum(self.strategy.budget_allocation[pos] for pos in positions)
            if total_allocation == 0:
                logging.error(f"Unexpected zero total allocation for positions: {positions}")
                return amount  # Optionally, handle this situation more gracefully
            if evenly:
                per_position = round(amount / len(positions), 2)
                for position in positions:
                    subtract_amount = min(per_position, self.strategy.budget_allocation[position] - 1)
                    self.strategy.budget_allocation[position] -= subtract_amount
                    amount -= subtract_amount
            else:
                for position in positions:
                    proportion = (self.strategy.budget_allocation[position] / total_allocation)
                    subtract_amount = min(round(amount * proportion, 2), self.strategy.budget_allocation[position] - 1)
                    self.strategy.budget_allocation[position] -= subtract_amount
                    amount -= subtract_amount
        except Exception as e:
            logging.error(f"Error in reducing budget: {e}")
            raise  # Reraise the exception to handle it upstream if necessary
        return amount