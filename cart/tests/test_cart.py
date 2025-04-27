import pytest
from unittest.mock import MagicMock
from cart.cart import Cart
from store.models import ProductVariation
from decimal import Decimal

@pytest.fixture
def mock_request():
    """
    Create a mock request with a session to simulate the behavior of a real request.
    """
    mock_request = MagicMock()
    mock_request.session = {}
    return mock_request


@pytest.fixture
def mock_product_variation():
    """
    Create a mock ProductVariation object to be used in cart operations.
    """
    mock_variation = MagicMock(spec=ProductVariation)
    mock_variation.id = 1
    mock_variation.price = 1000  # Price in cents
    mock_variation.stock = 10
    mock_variation.image = "image_url"
    mock_variation.slug = "product-slug"
    mock_variation.product.name = "Test Product"
    mock_variation.product.slug = "test-product-slug"
    return mock_variation


@pytest.fixture
def cart(mock_request):
    """
    Create a Cart instance with a mock request.
    """
    return Cart(mock_request)


def test_add_product_to_cart(cart, mock_product_variation):
    """
    Test adding a product to the cart.
    """
    # Mock the ProductVariation get query
    ProductVariation.objects.get = MagicMock(return_value=mock_product_variation)
    
    # Add product to cart
    cart.add(mock_product_variation.id, quantity=2)
    
    # Check cart has the product with correct quantity
    assert len(cart.cart) == 1
    assert cart.cart[str(mock_product_variation.id)]['quantity'] == 2
    assert cart.cart[str(mock_product_variation.id)]['price_cents'] == 1000


def test_update_product_quantity_in_cart(cart, mock_product_variation):
    """
    Test updating the quantity of a product in the cart.
    """
    # Mock the ProductVariation get query
    ProductVariation.objects.get = MagicMock(return_value=mock_product_variation)
    
    # Add product to cart
    cart.add(mock_product_variation.id, quantity=2)
    
    # Update the quantity
    cart.add(mock_product_variation.id, quantity=3, update_quantity=True)
    
    # Check cart has the updated quantity
    assert cart.cart[str(mock_product_variation.id)]['quantity'] == 5


def test_remove_product_from_cart(cart, mock_product_variation):
    """
    Test removing a product from the cart.
    """
    # Mock the ProductVariation get query
    ProductVariation.objects.get = MagicMock(return_value=mock_product_variation)
    
    # Add product to cart
    cart.add(mock_product_variation.id, quantity=2)
    
    # Remove product from cart
    cart.remove(mock_product_variation.id)
    
    # Check cart is empty
    assert len(cart.cart) == 0


def test_clear_cart(cart, mock_product_variation):
    """
    Test clearing the entire cart.
    """
    # Mock the ProductVariation get query
    ProductVariation.objects.get = MagicMock(return_value=mock_product_variation)
    
    # Add product to cart
    cart.add(mock_product_variation.id, quantity=2)
    
    # Clear the cart
    cart.clear()
    
    # Check cart is empty
    assert len(cart.cart) == 0


def test_get_cart_total_cost(cart, mock_product_variation):
    """
    Test calculating the total cost of the cart.
    """
    # Mock the ProductVariation get query
    ProductVariation.objects.get = MagicMock(return_value=mock_product_variation)
    
    # Add product to cart
    cart.add(mock_product_variation.id, quantity=2)
    
    # Calculate the total cost
    total_cost = cart.get_total_cost()
    
    # Assert that total cost is correct (1000 cents * 2 = 2000 cents = 20 dollars)
    assert total_cost == Decimal('20.00')


def test_cart_length(cart, mock_product_variation):
    """
    Test getting the total number of items in the cart.
    """
    # Mock the ProductVariation get query
    ProductVariation.objects.get = MagicMock(return_value=mock_product_variation)
    
    # Add products to the cart
    cart.add(mock_product_variation.id, quantity=2)
    cart.add(mock_product_variation.id, quantity=3)
    
    # Check total number of items in cart
    assert len(cart) == 5


def test_cart_iteration(cart, mock_product_variation):
    """
    Test iterating over the cart and enriching it with product details.
    """
    # Mock the ProductVariation get query
    ProductVariation.objects.get = MagicMock(return_value=mock_product_variation)
    ProductVariation.objects.filter = MagicMock(return_value=[mock_product_variation])
    
    # Add product to cart
    cart.add(mock_product_variation.id, quantity=2)
    
    # Iterate over the cart and get enriched details
    cart_items = list(cart.__iter__())
    
    # Assert that the cart item has enriched details like name, image, total cost
    assert len(cart_items) == 1
    assert cart_items[0]['name'] == "Test Product"
    assert cart_items[0]['image_url'] == "image_url"
    assert cart_items[0]['total'] == Decimal('20.00')  # 1000 cents * 2 items = 2000 cents = 20 dollars
