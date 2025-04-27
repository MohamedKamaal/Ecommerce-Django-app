import pytest
from myapp.factories import BrandFactory, CategoryFactory, ProductFactory, ProductVariationFactory, SizeFactory
from myapp.models import Product, ProductVariation, Category

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
    product_variation = ProductVariationFactory(discount=20)
    assert product_variation.price_after == (product_variation.price_cents / 100) * (1 - 0.20)
    
@pytest.mark.django_db
def test_sku_generation():
    """Test that SKU is generated correctly."""
    product_variation = ProductVariationFactory()
    assert product_variation.sku.startswith(str(product_variation.product.id))

@pytest.mark.django_db
def test_active_variation():
    """Test the 'is_active' functionality for variations."""
    product_variation = ProductVariationFactory(stock=0)
    assert not product_variation.is_active  # Stock is 0, so is_active should be False

@pytest.mark.django_db
def test_get_absolute_url():
    """Test the 'get_absolute_url' for product variations."""
    product_variation = ProductVariationFactory()
    url = product_variation.get_absolute_url()
    assert 'variant_slug' in url
    assert 'product-detail' in url  # Ensure the URL points to the correct product detail
