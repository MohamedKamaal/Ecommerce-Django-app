import pytest
from reviews.forms import ReviewForm
from reviews.models import Review
from store.models import Product
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
class TestReviewForm:
    
    def test_valid_review_form_authenticated_user(self, user_factory, product_factory):
        """
        Test the form validation when a review is submitted by an authenticated user.
        """
        user = user_factory.create()
        product = product_factory.create()
        
        # Valid data for the form
        data = {
            'name': 'John Doe',
            'email': 'johndoe@example.com',
            'rating': 5,
            'review': 'Excellent product, highly recommended!',
        }
        
        # Create the form instance with the valid data
        form = ReviewForm(data)
        
        # Ensure the form is valid
        assert form.is_valid()
        
        # Save the form and ensure the review is created
        review = form.save(commit=False)
        review.product = product
        review.user = user
        review.save()
        
        # Check that the review has been saved to the database
        assert Review.objects.count() == 1
        saved_review = Review.objects.first()
        assert saved_review.product == product
        assert saved_review.user == user
        assert saved_review.rating == 5
        assert saved_review.review == 'Excellent product, highly recommended!'
    
    def test_valid_review_form_anonymous_user(self, product_factory):
        """
        Test the form validation when a review is submitted by an anonymous user.
        """
        product = product_factory.create()
        
        # Valid data for the form
        data = {
            'name': 'Jane Doe',
            'email': 'janedoe@example.com',
            'rating': 4,
            'review': 'Good quality, but could be improved.',
        }
        
        # Create the form instance with the valid data
        form = ReviewForm(data)
        
        # Ensure the form is valid
        assert form.is_valid()
        
        # Save the form and ensure the review is created
        review = form.save(commit=False)
        review.product = product
        review.save()
        
        # Check that the review has been saved to the database
        assert Review.objects.count() == 1
        saved_review = Review.objects.first()
        assert saved_review.product == product
        assert saved_review.name == 'Jane Doe'
        assert saved_review.email == 'janedoe@example.com'
        assert saved_review.rating == 4
        assert saved_review.review == 'Good quality, but could be improved.'
    
    def test_invalid_email_field(self):
        """
        Test the form validation for an invalid email address.
        """
        data = {
            'name': 'John Doe',
            'email': 'invalid-email',
            'rating': 3,
            'review': 'Product is okay, but could be better.',
        }
        
        form = ReviewForm(data)
        
        # Ensure the form is not valid due to invalid email
        assert not form.is_valid()
        assert 'Enter a valid email address.' in form.errors['email']
    
    def test_missing_review_field(self):
        """
        Test the form validation when the 'review' field is empty (required).
        """
        data = {
            'name': 'John Doe',
            'email': 'johndoe@example.com',
            'rating': 5,
            'review': '',  # Empty review field should be invalid
        }
        
        form = ReviewForm(data)
        
        # Ensure the form is not valid because the 'review' field is required
        assert not form.is_valid()
        assert 'This field is required.' in form.errors['review']
    
    def test_missing_rating_field(self):
        """
        Test the form validation when the 'rating' field is missing (required).
        """
        data = {
            'name': 'John Doe',
            'email': 'johndoe@example.com',
            'review': 'This is a valid review.',
        }
        
        form = ReviewForm(data)
        
        # Ensure the form is not valid because the 'rating' field is required
        assert not form.is_valid()
        assert 'This field is required.' in form.errors['rating']
