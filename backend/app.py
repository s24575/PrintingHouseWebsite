import os
from flask import Flask, jsonify
from flask_cors import CORS
from pydantic import ValidationError
import stripe

from src.db.db import init_db
from src.api.v1.carts.routes import carts_blueprint
from src.api.v1.products.routes import products_blueprint


class Config:
    SECRET_KEY = os.environ.get("PRINTING_HOUSE_SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("PRINTING_HOUSE_DATABASE_URI")


def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)
    init_db(app)
    _register_blueprints(app)
    _register_error_handlers(app)
    return app


def _register_blueprints(app: Flask) -> None:
    app.register_blueprint(carts_blueprint, url_prefix=carts_blueprint.url_prefix)
    app.register_blueprint(products_blueprint, url_prefix=products_blueprint.url_prefix)


def _register_error_handlers(app: Flask) -> None:
    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        response = jsonify({"error": "Validation error", "messages": error.errors()})
        response.status_code = 422
        return response


stripe.api_key = os.getenv("STRIPE_API_KEY")
app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
