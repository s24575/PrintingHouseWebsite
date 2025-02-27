import datetime

import stripe
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.orm import joinedload

from api.v1.orders.models import OrderCreate, OrdersResponse, OrderBasicInfo, ItemBasicInfo
from common.utils import calculate_price, create_address_for_order
from db.db import Session
from db.models import Order, CartItem, Item, ItemOption

orders_blueprint = Blueprint("orders", __name__, url_prefix="/order")


@orders_blueprint.route("", methods=["GET"])
@jwt_required()
def get_orders():
    user_id = get_jwt_identity()
    with Session() as session:
        orders = (session.query(Order).options(joinedload(Order.items)).filter(Order.user_id == user_id)).all()

    return OrdersResponse(
        orders=[
            OrderBasicInfo(
                order_id=order.order_id,
                status=order.status,
                total_price=float(order.total_price),
                shipping_method=order.shipping_method,
                created_at=order.created_at,
                items=[
                    ItemBasicInfo(
                        name=item.name,
                        quantity=item.quantity,
                    )
                    for item in order.items
                ],
            )
            for order in orders
        ]
    ).model_dump_json()


@orders_blueprint.route("", methods=["POST"])
@jwt_required()
def create_order():
    user_id = get_jwt_identity()

    data: OrderCreate = OrderCreate.model_validate(request.json)

    with Session() as session:
        cart_items = (
            session.query(CartItem)
            .options(joinedload(CartItem.product), joinedload(CartItem.options))
            .where(CartItem.user_id == user_id)
            .all()
        )

        prices = [
            calculate_price(cart_item.product.base_price, cart_item.options, cart_item.quantity)
            for cart_item in cart_items
        ]
        total_price = sum(prices)

        payment_intent = stripe.PaymentIntent.create(
            amount=int(total_price) * 100,
            currency="pln",
            receipt_email="a@a.a",
            metadata={"integration_check": "accept_a_payment"},
        )

        address = create_address_for_order(data.shipping_method, data.shipping_details)
        if address is not None:
            session.add(address)
            session.flush()
            address_id = address.address_id
        else:
            address_id = None

        order = Order(
            user_id=user_id,
            delivery_address_id=address_id,
            shipping_method=data.shipping_method,
            total_price=total_price,
            shipping_date=datetime.date.today(),
            number_nip=data.nip,
            is_invoice=bool(data.nip),
        )

        order.items = [
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
                files=cart_item.files,
            )
            for cart_item, price in zip(cart_items, prices)
        ]

        for cart_item in cart_items:
            session.delete(cart_item)

        session.add(order)
        session.commit()

    return jsonify({"client_secret": payment_intent["client_secret"]})
