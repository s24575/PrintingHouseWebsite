from pydantic import BaseModel
from typing import Literal


class OrderCreate(BaseModel):
    user_id: int
    delivery_address_id: int
    delivery_method: Literal["local", "inpost", "dhl"]
    total_price: float
