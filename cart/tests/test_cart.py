import pytest
from django.test import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.http import Http404
from django.core.exceptions import ValidationError
from cart.cart import Cart
from store.models import ProductVariation
from store.tests.factories import ProductVariationFactory


@pytest.fixture
def request_factory():
    return RequestFactory()

@pytest.fixture
def cart(request_factory):
    request = request_factory.get('/')
    middleware = SessionMiddleware(lambda x: None)
    middleware.process_request(request)
    request.session.save()
    return Cart(request)

@pytest.fixture
def product_variation():
    return ProductVariationFactory(stock=10)  # Ensure sufficient stock

@pytest.mark.django_db
def test_cart_initialization_empty(cart):
    assert cart.cart == {}
    assert cart.session.get('cart') == {}

@pytest.mark.django_db
def test_cart_initialization_existing_cart(cart, product_variation, request_factory):
    cart.session['cart'] = {
        str(product_variation.id): {'id': product_variation.id, 'quantity': 2, 'price_cents': 1000}
    }
    cart.session.modified = True
    new_request = request_factory.get('/')
    new_request.session = cart.session
    new_cart = Cart(new_request)
    assert new_cart.cart == cart.session['cart']

@pytest.mark.django_db
def test_save_marks_session_modified(cart):
    cart.save()
    assert cart.session.modified is True

@pytest.mark.django_db
def test_clear_removes_cart(cart, product_variation):
    cart.cart = {
        str(product_variation.id): {'id': product_variation.id, 'quantity': 2, 'price_cents': 1000}
    }
    cart.session['cart'] = cart.cart
    cart.clear()
    assert cart.cart == {}
    assert 'cart' not in cart.session
    assert cart.session.modified is True

@pytest.mark.django_db
def test_add_new_product(cart, product_variation):
    cart.add(product_variation.id, quantity=2, update_quantity=True)
    assert str(product_variation.id) in cart.cart
    assert cart.cart[str(product_variation.id)] == {
        'id': product_variation.id,
        'price_cents': int(product_variation.price_cents),
        'quantity': 2
    }

@pytest.mark.django_db
def test_add_existing_product_without_update(cart, product_variation):
    cart.add(product_variation.id, quantity=2, update_quantity=True)
    cart.add(product_variation.id, quantity=3, update_quantity=False)
    assert cart.cart[str(product_variation.id)]['quantity'] == 5

@pytest.mark.django_db
def test_add_existing_product_with_update(cart, product_variation):
    cart.add(product_variation.id, quantity=2, update_quantity=True)
    cart.add(product_variation.id, quantity=3, update_quantity=True)
    assert cart.cart[str(product_variation.id)]['quantity'] == 3

@pytest.mark.django_db
def test_add_zero_quantity_removes_product(cart, product_variation):
    cart.add(product_variation.id, quantity=2, update_quantity=True)
    cart.add(product_variation.id, quantity=0, update_quantity=True)
    assert str(product_variation.id) not in cart.cart

@pytest.mark.django_db
def test_add_invalid_product_id(cart):
    with pytest.raises(Http404):  # get_object_or_404 raises Http404
        cart.add(id=9999)

@pytest.mark.django_db
def test_add_exceeds_stock(cart):
    variation = ProductVariationFactory(stock=2)
    with pytest.raises(ValidationError):
        cart.add(variation.id, quantity=5, update_quantity=True)

@pytest.mark.django_db
def test_remove_product(cart, product_variation):
    cart.add(product_variation.id, quantity=2, update_quantity=True)
    cart.remove(product_variation.id)
    assert str(product_variation.id) not in cart.cart

@pytest.mark.django_db
def test_remove_non_existent_product(cart):
    cart.remove(id=9999)  # Should not raise
    assert cart.session.modified is True

@pytest.mark.django_db
def test_len_empty_cart(cart):
    assert len(cart) == 0

@pytest.mark.django_db
def test_len_non_empty_cart(cart, product_variation):
    variation2 = ProductVariationFactory(stock=5)
    cart.add(product_variation.id, quantity=2, update_quantity=True)
    cart.add(variation2.id, quantity=3, update_quantity=True)
    assert len(cart) == 5

@pytest.mark.django_db
def test_get_total_cost_empty_cart(cart):
    assert cart.get_total_cost() == 0

@pytest.mark.django_db
def test_get_total_cost_non_empty_cart(cart, product_variation):
    cart.add(product_variation.id, quantity=2, update_quantity=True)
    expected_total = (product_variation.price_cents * 2) / 100
    assert cart.get_total_cost() == expected_total

@pytest.mark.django_db
def test_iter_empty_cart(cart):
    assert list(cart) == []

@pytest.mark.django_db
def test_iter_non_empty_cart(cart, product_variation):
    cart.add(product_variation.id, quantity=2, update_quantity=True)
    items = list(cart)
    assert len(items) == 1
    item = items[0]
    assert item['id'] == product_variation.id
    assert item['quantity'] == 2
    assert item['price'] == product_variation.price_cents / 100
    assert item['image_url'] == (product_variation.image or None)
    assert item['product_slug'] == product_variation.product.slug
    assert item['slug'] == product_variation.slug
    assert item['name'] == product_variation.product.name
    assert item['total'] == (product_variation.price_cents * 2) / 100

@pytest.mark.django_db
def test_iter_multiple_products(cart, product_variation):
    variation1 = product_variation
    variation2 = ProductVariationFactory(stock=5)
    cart.add(variation1.id, quantity=2, update_quantity=True)
    cart.add(variation2.id, quantity=3, update_quantity=True)
    items = list(cart)
    assert len(items) == 2
    item_ids = {item['id'] for item in items}
    assert item_ids == {variation1.id, variation2.id}
