from datetime import datetime

from pydantic import BaseModel

from db.models import ShippingMethod


class OrderCreate(BaseModel):
    delivery_address_id: int | None
    shipping_method: ShippingMethod


class ItemBasicInfo(BaseModel):
    name: str
    quantity: int


class OrderBasicInfo(BaseModel):
    order_id: int
    status: str
    total_price: float
    shipping_method: str
    created_at: datetime
    items: list[ItemBasicInfo]


class OrdersResponse(BaseModel):
    orders: list[OrderBasicInfo]
