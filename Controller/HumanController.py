class HumanController:
    def __init__(self, league, view):
        self.league = league  # The model
        self.view = view      # The view

    def start_draft(self):
        self.league.start_draft()

    def get_player_nominated(self):
        # Determine the team nominating the player
        nominating_team = self.league.get_nominating_team()

        # If the nominating team is human-controlled, get the user's selection
        if nominating_team.is_human():
            return self.get_user_selected_player()
        else:
            return self.league.get_computer_nominated_player()

    def get_user_selected_player(self):
        # Get the list of available players from the model
        available_players = self.league.get_available_players()

        # Ask the view to display the options to the user and collect their selection
        selected_player_name = self.view.display_nomination_options(available_players)

        # Find the selected player in the list of available players
        selected_player = next(player for player in available_players if player.name == selected_player_name)

        return selected_player

    # You can add more methods as needed to handle different parts of the draft process
