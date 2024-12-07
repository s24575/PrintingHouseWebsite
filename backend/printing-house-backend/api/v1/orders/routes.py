import datetime

import stripe
from flask import Blueprint, request, jsonify
from pydantic import BaseModel
from sqlalchemy import sql
from sqlalchemy.orm import joinedload

from api.v1.orders.models import OrderCreate
from common.utils import calculate_price
from db.db import Session
from db.models import Order, CartItem, Item, ItemOption, User, OrderStatus

orders_blueprint = Blueprint("orders", __name__, url_prefix="/order")


class ItemBasicInfo(BaseModel):
    name: str
    quantity: int


class OrderBasicInfo(BaseModel):
    order_id: int
    status: str
    total_price: float
    shipping_method: str
    created_at: datetime.datetime
    items: list[ItemBasicInfo]


class OrdersResponse(BaseModel):
    orders: list[OrderBasicInfo]


@orders_blueprint.route("", methods=["GET"])
def get_orders():
    user_id = 1
    with Session() as session:
        orders = (
            session.query(Order)
            .options(joinedload(Order.items))
            .filter(sql.and_(Order.user_id == user_id, Order.status != OrderStatus.completed))
        ).all()

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
            )
            for cart_item, price in zip(cart_items, prices)
        ]

        for cart_item in cart_items:
            session.delete(cart_item)

        session.add(order)
        session.commit()

    return jsonify({"client_secret": payment_intent["client_secret"]})
