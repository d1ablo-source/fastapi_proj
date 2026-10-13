from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Literal
import httpx

#r = httpx.post(
#    "http://127.0.0.1:8000/orders",
#    json={"user": "elvus", "amount": 120.6, "status": "pending"},
#)
#print(r.status_code, r.json())

app = FastAPI()

order_dict: dict[int, dict] = {}
next_id = 1

class Order(BaseModel):
    user: str
    amount: float = Field(gt=0)
    status: Literal["pending", "completed", "canceled"] = "pending"
@app.post("/orders", status_code=201)
def create_order(order: Order):
    global next_id
    new = {"id": next_id, **order.model_dump()}
    order_dict[next_id] = new
    next_id += 1
    return new
@app.get("/orders/{order_id}")
def get_order(order_id: int):
    order = order_dict.get(order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order