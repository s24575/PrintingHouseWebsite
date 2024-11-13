from flask import Flask, jsonify
from flask_cors import CORS
from pydantic import ValidationError

import settings
from api.v1.carts.routes import carts_blueprint
from api.v1.orders.routes import orders_blueprint
from api.v1.products.routes import products_blueprint


def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app)
    settings.init_app(app)
    _register_blueprints(app)
    _register_error_handlers(app)
    return app


def _register_blueprints(app: Flask) -> None:
    app.register_blueprint(carts_blueprint, url_prefix=carts_blueprint.url_prefix)
    app.register_blueprint(products_blueprint, url_prefix=products_blueprint.url_prefix)
    app.register_blueprint(orders_blueprint, url_prefix=orders_blueprint.url_prefix)


def _register_error_handlers(app: Flask) -> None:
    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        response = jsonify({"error": "Validation error", "messages": error.errors()})
        response.status_code = 422
        return response
