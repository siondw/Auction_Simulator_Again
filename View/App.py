from flask import Flask, render_template, redirect
from flask import request
from Controller.HumanController import HumanController
from Model.League import League
from View import View

app = Flask(__name__)

# Create an instance of the League class
league = League()

# Create an instance of the View class
view = View(app)
view.register_routes()

# Create an instance of the HumanController class
controller = HumanController(league, view)

@app.route('/draft')
def draft():
    # Use the controller to get the available players
    players = controller.get_all_players()

    controller.start_draft()

    # Get the current player being nominated
    current_player = controller.get_player_nominated()

    return render_template('draft.html', current_player=current_player, players=players)

@app.route('/handle_nomination', methods=['POST'])
def handle_nomination():
    selected_player_name = request.form['player_name']
    # Pass this 'selected_player_name' back to your Controller to handle it.
    # ... (your logic here)
    return redirect('/draft')  # Redirect back to the draft page, or wherever appropriate

if __name__ == '__main__':
    app.run(debug=True)
