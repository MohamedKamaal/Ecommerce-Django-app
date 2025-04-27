import pytest
from django.urls import reverse
from .factories import CategoryFactory, ProductFactory, BrandFactory, ProductVariationFactory, SizeFactory

pytestmark = pytest.mark.django_db  # This decorator ensures that the tests run with a database setup

# Test HomePageView
def test_home_page_view(client):
    # Create some categories and products using factories
    category1 = CategoryFactory()
    category2 = CategoryFactory()

    product1 = ProductFactory(category=category1, is_active=True)
    product2 = ProductFactory(category=category2, is_active=True)

    # Make a GET request to the homepage
    response = client.get(reverse("home"))
    
    # Assert that the response status is 200 (OK)
    assert response.status_code == 200
    assert "latest_products" in response.context
    assert "popular_products" in response.context
    assert "top_categories" in response.context
    assert category1.name in str(response.content)  # Check if category appears in the response
    assert product1.name in str(response.content)   # Check if product appears in the response

# Test ProductDetailPageView
def test_product_detail_page_view(client):
    # Create a product with a variation
    product = ProductFactory(is_active=True)
    variation = ProductVariationFactory(product=product)

    # Get the URL for the product detail page using its slug
    response = client.get(reverse("product-detail", args=[product.slug]))
    
    # Assert that the response status is 200 (OK)
    assert response.status_code == 200
    assert "product" in response.context
    assert "chosen" in response.context
    assert product.name in str(response.content)  # Check if product name appears in the response

# Test ShopPageView with filters
def test_shop_page_view_with_filters(client):
    # Create products and categories using factories
    category = CategoryFactory(name="Category 1")
    brand = BrandFactory(name="Brand A")
    size = SizeFactory(name="Small")

    product1 = ProductFactory(category=category, brand=brand, is_active=True)
    product2 = ProductFactory(category=category, brand=brand, is_active=True)

    # Create a variation for filtering by size
    variation1 = ProductVariationFactory(product=product1, size=size)
    variation2 = ProductVariationFactory(product=product2, size=size)

    # Get the URL for the shop page with query parameters
    response = client.get(reverse("shop") + "?category=" + category.slug + "&brand=" + brand.name)
    
    # Assert that the response status is 200 (OK)
    assert response.status_code == 200
    assert "products" in response.context
    assert product1.name in str(response.content)  # Check if product appears in the response
    assert product2.name in str(response.content)  # Check if product appears in the response

    # Test pagination (ensure that pagination is handled correctly)
    paginator = response.context["page"]
    assert paginator.has_next()  # Check if there's a next page
