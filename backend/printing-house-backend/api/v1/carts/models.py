from typing import Any

from pydantic import BaseModel


class CartItemData(BaseModel):
    cart_item_id: int
    product_id: int
    name: str
    price: float
    quantity: int


class AddCartItemRequest(BaseModel):
    product_id: int
    name: str
    selected_options: dict[int, int]


class DeleteCartItemData(BaseModel):
    cart_item_id: int


class CartItemsRequest(BaseModel):
    cart: AddCartItemRequest


class GetCartItemsResponse(BaseModel):
    items: list[CartItemData]
    total: float
