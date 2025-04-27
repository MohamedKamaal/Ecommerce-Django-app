from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from reviews.forms import ReviewForm
from store.models import Product

class ReviewProductView(View):
    """
    View for submitting a product review.

    This view handles the `POST` request to submit a review for a specific product.
    If the user is authenticated, the review will be linked to their account.
    """

    def post(self, request, slug):
        """
        Handles the submission of a review for a product.

        Args:
            request: The incoming HTTP request, containing the review data.
            slug (str): The slug of the product being reviewed.

        Returns:
            HttpResponseRedirect: Redirects back to the product detail page after the review is submitted.
        """

        # Fetch the product using its slug
        product = get_object_or_404(Product, slug=slug)
        
        # Get the current authenticated user
        user = request.user
        
        # Initialize the review form with POST data
        form = ReviewForm(request.POST)
        
        # Validate the form
        if form.is_valid():
            # Save the form without committing to the database yet
            review = form.save(commit=False)
            
            # Assign the product being reviewed
            review.product = product
            
            # If the user is authenticated, associate the review with the user
            if user.is_authenticated:
                review.user = user
            
            # Save the review in the database
            review.save()

        # Redirect back to the product detail page
        return redirect("product-detail", slug=slug)
