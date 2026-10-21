import pytest
from fastapi.testclient import TestClient
from main import app



@pytest.fixture()
def test_client():
    return TestClient(app)


@pytest.fixture()
def order_id_123():
    return "123"