from decimal import Decimal
from typing import Type

from db.models import CartItem


# def calculate_price(product_id: int, selected_options: dict[int, Any]) -> Decimal:
#     product = Product.query.get(product_id)
#
#     total_price = product.base_price
#     for option_group_id, value in selected_options.items():
#         option_group: OptionGroup = OptionGroup.query.get(option_group_id)
#         if option_group is None:
#             raise ValueError(f"OptionGroup with id {option_group_id} does not exist!")
#
#         option_group_type = OptionGroupType(option_group.type)
#
#         match option_group_type:
#             case OptionGroupType.Select:
#                 if not isinstance(value, int):
#                     raise ValueError(f"Value for {OptionGroupType.Select} type has to be a primary key to an option")
#                 option_id = value
#                 option: Option = Option.query.get(option_id)
#
#                 if option is None:
#                     raise ValueError(f"Option with id {option_id} does not exist!")
#                 total_price += option.price_increment
#             case OptionGroupType.Number:
#                 if not isinstance(value, int):
#                     raise ValueError(f"Value for {OptionGroupType.Number} type has to be a number")
#                 if option_group.name == "ilosc":
#                     total_price *= value
#
#     return total_price


def calculate_price_for_cart_item(cart_item: Type[CartItem]) -> Decimal:
    return calculate_price(cart_item.product.base_price, cart_item.options, cart_item.quantity)


def calculate_price(base_price: Decimal, options: list, quantity: int) -> Decimal:
    return Decimal(quantity) * (sum([option.price_increment for option in options]) + base_price)
