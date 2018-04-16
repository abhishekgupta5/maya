#app/__init__.py

#3rd party Imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
#Local imports
from config import app_config

#Initializing db object
db = SQLAlchemy()

#Initializing login manager object
login_manager = LoginManager()

def create_app(config_name):
    #App config details
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py', silent=True)
    #For dev only
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    #Initializing database
    db.init_app(app)
    #Initializing login manager
    login_manager.init_app(app)
    login_manager.session_protection='strong'
    login_manager.login_view = 'auth.login'
    #Initialize flask_bootstrap
    Bootstrap(app)

    from app import models

    #Registering Blueprints
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    return app
