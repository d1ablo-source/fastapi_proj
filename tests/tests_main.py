from fastapi.testclient import TestClient
from main import app
client = TestClient(app)

def test_create_and_get_order():
    r = client.post()