from flask import Blueprint, request, jsonify, make_response, current_app
from flask_app.Model.League import League 
import json




teams = Blueprint('teams', __name__)

@teams.route('/get-team-roster/<team_id>', methods=['GET'])
def get_team_roster(team_id):
    league = current_app.league

    team_name = f"Team {team_id}"
    team_roster = league.get_team_roster(team_name)  # Retrieve the team object

    if not team_roster:
        # Handle case where team is not found
        return jsonify({'error': 'Team not found'}), 404

    # team_roster = team.get_roster()  # Retrieve the roster using get_roster method

    formatted_roster = []
    for slot, player in team_roster.items():
        if player is not None:
            player_data = {'name': player.get_name(), 'slot': slot}
        else:
            player_data = {'name': 'Empty', 'slot': slot}

        formatted_roster.append(player_data)

    return jsonify(formatted_roster)


@teams.route('get-team-names', methods=['GET'])
def get_team_names():
    league = current_app.league
    nom_order = league.nomination_order
    teams = []

    for team in nom_order:
        teams.append(team.name)

    return jsonify(teams)



