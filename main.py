from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Literal

fastapi = FastAPI()

order_dict = {}

class Order(BaseModel):
    user: str
    amount: float = Field(gt=0)
    status: Literal["pending", "completed", "canceled"] = "pending"
@fastapi.post("/orders")
def create_order(user: str, amount: float, status: str) -> Order:
    order = Order(user=user, amount=amount, status=status)
    order_dict[order.user] = order
    return order
