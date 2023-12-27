###
# Main application interface
###

# import the create app function 
# that lives in src/__init__.py
from src import create_app
from Model.League import League
from flask import Blueprint, request, jsonify, make_response, current_app


# create the app object
app = create_app()

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




