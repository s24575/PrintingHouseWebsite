from decimal import Decimal
from src.db.models import Product, Option


def calculate_price(product_id: int, selected_options: list) -> Decimal:
    # Get the product's base price
    product = Product.query.get(product_id)
    base_price = product.base_price

    # Add price increments from selected options
    total_price = base_price
    for option_id in selected_options:
        option = Option.query.get(option_id)
        if option:
            total_price += option.price_increment

    return total_price
