from django.db import models
from store.models import TimeStampedModel, Product, ProductVariation
from shipping.models import ShippingInfo
from django.contrib.auth import get_user_model
from orders.models import Order 
User = get_user_model()


class Payment(TimeStampedModel):
    """
    Represents a payment for a specific order.

    The `Payment` model links a payment to an order and stores the total 
    amount paid in cents. This model is used for recording payment 
    information and keeping track of payments associated with orders.

    Attributes:
        order (OneToOneField): The order that this payment is linked to.
        total_cents (IntegerField): The total amount of the payment in cents.
    """
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    total_cents = models.IntegerField()

    def __str__(self):
        """
        Return a string representation of the payment.

        Returns:
            str: A string in the format 'Payment for Order {order_id} - ${total_amount}'.
        """
        return f"Payment for Order {self.order.id} - ${self.total_cents / 100:.2f}"

    class Meta:
        """
        Meta options for the Payment model.

        - verbose_name: The singular name for the model in the admin interface.
        - verbose_name_plural: The plural name for the model in the admin interface.
        """
        verbose_name = "Payment"
        verbose_name_plural = "Payments"