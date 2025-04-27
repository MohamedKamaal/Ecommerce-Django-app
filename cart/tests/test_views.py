import pytest
from django.test import RequestFactory, Client
from django.urls import reverse
from django.http import Http404
from django.contrib.sessions.middleware import SessionMiddleware

from cart.views import CartPageView, CartAddView, CartResetView, CartUpdateView
from cart.cart import Cart
from store.models import ProductVariation
from store.tests.factories import ProductVariationFactory
from store.forms import QuantityForm

# Fixtures

@pytest.fixture
def request_factory():
    return RequestFactory()

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def product_variation():
    return ProductVariationFactory(stock=10)

@pytest.fixture
def session_request(request_factory):
    request = request_factory.get('/')
    middleware = SessionMiddleware(lambda x: None)
    middleware.process_request(request)
    request.session.save()
    return request

# Tests

@pytest.mark.django_db
def test_cart_page_view_renders(client):
    client.session.flush()
    response = client.get(reverse('cart'))
    assert response.status_code == 200
    assert 'cart.html' in [t.name for t in response.templates]
    assert 'cart' in response.context
    assert isinstance(response.context['cart'], Cart)

@pytest.mark.django_db
def test_cart_add_view_success(client, product_variation):
    client.session.flush()
    url = reverse('cart-add', kwargs={'slug': product_variation.slug})
    response = client.get(url, {'quantity': 2})
    assert response.status_code == 302
    assert response.url == reverse('cart')

    cart = Cart(client)
    assert str(product_variation.id) in cart.cart
    assert cart.cart[str(product_variation.id)] == {
        'id': product_variation.id,
        'price_cents': int(product_variation.price_cents),
        'quantity': 2,
    }

@pytest.mark.django_db
def test_cart_add_view_default_quantity(client, product_variation):
    client.session.flush()
    url = reverse('cart-add', kwargs={'slug': product_variation.slug})
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == reverse('cart')

    cart = Cart(client)
    assert str(product_variation.id) in cart.cart
    assert cart.cart[str(product_variation.id)]['quantity'] == 1


@pytest.mark.django_db
def test_cart_add_view_non_existent_slug(client):
    client.session.flush()
    url = reverse('cart-add', kwargs={'slug': 'non-existent-slug'})
    response = client.get(url)
    assert response.status_code == 404

@pytest.mark.django_db
def test_cart_reset_view_clears_cart(client, product_variation):
    client.session.flush()
    cart = Cart(client)
    cart.add(product_variation.id, quantity=2)

    url = reverse('cart-reset')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == reverse('cart')

    cart = Cart(client)
    assert cart.cart == {}



@pytest.mark.django_db
def test_cart_update_view_non_existent_id(client):
    client.session.flush()
    url = reverse('cart-update', kwargs={'id': 9999, 'action': 'increment'})
    response = client.get(url)
    assert response.status_code == 404

@pytest.mark.django_db
def test_cart_update_view_invalid_action(client):
    client.session.flush()
    cart = Cart(client)
    product_variation = ProductVariationFactory()
    cart.add(product_variation.id, quantity=2)

    url = reverse('cart-update', kwargs={'id': product_variation.id, 'action': 'invalid'})
    response = client.get(url)
    assert response.status_code == 404
