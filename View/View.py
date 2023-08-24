from flask import render_template


class View:
    def __init__(self, app):
        self.app = app

    def register_routes(self):
        @self.app.route('/')
        def home():
            return render_template('welcome.html')

    def run(self, debug=True):
        self.app.run(debug=debug)
