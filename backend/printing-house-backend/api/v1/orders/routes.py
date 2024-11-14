import datetime

import stripe
from flask import Blueprint, request, jsonify
from sqlalchemy.orm import joinedload

from api.v1.orders.models import OrderCreate
from common.utils import calculate_price
from db.db import Session
from db.models import Order, CartItem, Item, ItemOption

orders_blueprint = Blueprint("orders", __name__, url_prefix="/order")


@orders_blueprint.route("", methods=["POST"])
def create_order():
    data: OrderCreate = OrderCreate.model_validate(request.json)

    with Session() as session:
        cart_items = (
            session.query(CartItem)
            .options(joinedload(CartItem.product), joinedload(CartItem.options))
            .where(CartItem.user_id == data.user_id)
            .all()
        )

        prices = [calculate_price(cart_item) for cart_item in cart_items]
        total_price = sum(prices)

        payment_intent = stripe.PaymentIntent.create(
            amount=int(total_price) * 100,
            currency="pln",
            receipt_email="a@a.a",
            metadata={"integration_check": "accept_a_payment"},
        )

        order = Order(
            user_id=data.user_id,
            delivery_address_id=data.delivery_address_id,
            shipping_method=data.shipping_method,
            total_price=total_price,
            shipping_date=datetime.date.today(),
        )

        items = [
            Item(
                product_id=cart_item.product_id,
                name=cart_item.product.name,
                quantity=cart_item.quantity,
                price=price,
                item_options=[
                    ItemOption(
                        option_id=option.option_id,
                        name=option.option_group.title,
                        value=option.name,
                    )
                    for option in cart_item.options
                ],
            )
            for cart_item, price in zip(cart_items, prices)
        ]

        order.items = items

        for cart_item in cart_items:
            session.delete(cart_item)

        session.add(order)
        session.commit()

    return jsonify({"client_secret": payment_intent["client_secret"]})
