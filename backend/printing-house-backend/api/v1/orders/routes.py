import stripe
from flask import Blueprint, request, jsonify

from api.v1.orders.models import OrderCreate
from common.utils import calculate_price
from db.db import db
from db.models import Order

orders_blueprint = Blueprint("orders", __name__)


@orders_blueprint.route("/orders", methods=["POST"])
def create_order():
    data = OrderCreate.model_validate(request.json)

    user_id = 1
    items = Item.query.filter_by(cart_user_id=user_id).all()

    amount = calculate_price()

    payment_intent = stripe.PaymentIntent.create(
        amount=int(amount),
        currency="pln",
        receipt_email="a@a.a",
        metadata={"integration_check": "accept_a_payment"},
    )

    order = Order(
        user_id=data.user_id,
        delivery_address_id=data.delivery_address_id,
        delivery_method=data.delivery_method,
        total_price=data.total_price,
    )
    db.session.add(order)
    db.session.commit()

    for item in items:
        item.order_id = order.order_id
        item.cart_user_id = None
    db.session.add_all(items)

    db.session.commit()
    # return jsonify({"message": "Order created successfully", "order_id": order.order_id}), 201
    return jsonify({"client_secret": payment_intent["client_secret"]})
