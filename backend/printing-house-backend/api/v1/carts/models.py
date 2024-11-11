from typing import Any

from pydantic import BaseModel


class GetCartItemsData(BaseModel):
    product_id: int
    name: str
    price: float
    quantity: int
    user_comment: str | None

    class Config:
        from_attributes = True


class AddCartItemData(BaseModel):
    product_id: int
    name: str
    quantity: int
    user_comment: str = ""
    selected_options: dict[int, Any]

    class Config:
        from_attributes = True


class CartItemsRequest(BaseModel):
    cart: AddCartItemData


class CartItemsResponse(BaseModel):
    items: list[GetCartItemsData]
    total: float


class DeleteCartItemData(BaseModel):
    item_id: int
