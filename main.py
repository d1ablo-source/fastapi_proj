from fastapi import FastAPI, HTTPException, Query
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
    user: str = Field(min_length=2, max_length=30)
    amount: float = Field(gt=0, le=1000000)
    status: Literal["pending", "completed", "canceled"] = "pending"

class OrderUpdate(BaseModel):
    user: str | None = Field(min_length=2, max_length=30)
    amount: float | None = Field(gt=0, le=1000000) 
    status: Literal["pending", "completed", "canceled"] | None = None

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


@app.get("/orders")
def get_orders(status: str | None = None, limit: int = Query(10, ge=1, le=100), offset: int = Query(0, ge=0)):
    if status is None:
        orders = list(order_dict.values())
        return orders[offset : offset + limit]
    return [order for order in order_dict.values() if order["status"] == status]


@app.put("/orders/{order_id}")
def update_orders_full(update_id: int, update_order: Order):
    order_dict[update_id] = update_order.model_dump(exclude_unset=True)
    return {"message": "Заказы полностью обновлены", "data": order_dict}