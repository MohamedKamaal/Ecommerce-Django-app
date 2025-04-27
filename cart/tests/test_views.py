import pytest
from django.urls import reverse
from django.test import Client
from django.core.exceptions import ValidationError
from store.tests.factories import ProductVariationFactory, CartFactory, ProductFactory, SizeFactory, CategoryFactory, BrandFactory
from cart.cart import Cart
from unittest.mock import MagicMock

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def mock_cart():
    """Mock Cart class to avoid modifying the actual session in tests"""
    return MagicMock(spec=Cart)

@pytest.fixture
def product_variation():
    """Creates a product variation using the ProductVariationFactory"""
    return ProductVariationFactory()

@pytest.fixture
def cart_data(product_variation):
    """Creates a cart data fixture with a sample item"""
    return {
        'cart': {
            str(product_variation.id): {'id': product_variation.id, 'quantity': 2, 'price_cents': 1000},
        }
    }

def test_cart_page_view(client, cart_data):
    """Test if the cart page renders correctly"""
    client.cookies["cart"] = cart_data  # Set mock cart cookie
    response = client.get(reverse("cart"))
    assert response.status_code == 200
    assert "cart" in response.context

def test_cart_add_view(client, product_variation):
    """Test adding a product variation to the cart"""
    url = reverse("cart:add", kwargs={"slug": product_variation.slug})
    response = client.get(url)
    cart = Cart(client.request)
    cart.add(product_variation.id, quantity=1, update_quantity=True)
    
    # Check if cart was updated correctly
    assert response.status_code == 302
    assert product_variation.id in cart.cart
    assert cart.cart[str(product_variation.id)]['quantity'] == 1

def test_cart_add_view_invalid_quantity(client, product_variation):
    """Test adding a product with invalid quantity"""
    url = reverse("cart:add", kwargs={"slug": product_variation.slug}) + "?quantity=20"
    response = client.get(url)
    cart = Cart(client.request)

    with pytest.raises(ValidationError):
        cart.add(product_variation.id, quantity=20, update_quantity=True)
    
    # Ensure the cart did not add the invalid product
    assert product_variation.id not in cart.cart

def test_cart_reset_view(client, cart_data):
    """Test resetting the cart"""
    client.cookies["cart"] = cart_data  # Set mock cart cookie
    url = reverse("cart:reset")
    response = client.get(url)
    
    cart = Cart(client.request)
    assert response.status_code == 302
    assert not cart.cart  # Ensure the cart is cleared

def test_cart_update_view_increment(client, cart_data, product_variation):
    """Test incrementing the quantity of a product variation in the cart"""
    cart_data['cart'][str(product_variation.id)] = {'id': product_variation.id, 'quantity': 2, 'price_cents': 1000}
    client.cookies["cart"] = cart_data  # Set mock cart cookie
    
    url = reverse("cart:update", kwargs={"id": product_variation.id, "action": "increment"})
    response = client.get(url)
    
    cart = Cart(client.request)
    assert response.status_code == 302
    assert cart.cart[str(product_variation.id)]['quantity'] == 3  # Quantity incremented by 1

def test_cart_update_view_decrement(client, cart_data, product_variation):
    """Test decrementing the quantity of a product variation in the cart"""
    cart_data['cart'][str(product_variation.id)] = {'id': product_variation.id, 'quantity': 2, 'price_cents': 1000}
    client.cookies["cart"] = cart_data  # Set mock cart cookie
    
    url = reverse("cart:update", kwargs={"id": product_variation.id, "action": "decrement"})
    response = client.get(url)
    
    cart = Cart(client.request)
    assert response.status_code == 302
    assert cart.cart[str(product_variation.id)]['quantity'] == 1  # Quantity decremented by 1

def test_cart_update_view_invalid_decrement(client, cart_data, product_variation):
    """Test decrementing a product variation when quantity is already 1"""
    cart_data['cart'][str(product_variation.id)] = {'id': product_variation.id, 'quantity': 1, 'price_cents': 1000}
    client.cookies["cart"] = cart_data  # Set mock cart cookie
    
    url = reverse("cart:update", kwargs={"id": product_variation.id, "action": "decrement"})
    response = client.get(url)
    
    cart = Cart(client.request)
    assert response.status_code == 302
    assert cart.cart[str(product_variation.id)]['quantity'] == 0  # Quantity should be 0 after decrement
