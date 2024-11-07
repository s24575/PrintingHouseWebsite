from flask import Blueprint, request

from src.db import db
from src.utils import calculate_price
from src.api.v1.carts.models import (
    AddCartItemsData,
    CartItemsResponse,
    DeleteCartItemData,
    GetCartItemsData,
)
from src.db.models import Item, Product


carts_blueprint = Blueprint("carts_endpoints", __name__, url_prefix="/cart")


@carts_blueprint.route("/get", methods=["GET"])
def get_cart() -> dict:
    user_id = 1
    cart_items = Item.query.filter_by(cart_user_id=user_id).all()
    # product = Product.get(product_id=cart_items)

    return CartItemsResponse(
        cart=[GetCartItemsData.model_validate(item) for item in cart_items]
    ).model_dump_json()


@carts_blueprint.route("/add", methods=["POST"])
def add_to_cart() -> dict:
    user_id = 1
    data = AddCartItemsData.model_validate_json(request.json)

    item = Item(
        cart_user_id=user_id,
        product_id=data.product_id,
        quantity=data.quantity,
        price=calculate_price(data.product_id, data.selected_options),
        user_comment=data.get("user_comment", ""),
    )
    db.session.add(item)
    db.session.commit()

    return Item.to_dict()


@carts_blueprint.route("/remove", methods=["DELETE"])
def remove_from_cart() -> dict:
    data = DeleteCartItemData.model_validate_json(request.json)
    item = Item.query.get(data.item_id)
    if not item:
        return {"message": "Item not found"}, 404

    db.session.delete(item)
    db.session.commit()
    return {"message": "Item removed from cart"}, 204
