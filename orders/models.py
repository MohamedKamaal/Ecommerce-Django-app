from django.db import models
from store.models import TimeStampedModel, Product, ProductVariation
from shipping.models import ShippingInfo
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.timezone import now 

User = get_user_model()

class Order(TimeStampedModel):
    """
    Represents a customer's order in the system.

    An `Order` is associated with a user and shipping information. It keeps track 
    of the order's status (e.g., pending, shipped, delivered), payment status, 
    and total cost.

    Attributes:
        shipping_info (ForeignKey): The shipping information associated with the order.
        user (ForeignKey): The user who placed the order.
        is_paid (BooleanField): Whether the order has been paid or not.
        status (CharField): The current status of the order.
        total_cents (IntegerField): The total amount of the order in cents.
    """
    
    class Status(models.TextChoices):
        """
        Defines the different statuses an order can have.

        The statuses help track the progress of an order from creation to delivery.

        Attributes:
            PENDING: The order is placed but not yet processed.
            PROCESSING: The order is being prepared or packed.
            SHIPPED: The order has been shipped.
            DELIVERED: The order has been delivered to the customer.
            CANCELED: The order has been canceled.
        """
        PENDING = ("pending", "Pending")
        PROCESSING = ("processing", "Processing")
        SHIPPED = ("shipped", "Shipped")
        DELIVERED = ("delivered", "Delivered")
        CANCELED = ("canceled", "Canceled")

    shipping_info = models.ForeignKey(
        ShippingInfo, on_delete=models.CASCADE, related_name="orders"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_orders"
    )
    is_paid = models.BooleanField(default=False)
    status = models.CharField(
        choices=Status.choices, max_length=50, default=Status.PENDING
    )
    total_cents = models.IntegerField()

    @property
    def total(self):
        """
        Returns the total price of the order in dollars.

        This is a property that converts the total price (stored in cents) into 
        dollars.

        Returns:
            float: The total price of the order in dollars.
        """
        return self.total_cents / 100

    def __str__(self):
        """
        String representation of the order.

        Returns:
            str: A string representation of the order in the format 'Order #<id> - <status>'.
        """
        return f"Order #{self.id} - {self.get_status_display()}"

class OrderItem(models.Model):
    """
    Represents an item in an order.

    An `OrderItem` is a product variation added to an order with a specified 
    quantity. It keeps track of the product, the quantity ordered, and the 
    total cost for that item.

    Attributes:
        order (ForeignKey): The order this item is part of.
        product (ForeignKey): The product variation associated with this item.
        quantity (PositiveIntegerField): The number of units of the product in the order.
        total_cents (IntegerField): The total cost of this item in cents.
    """
    
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="items"
    )
    product = models.ForeignKey(
        ProductVariation, on_delete=models.CASCADE, related_name="order_items"
    )
    quantity = models.PositiveIntegerField(default=1)
    total_cents = models.IntegerField()

    @property
    def total(self):
        """
        Returns the total price of this item in dollars.

        This is a property that converts the total price (stored in cents) into 
        dollars.

        Returns:
            float: The total price of the item in dollars.
        """
        return self.total_cents / 100
    
    def __str__(self):
        """
        String representation of the order item.

        Returns:
            str: A string representation of the order item in the format 
                 '<quantity> x <product_name> in Order #<order_id>'.
        """
        return f"{self.quantity} x {self.product.name} in Order #{self.order.id}"
