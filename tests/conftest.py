import pytest
from fastapi.testclient import TestClient
from main import app, order_dict



@pytest.fixture()
def test_client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def clear_order():
    order_dict.clear()