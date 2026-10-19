from main import Order
from pydantic import ValidationError
import pytest


def test_order_valid():
    o = Order(user="Lev", amount=200, status="completed")
    assert o.user == "Lev"
    assert o.amount == 200
    assert o.status == "completed"


def test_order_status_default():
    o = Order(user="Lev", amount=200)
    assert o.status == "pending"


def test_order_short_name():
    with pytest.raises(ValidationError):
        Ordero = Order(user="L", amount=200, status="completed")

def test_order_zero_amount_rejected():
    with pytest.raises(ValidationError):
        Order(user="Lev", amount=0, status="pending")


def test_order_negative_amount_rejected():
    with pytest.raises(ValidationError):
        Order(user="Lev", amount=-5, status="pending")


def test_order_bad_status():
    with pytest.raises(ValidationError):
        Order(user="Lev", amount=200, status="paid")