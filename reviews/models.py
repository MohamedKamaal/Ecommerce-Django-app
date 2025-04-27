from django.db import models
from store.models import TimeStampedModel, Product
from django.contrib.auth import get_user_model
from django.utils.timezone import now

User = get_user_model()

class Review(TimeStampedModel):
    """
    Represents a user-generated review for a product.

    This model allows both authenticated and anonymous users to submit reviews,
    consisting of a rating, a text comment, and optional personal details.
    """

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    """
    The product being reviewed.
    When the product is deleted, all associated reviews are also removed.
    """

    rating = models.IntegerField(
        choices=[(1, '★'), (2, '★★'), (3, '★★★'), (4, '★★★★'), (5, '★★★★★')],
        default=5
    )
    """
    Rating score for the product (1 to 5 stars).
    Displayed using Unicode stars for better readability.
    """

    review = models.TextField()
    """
    The textual content of the review, typically a customer comment.
    """

    name = models.CharField(max_length=50, null=True, blank=True)
    """
    Optional name for anonymous reviewers.
    Ignored if a `user` is provided.
    """

    email = models.EmailField(max_length=254, null=True, blank=True)
    """
    Optional email for anonymous reviewers.
    Useful for follow-ups or verification.
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="reviews"
    )
    """
    Optional link to a registered user.
    If the user is deleted, associated reviews are also deleted.
    """

    @property
    def from_user(self):
        """
        Indicates whether this review was submitted by an authenticated user.
        
        Returns:
            bool: True if submitted by a registered user, False otherwise.
        """
        return self.user is not None

    @property
    def username(self):
        """
        Returns a display-friendly name of the reviewer.
        
        If the review is by a registered user, it returns their full name.
        Otherwise, it falls back to the provided `name` field.

        Returns:
            str: The reviewer's name.
        """
        if self.user is not None:
            return f"{self.user.first_name} {self.user.last_name}"
        return self.name
