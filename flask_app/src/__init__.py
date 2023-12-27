# Some set up for the application 

from flask import Flask
from flaskext.mysql import MySQL
from Model.League import League

def create_app():
    app = Flask(__name__)
    app.league = League()
    
    
  
    
    # Add the default route
    # Can be accessed from a web browser
    # http://ip_address:port/
    # Example: localhost:8001
    @app.route("/")
    def welcome():
        return "<h1>Welcome</h1>"
    
    

   

    # Import the various Beluprint Objects
    from src.players.players import players
    from src.teams.teams import teams
    from src.roa import roa
    

    # Register the routes from each Blueprint with the app object
    # and give a url prefix to each
    app.register_blueprint(players,   url_prefix='/p')
    app.register_blueprint(teams,     url_prefix='/t')
    app.register_blueprint(roa,       url_prefix='/round')

     # Don't forget to return the app object
    return app
   