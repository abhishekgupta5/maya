# app/__init__.py

from flask import Flask
from config import app_config

def create_app(config_name):
    #App config details
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    @app.route('/')
    def test_server():
        return 'Testing flask'

    return app
