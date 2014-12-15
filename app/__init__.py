import os
basedir = os.path.abspath(os.path.dirname(__file__))

from flask import Flask
from flask.ext import assets
from flask.ext.bootstrap import Bootstrap
from flask.ext.assets import Environment, Bundle
from config import config
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

db = SQLAlchemy()
bootstrap = Bootstrap()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'main.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # scss compilation
    env = assets.Environment(app)
    env.load_path = [os.path.join(basedir, 'assets/scss')]
    sass_bundle = assets.Bundle('main.scss', filters='scss',
                                output='css/main.css')
    env.register('css_main', sass_bundle)

    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    # login_manager.user_loader(load_user)

    # main views
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
