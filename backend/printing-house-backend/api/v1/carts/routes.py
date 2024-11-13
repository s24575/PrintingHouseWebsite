from flask import Blueprint, request, jsonify
from api.v1.carts.models import (
    GetCartItemsResponse,
    GetCartItemsData,
    AddCartItemData,
    DeleteCartItemData,
)
from common.utils import calculate_price
from db.db import Session
from db.models import CartItem, Option

carts_blueprint = Blueprint("carts_endpoints", __name__, url_prefix="/cart")


@carts_blueprint.route("/get", methods=["GET"])
def get_cart():
    user_id = 1

    with Session() as session:
        cart_items = session.query(CartItem).where(CartItem.user_id == user_id).all()

        total = 0
        cart_items_data = []
        for cart_item in cart_items:
            price = calculate_price(cart_item)
            total += price

            cart_items_data.append(
                GetCartItemsData(
                    cart_item_id=cart_item.cart_item_id,
                    product_id=cart_item.product_id,
                    name=cart_item.product.name,
                    price=price,
                    quantity=cart_item.quantity,
                )
            )

        return GetCartItemsResponse(
            items=cart_items_data,
            total=total,
        ).model_dump_json()


@carts_blueprint.route("/add", methods=["POST"])
def add_to_cart():
    data = AddCartItemData.model_validate(request.json)
    user_id = 1

    with Session() as session:
        cart_item = CartItem(
            user_id=user_id,
            product_id=data.product_id,
            quantity=data.quantity,
        )

        cart_item.options = session.query(Option).where(Option.option_id.in_(data.selected_options)).all()

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
