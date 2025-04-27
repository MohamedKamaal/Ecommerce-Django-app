import pytest
from django.urls import reverse
from store.tests.factories import CategoryFactory, ProductFactory, BrandFactory, ProductVariationFactory, SizeFactory

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



def test_product_detail_with_variant_slug(client):
    product = ProductFactory(is_active=True)
    featured = ProductVariationFactory(product=product, featured=True)
    alt_variation = ProductVariationFactory(product=product)

    response = client.get(reverse("product-detail", args=[product.slug]) + f"?variant_slug={alt_variation.slug}")

    assert response.status_code == 200
    assert response.context["chosen"] == alt_variation


def test_shop_page_sorting_latest(client):
    ProductFactory(name="Alpha", is_active=True)
    ProductFactory(name="Beta", is_active=True)

    response = client.get(reverse("shop") + "?sorting=alpha")
    products = list(response.context["page"].object_list)
    names = [p.name for p in products]
    assert names == sorted(names)
