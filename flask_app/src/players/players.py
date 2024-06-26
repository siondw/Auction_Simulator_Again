from flask import Blueprint, request, jsonify, make_response, current_app
from flask_app.Model.League import League 
import json

players = Blueprint('players', __name__)


@players.route('/players')
def get_players():
    
    # Access the global League instance
    league = current_app.league

    # Assuming 'league' is a globally accessible League object
    players_data = league.get_all_players()
        
    # Sort players by estimated_value
    sorted_players = sorted(players_data, key=lambda p: p.estimated_value, reverse=True)
    
    # Filter out players that have been drafted
    filtered_players = filter(lambda p: not p.drafted, sorted_players) 

    
    players_jsons = []

    for player in filtered_players:
        
        player_dict = player.to_dict()  # Convert player to dictionary
        players_jsons.append(player_dict)
        
    # Convert Players to JSON Format
    return jsonify(players_jsons)

