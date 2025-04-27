import pytest
from django.urls import reverse
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory
from cart.cart import Cart
from orders.models import Order, OrderItem
from shipping.models import ShippingInfo
from store.models import ProductVariation

pytestmark = pytest.mark.django_db

# Helper to add session to request (for Cart usage)
def add_session_to_request(request):
    middleware = SessionMiddleware(lambda req: None)
    middleware.process_request(request)
    request.session.save()

@pytest.fixture
def cart_with_items(client, product_variation_factory):
    session = client.session
    session["cart"] = {
        "1": {
            "quantity": 2,
            "price": "500",
            "total": "1000",
            "id": "1",
        }
    }
    session.save()
    return session

def test_get_checkout_view_logged_in_user(client, django_user_model, cart_with_items):
    user = django_user_model.objects.create_user(username="mohamed", password="pass")
    client.force_login(user)
    
    response = client.get(reverse("checkout"))
    assert response.status_code == 200
    assert "form" in response.context
    assert "total" in response.context

def test_post_checkout_creates_order(client, user_factory, product_variation_factory):
    user = user_factory()
    product = product_variation_factory(id=1)
    client.force_login(user)

    # Add product to cart
    session = client.session
    session["cart"] = {
        "1": {"quantity": 1, "price": "500", "total": "500", "id": "1"},
    }
    session.save()

    post_data = {
        "first_name": "Mohamed",
        "last_name": "Kamal",
        "email": "test@example.com",
        "address": "123 Main St",
        "city": "Cairo",
        "zip_code": "12345",
        "phone": "123456789",
    }

    response = client.post(reverse("checkout"), data=post_data)
    assert response.status_code == 302  # Redirect to payment
    assert Order.objects.count() == 1
    order = Order.objects.first()
    assert order.user == user
    assert order.total_cents == 510  # 500 + 10 shipping
