###
# Main application interface
###
import os
import sys
from pathlib import Path



# import the create app function 
# that lives in src/__init__.py
from flask_app.src import create_app
from flask_app.Model.League import League
from flask_app.Model.RoundOfAuction import RoundOfAuction
from flask_app.Model.Team import Team
from flask import jsonify, current_app
from flask_socketio import SocketIO, emit
from flask_cors import CORS



# create the app object
app = create_app()
CORS(app)  

# Create the Socket
socketio = SocketIO(app, cors_allowed_origins="*")

# Example WebSocket event for a client connection
@socketio.on('connect')
def handle_connect():
    print('Client connected')

# Example WebSocket event for a client disconnection
@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('sendEvent')
def doSomething():
    print('Message Received!')


@socketio.on('place_human_bid')
def handle_human_bid(data):
    
    league = current_app.league
    
    if not league:
        print("League not initialized")

    print("Received a bid:", data)  # This will print the received data
    auction = current_app.current_auction_round

    try:
        # Ensure the auction round is available
        auction = current_app.current_auction_round
        if not auction:
            emit('bid_update', {'status': 'failed', 'message': 'Auction round not available'})
            return

        # Parse and validate bid amount
        bid_amount = int(data.get('bid_amount', 0))
        human_team = league.get_human()

        # Additional checks (like max bid)
        if bid_amount <= auction.current_bid:
            emit('bid_update', {'status': 'failed', 'message': 'Bid must be higher than current bid'})
            return

        if bid_amount > human_team.get_max_bid():  # Assuming max_bid is a property of the team
            emit('bid_update', {'status': 'failed', 'message': 'Bid exceeds your maximum allowed bid'})
            return

        # Process the bid
        auction.process_bid(human_team, bid_amount)
        emit('bid_update', {'status': 'success', 'new_bid': bid_amount}, broadcast=True)

    except ValueError:
        emit('bid_update', {'status': 'failed', 'message': 'Invalid bid amount'})
    except Exception as e:
        # Generic error handling, log the exception for debugging
        print(f"Error handling bid: {e}")
        emit('bid_update', {'status': 'failed', 'message': 'An error occurred while processing the bid'})

@socketio.on('player_nominated')
def handle_player_nomination(data):
    selected_player = data['player']
    print("Player Nominated")
    
    # Access the league instance stored in current_app
    league = current_app.league
    if not league:
        # Handle the case where the league is not yet initialized
        emit('error', {'message': 'League not initialized'})
        return

    # Find the player object based on the selected player's name
    player_object = league.find_player_by_name(selected_player)

    if player_object:
        # Call a method to continue the auction round with the nominated player
        league.continue_auction_round(player_object)
    else:
        # Handle the case where the player is not found
        emit('error', {'message': 'Player not found'})

@socketio.on('start_round')
def handle_start_round():
    print("Start Round")
    # Assuming you have an instance of your auction/league class
    league = current_app.league
        
    league.initiate_auction_round()

@socketio.on('pass_bid')
def handle_pass_bid():

    auction = current_app.current_auction_round
    

    try:
        if not auction:
            raise ValueError("Auction round not available.")
        auction.set_isHumanInterested(False)
        print("Pass Bid")
    except Exception as e:
        emit('error', {'message': str(e)})
            
# @app.errorhandler(Exception)
# def handle_exception(e):
#     # You can log the exception here for debugging
#     # Then, emit a response to Appsmith
#     emit('error', {'message': str(e)}, broadcast=True)
#     return "Please wait for round to begin", 500


@app.route('/start-draft', methods=['GET'])
def start_draft():
    # Creating a new instance for the draft
    current_app.league = League()

    # Setting up the league (e.g., loading players)
    current_app.league.import_players()  

    # Set nomination order
    # current_app.league.set_nomination_order

    # Since no data needs to be returned, just send a confirmation response
    return jsonify({'message': 'Draft initialized successfully'}), 200

@app.route('/get-round-summaries/', methods=['GET'])
def get_summaries():

    league = current_app.league
    
    if not league:
        return jsonify({'message': 'League not initialized'}), 500

    return jsonify(league.round_summaries), 200


if __name__ == '__main__':
    # we want to run in debug mode (for hot reloading) 
    # this app will be bound to port 4000. 
    # Take a look at the docker-compose.yml to see 
    # what port this might be mapped to... 
    app.run(debug = True, host = '0.0.0.0', port = 4000)
    # port = int(os.environ.get("PORT", 5000))
    # app.run(host='0.0.0.0', port=port)




