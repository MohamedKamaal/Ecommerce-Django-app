# reviews/tests/conftest.py
import pytest
from users.tests.factories import UserFactory
from reviews.tests.factories import ReviewFactory
from store.tests.factories import ProductFactory

@pytest.fixture
def user_factory():
    return UserFactory

@pytest.fixture
def product_factory():
    return ProductFactory

@pytest.fixture
def review_factory():
    return ReviewFactory
