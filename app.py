import os
import sys
from pathlib import Path
import eventlet
import uuid
eventlet.monkey_patch()

from flask_app.src import create_app
from flask_app.Model.League import League
from flask_app.Model.RoundOfAuction import RoundOfAuction
from flask_app.Model.Team import Team
from flask import jsonify, current_app, request, g  # Import g from flask
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from flask_app.session_manager import get_session_data  

#
# Create the app object
app = create_app()
CORS(app)

# Create the Socket
socketio = SocketIO(app, cors_allowed_origins="*")

# WebSocket Events
@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('sendEvent')
def doSomething():
    print('Message Received!')

@socketio.on('place_human_bid')
def handle_human_bid(data):
    session_id = data.get('session_id')
    session_data = get_session_data()
    league = session_data.get(session_id)
    
    if not league:
        print("League not initialized")
        emit('bid_update', {'status': 'failed', 'message': 'League not initialized'})
        return

    print("Received a bid:", data)
    auction = current_app.current_auction_round

    try:
        if not auction:
            emit('bid_update', {'status': 'failed', 'message': 'Auction round not available'})
            return

        bid_amount = int(data.get('bid_amount', 0))
        human_team = league.get_human()

        if bid_amount <= auction.current_bid:
            emit('bid_update', {'status': 'failed', 'message': 'Bid must be higher than current bid'})
            return

        if bid_amount > human_team.get_max_bid():
            emit('bid_update', {'status': 'failed', 'message': 'Bid exceeds your maximum allowed bid'})
            return

        auction.process_bid(human_team, bid_amount)
        emit('bid_update', {'status': 'success', 'new_bid': bid_amount}, broadcast=True)

    except ValueError:
        emit('bid_update', {'status': 'failed', 'message': 'Invalid bid amount'})
    except Exception as e:
        print(f"Error handling bid: {e}")
        emit('bid_update', {'status': 'failed', 'message': 'An error occurred while processing the bid'})

@socketio.on('player_nominated')
def handle_player_nomination(data):
    session_id = data.get('session_id')
    session_data = get_session_data()
    league = session_data.get(session_id)
    
    if not league:
        emit('error', {'message': 'League not initialized'})
        return

    selected_player = data['player']
    player_object = league.find_player_by_name(selected_player)

    if player_object:
        league.continue_auction_round(player_object)
    else:
        emit('error', {'message': 'Player not found'})


@socketio.on('start_round')
def handle_start_round(data):
    session_id = data.get('session_id')
    print(f"Received session_id for start_round: {session_id}")
    session_data = get_session_data()
    league = session_data.get(session_id)
    print(f"Retrieved league for start_round: {league}")
    
    if not league:
        emit('error', {'message': 'League not initialized'})
        return
    
    league.initiate_auction_round()


@socketio.on('pass_bid')
def handle_pass_bid(data):
    session_id = data.get('session_id')
    auction = current_app.current_auction_round
    
    try:
        if not auction:
            raise ValueError("Auction round not available.")
        auction.set_isHumanInterested(False)
        print("Pass Bid")
    except Exception as e:
        emit('error', {'message': str(e)})

# Flask Routes
@app.route('/start-draft', methods=['GET'])
def start_draft():
    session_id = str(uuid.uuid4())
    league = League()
    
    session_data = get_session_data()
    session_data[session_id] = league
    
    print(f"New league object created: {league}")
    print(f"New session created with ID: {session_id}")
    print(f"Stored league object: {session_data[session_id]}")
    print(f"Current session_data: {session_data}")

    return jsonify({'message': 'Draft initialized successfully', 'session_id': session_id}), 200

@app.route('/get-round-summaries/', methods=['GET'])
def get_summaries():
    session_id = request.args.get('session_id')
    session_data = get_session_data()
    league = session_data.get(session_id)

    if not league:
        return jsonify({'message': 'League not initialized'}), 500

    return jsonify(league.round_summaries), 200

@app.route('/test-session', methods=['GET'])
def test_session():
    session_id = request.args.get('session_id')
    action = request.args.get('action')
    
    session_data = get_session_data()
    
    if action == 'create':
        session_data[session_id] = {'test': 'This is a test value'}
        print(f"Session created: {session_data}")
        return jsonify({'message': 'Session created', 'session_id': session_id})
    
    elif action == 'retrieve':
        value = session_data.get(session_id)
        print(f"Session data retrieved: {value}")
        return jsonify({'session_data': value})
    
    else:
        return jsonify({'error': 'Invalid action'}), 400

if __name__ == '__main__':
    socketio.run(app, debug=False, host='0.0.0.0', port=4000)
