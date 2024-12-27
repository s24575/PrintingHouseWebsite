from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from api.v1.carts.models import (
    GetCartItemsResponse,
    CartItemData,
    AddCartItemRequest,
    DeleteCartItemData,
)
from common.utils import calculate_price
from db.db import Session
from db.models import CartItem, Option, OptionGroup

carts_blueprint = Blueprint("carts_endpoints", __name__, url_prefix="/cart")


@carts_blueprint.route("/get", methods=["GET"])
@jwt_required()
def get_cart():
    user_id = get_jwt_identity()

    with Session() as session:
        cart_items = session.query(CartItem).filter_by(user_id=user_id).all()

        cart_items_data = [
            CartItemData(
                cart_item_id=cart_item.cart_item_id,
                product_id=cart_item.product_id,
                name=cart_item.product.name,
                price=float(calculate_price(cart_item.product.base_price, cart_item.options, cart_item.quantity)),
                quantity=cart_item.quantity,
            )
            for cart_item in cart_items
        ]

    total = sum([cart_item_data.price for cart_item_data in cart_items_data])

    return GetCartItemsResponse(
        items=cart_items_data,
        total=total,
    ).model_dump_json()


@carts_blueprint.route("/add", methods=["POST"])
@jwt_required()
def add_to_cart():
    user_id = get_jwt_identity()

    data = AddCartItemRequest.model_validate(request.json)

    with Session() as session:
        option_groups = session.query(OptionGroup).where(OptionGroup.product_id == data.product_id).all()

        quantity = 1
        option_ids = []
        for option_group in option_groups:
            if option_group.type == "select":
                if (option_id := data.selected_options.get(option_group.option_group_id)) is not None:
                    option_ids.append(option_id)
            elif option_group.type == "number":
                if (value := data.selected_options.get(option_group.option_group_id)) is not None:
                    if option_group.name == "ilosc":
                        quantity = value

        options = session.query(Option).where(Option.option_id.in_(option_ids)).all()

        cart_item = CartItem(user_id=user_id, product_id=data.product_id, quantity=quantity or 1, options=options)

        session.add(cart_item)
        session.commit()

        return jsonify(cart_item.to_dict()), 201


@carts_blueprint.route("/remove", methods=["DELETE"])
def remove_from_cart():
    data = DeleteCartItemData.model_validate(request.json)

    with Session() as session:
        cart_item = session.get(CartItem, data.cart_item_id)
        if not cart_item:
            return jsonify({"error": "Item not found"}), 404

        session.delete(cart_item)
        session.commit()
        return jsonify({"message": "Item removed from cart"}), 204
