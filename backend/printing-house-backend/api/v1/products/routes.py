from flask import Blueprint, jsonify, request
from api.v1.products.models import (
    MultipleProductsResponse,
    ProductDetailsResponse,
    ProcessSelectedOptionsData,
    ProcessSelectedOptionsResponse,
)
from common.models import ProductModel
from common.consts import OptionGroupType, QUANTITY_OPTION_GROUP_NAME
from common.utils import calculate_price
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


@products_blueprint.route("/<int:product_id>", methods=["POST"])
def process_selected_options(product_id):
    data = ProcessSelectedOptionsData.model_validate(request.json)

    with Session() as session:
        option_groups = session.query(OptionGroup).where(OptionGroup.product_id == product_id).all()

        quantity = 1
        option_ids = []
        for option_group in option_groups:
            value = data.selected_options.get(option_group.option_group_id)
            if value is None:
                raise ValueError(f"No value specified for {option_group.option_group_id}")
            match option_group.type:
                case OptionGroupType.Select:
                    option_ids.append(value)
                case OptionGroupType.Number:
                    if option_group.name == QUANTITY_OPTION_GROUP_NAME:
                        quantity = value

        options = session.query(Option).where(Option.option_id.in_(option_ids)).all()

        product = session.query(Product).filter_by(product_id=product_id).first()
        price = calculate_price(product.base_price, options, quantity)

    return ProcessSelectedOptionsResponse(
        price=float(price),
    ).model_dump_json()
