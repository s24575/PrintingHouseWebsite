from decimal import Decimal
from enum import StrEnum
from typing import Any, Type

from db.models import Product, Option, OptionGroup, CartItem


class OptionGroupType(StrEnum):
    Select = ("select",)
    Number = ("number",)


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


def calculate_price(cart_item: Type[CartItem]) -> Decimal:
    total_price = cart_item.product.base_price
    for option in cart_item.options:
        total_price += option.price_increment
    return total_price * cart_item.quantity
