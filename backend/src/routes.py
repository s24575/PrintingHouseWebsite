# app/routes.py
from flask import current_app as app, request, jsonify
from src import db
from src.models import Order


@app.route("/orders", methods=["POST"])
def create_order():
    data = request.get_json()

    customer_name = data.get("customer_name")
    product_name = data.get("product_name")
    quantity = data.get("quantity")

    if not customer_name or not product_name or not quantity:
        return jsonify({"error": "Missing data"}), 400

    new_order = Order(
        customer_name=customer_name,
        product_name=product_name,
        quantity=quantity,
        status="Pending",
    )

    db.session.add(new_order)
    db.session.commit()

    return jsonify({"message": "Order placed successfully!"}), 201


@app.route("/orders", methods=["GET"])
def get_orders():
    try:
        orders = Order.query.all()
        orders_list = [
            {
                "id": order.id,
                "customer_name": order.customer_name,
                "product_name": order.product_name,
                "quantity": order.quantity,
                "status": order.status,
            }
            for order in orders
        ]
        return jsonify({"orders": orders_list}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
