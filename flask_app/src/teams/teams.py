from flask import Blueprint, request, jsonify
from flask_app.session_manager import get_session_data

teams = Blueprint('teams', __name__)

@teams.route('/get-team-roster/<team_id>', methods=['GET'])
def get_team_roster(team_id):
    session_id = request.args.get('session_id')
    print(f"Attempting to access session data with session_id: {session_id}")
    session_data = get_session_data()
    print(f"Session data immediately after retrieval: {session_data}")

    league = session_data.get(session_id)
    print(f"League object retrieved: {league}")

    if not league:
        return jsonify({'error': 'League not initialized'}), 500

    team_name = f"Team {team_id}"
    team_roster = league.get_team_roster(team_name)

    if not team_roster:
        return jsonify({'error': 'Team not found'}), 404

    formatted_roster = [{'name': player.get_name() if player else 'Empty', 'slot': slot}
                        for slot, player in team_roster.items()]

    return jsonify(formatted_roster)

@teams.route('/get-team-names', methods=['GET'])
def get_team_names():
    try:
        session_id = request.args.get('session_id')
        session_data = get_session_data()
        league = session_data.get(session_id)

        if not league:
            return jsonify({'message': 'League not initialized'}), 500

        team_names = [team.name for team in league.nomination_order]
        print(f"Team names: {team_names}")  # Log the team names

        return jsonify(team_names)

    except Exception as e:
        print(f"Error in get_team_names: {e}")  # Log any exceptions
        return jsonify({'error': 'An error occurred while fetching team names'}), 500
