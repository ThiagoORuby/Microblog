from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate(db = db)
login = LoginManager()
login.login_view = 'login'

def init_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize plugins (db, redis)
    db.init_app(app)
    migrate.init_app(app)
    login.init_app(app)

    with app.app_context():

        from . import routes, models

        # register the blueprints

        return app