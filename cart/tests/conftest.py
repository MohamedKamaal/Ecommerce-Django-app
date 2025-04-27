import pytest
from django.contrib.auth.models import User
from products.models import Product, Category
from cart.cart import Cart




@pytest.fixture
def category():
    
    return Category.objects.create(
        name="Phones",
    )
    
@pytest.fixture
def product(category):
    
    return Product.objects.create(
        name="Test Product",
        price_cents=1000,  # $10.00
        slug="test-product",
        category=category
    )



@pytest.fixture
def cart(client):
    cart = Cart(request=client)
    return cart