from fastapi.testclient import TestClient
from main import app
import pytest




def test_get_orders(test_client: TestClient, order_id_123):
    result = test_client.get("/orders")
    print(f"Результат фикстуры: {order_id_123}")


def test_create_orders(test_client: TestClient):
    result = test_client.post("/orders")
    