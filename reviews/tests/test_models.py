import pytest
from store.models import Product
from reviews.models import Review
from django.contrib.auth import get_user_model
from users.tests.factories import UserFactory 
from store.tests.factories import ProductFactory
from reviews.tests.factories import ReviewFactory

User = get_user_model()

@pytest.mark.django_db
class TestReviewModel:

    def test_create_review_with_product(self, product_factory, review_factory):
        """
        Test creating a review and associating it with a product.
        """
        product = product_factory.create()
        review = review_factory.create(product=product)
        
        # Check if the review is saved correctly in the database
        assert Review.objects.count() == 1
        assert review.product == product
        assert review.rating in [1, 2, 3, 4, 5]  # Check that the rating is valid
        assert review.review is not None
        assert review.product.reviews.count() == 1  # Ensure product has this review
        
    def test_create_review_with_user(self, user_factory, product_factory, review_factory):
        """
        Test creating a review by an authenticated user.
        """
        user = user_factory.create()
        product = product_factory.create()
        
        # Create review linked to the user
        review = review_factory.create(product=product, user=user)
        
        # Check if the review is saved and linked to the user
        assert review.user == user
        assert review.from_user is True  # Check the from_user property
        assert review.username == f"{user.first_name} {user.last_name}"  # Check the username property

    def test_create_review_without_user(self, product_factory, review_factory):
        """
        Test creating a review by an anonymous user (no user linked).
        """
        product = product_factory.create()
        
        # Create review without a user
        review = review_factory.create(product=product, user=None)
        
        # Check if the review is saved correctly
        assert review.user is None
        assert review.from_user is False  # Check the from_user property
        assert review.username == review.name  # Should return the name field since no user is linked

    def test_review_fields(self, review_factory):
        """
        Test various fields on the review model.
        """
        review = review_factory.create(rating=4, review="Great product!", name="Anonymous", email="test@example.com")
        
        assert review.rating == 4
        assert review.review == "Great product!"
        assert review.name == "Anonymous"
        assert review.email == "test@example.com"
        
    def test_review_related_name(self, product_factory, review_factory):
        """
        Test the related_name for the product reviews.
        """
        product = product_factory.create()
        review = review_factory.create(product=product)
        
        # Check if the reverse relationship works
        assert product.reviews.count() == 1
        assert review.product == product
