from flask import Flask, render_template, url_for
from flask_app.Model.League import League
import os


print("Absolute path of templates:", os.path.abspath('static/templates'))

def create_app():
    app = Flask(__name__, static_folder='../../static', template_folder='../../templates')
    app.league = League()
    
    
  
    
    # Add the default route
    # Can be accessed from a web browser
    # http://ip_address:port/
    # Example: localhost:8001
    @app.route("/")
    def welcome():
        return render_template('index.html')

    
    

   

    # Import the various Beluprint Objects
    from .players.players import players
    from .teams.teams import teams
    from .roa import roa
    

    # Register the routes from each Blueprint with the app object
    # and give a url prefix to each
    app.register_blueprint(players,   url_prefix='/p')
    app.register_blueprint(teams,     url_prefix='/t')
    app.register_blueprint(roa,       url_prefix='/round')

     # Don't forget to return the app object
    return app
   