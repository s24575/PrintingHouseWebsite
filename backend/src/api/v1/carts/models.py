from pydantic import BaseModel


class GetCartItemsData(BaseModel):
    product_id: int
    price: float
    quantity: int
    user_comment: str | None

    class Config:
        from_attributes = True


class AddCartItemsData(BaseModel):
    product_id: int
    quantity: int
    user_comment: str | None

    class Config:
        from_attributes = True


class CartItemsRequest(BaseModel):
    cart: AddCartItemsData


class CartItemsResponse(BaseModel):
    cart: list[AddCartItemsData]


class DeleteCartItemData(BaseModel):
    item_id: int
