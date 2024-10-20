import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import stripe
from src.config import Config

db = SQLAlchemy()
migrate = Migrate()
stripe.api_key = os.getenv("STRIPE_API_KEY")


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    with app.app_context():
        from src import routes, models

    return app
