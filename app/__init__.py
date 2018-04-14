#app/__init__.py

#3rd party Imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#Local imports
from config import app_config

#Initializing db object
db = SQLAlchemy()

def create_app(config_name):
    #App config details
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py', silent=True)
    #For dev only
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    #Initializing database
    db.init_app(app)
    from app import models
    @app.route('/')
    def test_server():
        return 'Testing flask'

    #Registering Blueprints
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    return app
