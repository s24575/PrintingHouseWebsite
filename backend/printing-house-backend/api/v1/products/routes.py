from flask import Blueprint, jsonify
from api.v1.products.models import MultipleProductsResponse, ProductDetailsResponse
from common.models import ProductModel
from db.db import Session
from db.models import Product, OptionGroup, Option


products_blueprint = Blueprint("products_endpoints", __name__, url_prefix="/products")


@products_blueprint.route("", methods=["GET"])
def get_products():
    with Session() as session:
        products = session.query(Product).all()
        response = MultipleProductsResponse(products=[ProductModel(**product.to_dict()) for product in products])
    return response.model_dump_json()


@products_blueprint.route("/<int:product_id>", methods=["GET"])
def get_product_details(product_id):
    with Session() as session:
        product = session.query(Product).get(product_id)
        if not product:
            return jsonify({"error": "Product not found"}), 404

        option_groups = session.query(OptionGroup).filter_by(product_id=product.product_id).all()
        all_options = {
            option_group.option_group_id: {
                "option_group": option_group.to_dict(),
                "options": [
                    option.to_dict()
                    for option in session.query(Option).filter_by(option_group_id=option_group.option_group_id).all()
                ],
            }
            for option_group in option_groups
        }

        response = ProductDetailsResponse(product=product.to_dict(), all_options=all_options)
    return response.model_dump_json()
