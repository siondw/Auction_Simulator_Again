from flask import Blueprint, request, jsonify, make_response, current_app
from Model.League import League 
import json




teams = Blueprint('teams', __name__)

@teams.route('/get-team-roster/<team_id>', methods=['GET'])
def get_team_roster(team_id):
    league = current_app.league

    team_name = f"Team {team_id}"

    team_roster = league.get_team_roster(team_name)

    if all(player is None for player in team_roster.values()):
        # Return a message indicating the roster is empty
        empty_roster = [{"name": None, "position": None, "other_attributes": None} for _ in range(17)]
        return jsonify(empty_roster), 200

    roster_dicts = [player.to_dict() for player in team_roster]

    return jsonify(roster_dicts)

@teams.route('get-team-names', methods=['GET'])
def get_team_names():
    league = current_app.league
    nom_order = league.nomination_order
    teams = []

    for team in nom_order:
        teams.append(team.name)

    return jsonify(teams)



