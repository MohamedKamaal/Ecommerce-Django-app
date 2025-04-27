import pytest
from store.tests.factories import BrandFactory, CategoryFactory, ProductFactory, ProductVariationFactory, SizeFactory
from store.models import Product, ProductVariation, Category

@pytest.mark.django_db
def test_category_creation():
    """Test that a category is created correctly."""
    category = CategoryFactory(name="Electronics")
    assert category.name == "Electronics"
    assert category.slug == "electronics"
    assert category.description is not None

@pytest.mark.django_db
def test_product_creation():
    """Test that a product is created correctly with relationships."""
    product = ProductFactory(name="Laptop")
    assert product.name == "Laptop"
    assert product.slug == "laptop"
    assert product.base_price_cents > 0  # Price should be a positive integer
    assert product.category is not None
    assert product.brand is not None

@pytest.mark.django_db
def test_product_variation_creation():
    """Test that a product variation is created correctly."""
    product_variation = ProductVariationFactory()
    assert product_variation.sku is not None
    assert product_variation.product is not None
    assert product_variation.size is not None
    assert product_variation.price_cents > 0
    assert product_variation.stock >= 0
    assert product_variation.featured is True
    assert product_variation.is_active is True

@pytest.mark.django_db
def test_product_with_discount():
    """Test that the discount functionality works correctly."""
    product_variation = ProductVariationFactory(price_cents=82744, discount=20)
    
    expected_price = round((82744 / 100) * (1 - 0.2), 2)
    
    assert product_variation.price_after == expected_price
    


@pytest.mark.django_db
def test_active_variation():
    """Test the 'is_active' functionality for variations."""
    product_variation = ProductVariationFactory(stock=0)
    assert not product_variation.is_active  # Stock is 0, so is_active should be False

