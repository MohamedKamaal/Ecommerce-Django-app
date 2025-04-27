import pytest
from django.urls import reverse
from django.test import Client
from orders.models import Order
from .factories import OrderFactory  # Assuming you have a factory for Order
from .models import Payment
from django.db import IntegrityError

@pytest.fixture
def order():
    """Creates an order fixture using the OrderFactory"""
    return OrderFactory()

@pytest.fixture
def payment(order):
    """Creates a payment fixture for the given order"""
    return Payment.objects.create(order=order, total_cents=5000)  # $50.00 payment

def test_payment_creation(payment, order):
    """Test if a payment is created correctly for an order"""
    assert payment.order == order
    assert payment.total_cents == 5000
    assert str(payment) == f"Payment for Order {order.id} - $50.00"

def test_payment_total_cents(payment):
    """Test if the payment total_cents is set correctly"""
    assert payment.total_cents == 5000  # Payment of $50.00

def test_payment_invalid_order():
    """Test if a payment cannot be created without an order"""
    with pytest.raises(IntegrityError):
        Payment.objects.create(total_cents=5000)  # Missing order
