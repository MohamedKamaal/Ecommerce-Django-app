from django.db import models
from users.models import User
from cities_light.models import City  # Django Cities Light model for geographic data
from phonenumber_field.modelfields import PhoneNumberField  # Validates and formats phone numbers

class ShippingInfo(models.Model):
    """
    Represents shipping details provided by a user during checkout.

    Stores the recipient's contact and address information,
    and links it to a registered user and optionally a city.
    """

    first_name = models.CharField(max_length=50)
    """Recipient's first name."""

    last_name = models.CharField(max_length=50)
    """Recipient's last name."""

    email = models.EmailField(max_length=254)
    """Contact email for delivery updates or confirmation."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    """
    The user who placed the order.
    If the user is deleted, all associated shipping info will be removed.
    """

    address = models.TextField()
    """Street address for delivery (can include building, floor, etc.)."""

    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    """
    Optional city reference using Django Cities Light.
    If the city is deleted, this will be set to NULL.
    """

    postal_code = models.CharField(max_length=20)
    """Postal or ZIP code for delivery area."""

    phone_number = PhoneNumberField(region="EG")
    """
    Validated phone number (Egyptian region by default).
    Ensures correct formatting for international standards.
    """

    def __str__(self):
        """Returns a readable representation combining username and address."""
        return f"{self.user.username} - {self.address}"
