from flask import Blueprint, request, jsonify

from api.v1.carts.models import (
    CartItemsResponse,
    GetCartItemsData,
    AddCartItemData,
    DeleteCartItemData,
)
from common.utils import calculate_price
from db.db import db
from db.models import Item, ItemOption

carts_blueprint = Blueprint("carts_endpoints", __name__, url_prefix="/cart")


@carts_blueprint.route("/get", methods=["GET"])
def get_cart():
    user_id = 1
    cart_items: list[Item] = Item.query.filter_by(cart_user_id=user_id).all()

    # total = 0
    # for item in cart_items:
    #     item_options = ItemOption.query.filter_by(item_id=item.item_id).all()
    #     total += calculate_price(item.product_id, item_options)
    total = sum([x.price * x.quantity for x in cart_items])

    return CartItemsResponse(
        items=[GetCartItemsData.model_validate(item) for item in cart_items],
        total=total,
    ).model_dump_json()


@carts_blueprint.route("/add", methods=["POST"])
def add_to_cart():
    user_id = 1
    data = AddCartItemData.model_validate(request.json)

    item = Item(
        cart_user_id=user_id,
        product_id=data.product_id,
        name=data.name,
        quantity=data.quantity,
        price=calculate_price(data.product_id, data.selected_options),
        user_comment=data.user_comment,
    )
    db.session.add(item)
    db.session.flush()

    item_options = [
        ItemOption(item_id=item.item_id, option_id=option_id)
        for option_id in data.selected_options
        if option_id is not None
    ]
    db.session.add_all(item_options)
    db.session.commit()

    return item.to_dict()


@carts_blueprint.route("/remove", methods=["DELETE"])
def remove_from_cart():
    data = DeleteCartItemData.model_validate(request.json)
    item = Item.query.get_or_404(data.item_id)

    db.session.delete(item)
    db.session.commit()
    return {"message": "Item removed from cart"}, 204
