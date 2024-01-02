###
# Main application interface
###

# import the create app function 
# that lives in src/__init__.py
from src import create_app
from Model.League import League
from Model.RoundOfAuction import RoundOfAuction
from Model.Team import Team
from flask import jsonify, current_app
from flask_socketio import SocketIO, emit


# create the app object
app = create_app()

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
def print():
    print('Message Received!')

@socketio.on('place_human_bid')
def handle_human_bid(data):
    print("Received a bid:", data)  # This will print the received data
    try:
        # Ensure the auction round is available
        auction = current_app.current_auction_round
        if not auction:
            emit('bid_update', {'status': 'failed', 'message': 'Auction round not available'})
            return

        # Parse and validate bid amount
        bid_amount = int(data.get('bid_amount', 0))
        human_team = current_app.League.get_human()

        # Additional checks (like max bid)
        if bid_amount <= auction.current_bid:
            emit('bid_update', {'status': 'failed', 'message': 'Bid must be higher than current bid'})
            return

        if bid_amount > human_team.max_bid:  # Assuming max_bid is a property of the team
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
    # Logic to handle the nominated player
    # This could involve updating the game state, storing the nomination, etc.

    # Optionally, emit a response or broadcast an update
    emit('nomination_received', {'player': selected_player}, broadcast=True)

@app.route('/start-draft', methods=['GET'])
def start_draft():
    # Creating a new instance for the draft
    current_app.league = League()

    # Setting up the league (e.g., loading players)
    current_app.league.import_players()  

    # Set nomination order
    current_app.league.set_nomination_order

    # Since no data needs to be returned, just send a confirmation response
    return jsonify({'message': 'Draft initialized successfully'}), 200


if __name__ == '__main__':
    # we want to run in debug mode (for hot reloading) 
    # this app will be bound to port 4000. 
    # Take a look at the docker-compose.yml to see 
    # what port this might be mapped to... 
    app.run(debug = True, host = '0.0.0.0', port = 4000)




