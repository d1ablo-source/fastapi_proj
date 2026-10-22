from fastapi.testclient import TestClient
from main import Order 
import pytest




def test_get_orders(test_client: TestClient):
    response = test_client.get("/orders")

    assert response.status_code == 200
    assert response.json() == []


def test_create_order(test_client: TestClient):
    response = test_client.post("/orders", json={"user": "lev", "amount": 120, "status": "pending"})
    body = response.json()

    assert response.status_code == 201
    assert body["user"] == "lev"
    assert body["amount"] == 120
    assert body["status"] == "pending"


def test_create_and_get_order(test_client: TestClient):
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




@pytest.mark.parametrize(
    argnames=["payload", "expected_user", "expected_amount", "expected_status"],
    argvalues=[
        [{"user": "anna", "amount": 120, "status": "pending"}, "anna", 120, "pending"],
        [{"user": "anna"}, "anna", 120, "pending"],
        [{"status": "completed"}, "lev", 120, "completed"],
        [{"amount": 12000, "status": "canceled"}, "lev", 12000, "canceled"] 
        ]
)
def test_update(created_order, payload, expected_user, expected_amount, expected_status, test_client):
    created_order_id = created_order['id']
    response = test_client.patch(f"/orders/{created_order_id}", json=payload)
    body = response.json()

    assert body["user"] == expected_user
    assert body["amount"] == expected_amount
    assert body["status"] == expected_status
