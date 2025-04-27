import pytest
from django.urls import reverse
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory
from cart.cart import Cart
from orders.models import Order, OrderItem
from shipping.models import ShippingInfo
from store.models import ProductVariation
from store.tests.factories import ProductVariationFactory
from users.tests.factories import UserFactory


pytestmark = pytest.mark.django_db



@pytest.fixture
def product_variation_factory():
    return ProductVariationFactory()


# Helper to add session to request (for Cart usage)
def add_session_to_request(request):
    middleware = SessionMiddleware(lambda req: None)
    middleware.process_request(request)
    request.session.save()

@pytest.fixture
def cart_with_items(client, product_variation_factory):
    session = client.session
    variation = ProductVariationFactory()
    session["cart"] = {
        "1": {
            "quantity": 2,
            "price_cents": variation.price_cents,
            "id": variation.id,
        }
    }
    session.save()
    return session


def test_get_checkout_view_logged_in_user(client, django_user_model, cart_with_items):
    user = UserFactory()
    client.force_login(user)
    
    response = client.get(reverse("checkout"))
    assert response.status_code == 200
    assert "form" in response.context
    assert "total" in response.context

