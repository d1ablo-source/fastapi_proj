from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Literal


app = FastAPI()

order_dict: dict[int, dict] = {}
next_id = 1

class Order(BaseModel):
    user: str = Field(min_length=2, max_length=30)
    amount: float = Field(gt=0, le=1000000)
    status: Literal["pending", "completed", "canceled"] = "pending"

class OrderUpdate(BaseModel):
    user: str | None = Field(default=None, min_length=2, max_length=30)
    amount: float | None = Field(default=None, gt=0, le=1000000) 
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
def get_orders():
    return list(order_dict.values())


@app.put("/orders/{order_id}", status_code=201)
def update_order_full(order_id: int, update_order: Order):
    order = order_dict.get(order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="order not found")
    order_dict[order_id] = {"id": order_id, **update_order.model_dump()}
    return order


@app.patch("/orders/{order_id}", status_code=201)
def update_order(order_id: int, update_order: OrderUpdate):
    order = order_dict.get(order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="order not found")
    data = update_order.model_dump(exclude_unset=True, exclude_none=True)
    order.update(data)
    return order