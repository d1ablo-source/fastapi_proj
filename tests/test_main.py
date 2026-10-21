from fastapi.testclient import TestClient
from main import Order 
import pytest




def test_get_orders(test_client: TestClient):
    response = test_client.get("/orders")

    assert response.status_code == 200
    assert response.json() == []


def test_create_orders(test_client: TestClient):
    response = test_client.post("/orders", json={"user": "lev", "amount": 120, "status": "pending"})
    body = response.json()

    assert response.status_code == 201
    assert body["user"] == "lev"
    assert body["amount"] == 120
    assert body["status"] == "pending"


def test_create_and_get_task(test_client: TestClient):
    post_response = test_client.post("/orders", json={"user": "lev", "amount": 120, "status": "pending"})

    assert post_response.status_code == 201

    get_response = test_client.get("/orders")
    get_body = get_response.json()

    assert get_response.status_code == 200
    assert len(get_body) == 1

    created_order = Order.model_validate(get_body[0])

    assert isinstance(created_order, Order)
    assert created_order.user == "lev"
    assert created_order.status == "pending"


def test_patch(test_client: TestClient):
    patch_response = test_client.patch("/orders/{order_id}")