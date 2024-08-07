from flask import Blueprint, request, jsonify
from flask_app.session_manager import get_session_data

players = Blueprint('players', __name__)

@players.route('/players', methods=['GET'])
def get_players():
    session_id = request.args.get('session_id')
    print(f"Received session_id: {session_id}")
    session_data = get_session_data()
    league = session_data.get(session_id)
    print(f"Retrieved league object: {league}")

    if not league:
        return jsonify({'message': 'League not initialized'}), 500

    players_data = league.get_all_players()

    # Sort players by estimated value and filter out drafted players
    sorted_players = sorted(players_data, key=lambda p: p.estimated_value, reverse=True)
    filtered_players = [player for player in sorted_players if not player.drafted]

    players_json = [player.to_dict() for player in filtered_players]

    return jsonify(players_json)
