from flask import Blueprint

from api.v1.products.models import MultipleProductsResponse, ProductDetailsResponse
from common.models import ProductModel
from db.models import Product, OptionGroup, Option

products_blueprint = Blueprint("products_endpoints", __name__, url_prefix="/products")


@products_blueprint.route("", methods=["GET"])
def get_products():
    products = Product.query.all()
    return MultipleProductsResponse(
        products=[ProductModel(**product.to_dict()) for product in products]
    ).model_dump_json()


@products_blueprint.route("/<int:product_id>", methods=["GET"])
def get_product_details(product_id):
    product = Product.query.get_or_404(product_id)

    option_groups = OptionGroup.query.filter_by(product_id=product.product_id).all()
    all_options = {
        option_group.option_group_id: {
            "option_group": option_group.to_dict(),
            "options": [
                option.to_dict()
                for option in Option.query.filter_by(
                    option_group_id=option_group.option_group_id
                ).all()
            ],
        }
        for option_group in option_groups
    }

    return ProductDetailsResponse(
        product=product.to_dict(), all_options=all_options
    ).model_dump_json()
