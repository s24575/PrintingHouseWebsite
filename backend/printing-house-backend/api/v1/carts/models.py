from typing import Any

from pydantic import BaseModel


class GetCartItemsData(BaseModel):
    cart_item_id: int
    product_id: int
    name: str
    price: float
    quantity: int


class AddCartItemData(BaseModel):
    product_id: int
    name: str
    quantity: int
    selected_options: dict[int, int]


class DeleteCartItemData(BaseModel):
    cart_item_id: int


class CartItemsRequest(BaseModel):
    cart: AddCartItemData


class GetCartItemsResponse(BaseModel):
    items: list[GetCartItemsData]
    total: float
