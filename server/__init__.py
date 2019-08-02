import os
from dotenv import load_dotenv
from flask import Flask, render_template, g

from twilio.rest import Client


def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)

    from os import path
    if path.exists('demo.env'):
        load_dotenv('demo.env')
        app.config.from_object('server.config')
    else:
        print("No env file found. Copy demo.env.example to demo.env to continue.")

    if app.config['TWILIO_ACCT_SID'] is None:
        print("Set environment variables to continue.")


    @app.route('/')
    def index():
        return render_template('index.html')


    # apply the blueprints to the app
    from server import verification, authy
    app.register_blueprint(verification.bp)
    app.register_blueprint(authy.bp)


    # add error routing
    from server import error
    app.register_error_handler(401, error.unauthorized)
    app.register_error_handler(403, error.forbidden)
    app.register_error_handler(404, error.page_not_found)
    app.register_error_handler(500, error.internal_error)

    return app


