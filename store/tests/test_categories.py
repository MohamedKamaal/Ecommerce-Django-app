import pytest
from django.urls import reverse
from django.test import Client
from store.models import Category

pytestmark = pytest.mark.django_db  # This decorator ensures that the tests run with a database setup

# Test the categories view to ensure it returns the correct categories
def test_categories_view(client):
    # Create sample categories using factories or directly
    category1 = Category.objects.create(name="Category 1")
    category2 = Category.objects.create(name="Category 2")

    # Make a GET request to the categories view
    response = client.get(reverse('categories'))  # Assuming 'categories' is the name of the view

    # Assert that the response status is 200 (OK)
    assert response.status_code == 200

    # Assert that the context contains the categories and that they match what was created
    assert "categories" in response.context
    categories = response.context["categories"]
    assert category1 in categories
    assert category2 in categories

    # Check that the categories are rendered correctly in the response
    assert category1.name in str(response.content)
    assert category2.name in str(response.content)
