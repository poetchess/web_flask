from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)

    # The configuration settings can be imported into the application using
    # from_object() method.
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # An application is created and configured, the extensions can be initialized.
    # Calling init_app() on the extensions completes their initialization.
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)

    # Attach routes and custom error pages here.
    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    # when 'url_prefix' is used, all the routes defined in the blueprint will be
    # registered with the given prefix. For example, the /login route will be
    # registered as /auth/login
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app