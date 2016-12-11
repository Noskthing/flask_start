from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment

import sys
sys.path.append("..")
from config import config


bootstrap = Bootstrap()
moment = Moment()

def create_app(config_name):
    app = Flask(__name__)
    
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    moment.init_app(app)

    # app.config['SECRET_KEY'] = 'hard to guess string'
   	
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint,url_prefix = '/auth')

    return app
