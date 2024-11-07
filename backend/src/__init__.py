# import os
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
# from flask_cors import CORS
# import stripe
# from backend.src.core import models
# from src.config import Config


# class Config:
#     SECRET_KEY = os.environ.get("PRINTING_HOUSE_SECRET_KEY")
#     SQLALCHEMY_DATABASE_URI = os.environ.get("PRINTING_HOUSE_DATABASE_URI")
#     SQLALCHEMY_TRACK_MODIFICATIONS = False


# db = SQLAlchemy()
# migrate = Migrate()
# stripe.api_key = os.getenv("STRIPE_API_KEY")


# def create_app(config_class=Config) -> Flask:
#     app = Flask(__name__)
#     app.config.from_object(config_class)

#     db.init_app(app)
#     migrate.init_app(app, db)
#     CORS(app)

#     with app.app_context():
#         from src import routes

#     return app
