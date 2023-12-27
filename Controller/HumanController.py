# import random


# class HumanController:
#     def __init__(self, league, view):
#         self.league = league  # The model
#         self.view = view      # The view
#         self.currently_nominating = None

#     def start_draft(self):
#         for round_number in range(15):
#             for team in self.league.nomination_order:
#                 self.currently_nominating = team
#                 player_nominated = self.get_player_nominated()
#                 # Conduct auction round for the nominated player
#                 self.league.conduct_auction_round(player_nominated, team)

#     def get_player_nominated(self):
#         # If the nominating team is human-controlled, get the user's selection
#         if self.currently_nominating.is_human_strategy():
#             return self.get_user_selected_player()
#         else:
#             # Filter undrafted players from all players
#             undrafted_players = [player for player in self.league.get_all_players() if not player.drafted]

#             # Group players by position and sort by rank, then take the top 15 from each group
#             grouped_by_position = {}
#             for player in undrafted_players:
#                 pos = player.pos
#                 if pos not in grouped_by_position:
#                     grouped_by_position[pos] = []
#                 grouped_by_position[pos].append(player)

#             top_players_by_position = []
#             for players in grouped_by_position.values():
#                 players.sort(key=lambda x: x.positional_rank)  # Assuming lower rank means higher quality
#                 top_players_by_position.extend(players[:15])

#             # Select a player from the top players, e.g., a computer-nominated player
#             return random.choice(top_players_by_position)

#     def get_user_selected_player(self):
#         # Get the list of available players from the model
#         available_players = [player for player in self.league.get_all_players() if not player.drafted]

#         # Ask the view to display the options to the user and collect their selection
#         selected_player_name = self.view.display_nomination_options(available_players)

#         # Find the selected player in the list of available players
#         selected_player = next(player for player in available_players if player.name == selected_player_name)

#         return selected_player

#     def get_all_players(self):
#         return self.league.get_all_players()


