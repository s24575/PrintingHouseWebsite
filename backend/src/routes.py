from flask import current_app as app, request, jsonify
from src import db
from src.models import Order, Product


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


@app.route("/products", methods=["GET"])
def get_products():
    products = Product.query.all()
    return jsonify({"products": [product.to_dict() for product in products]})


@app.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify(product.to_dict())


@app.route("/products", methods=["POST"])
def add_product():
    data = request.get_json()
    new_product = Product(
        name=data.get("name"),
        image_url=data.get("image_url"),
        description=data.get("description"),
        price=data.get("price"),
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify(new_product.to_dict()), 201
