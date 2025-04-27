from django.contrib import admin
from shipping.models import ShippingInfo

@admin.register(ShippingInfo)
class ShippingInfoAdmin(admin.ModelAdmin):
    """
    Admin interface for the ShippingInfo model.
    
    This class customizes how ShippingInfo instances are displayed and managed
    in the Django admin panel. It includes:
    - list_display: fields shown in the list view
    - list_filter: sidebar filters for quick filtering
    - search_fields: enables search functionality for specific fields
    """
    list_display = (
        "id",
        "user",
        "first_name",
        "last_name",
        "email",
        "city",
        "postal_code",
        "phone_number",
    )
    # Enables filtering by city and user
    list_filter = ("city", "user")

    # Allows admin to search by user name, email, or address
    search_fields = (
        "first_name",
        "last_name",
        "email",
        "user__username",
        "address",
    )

    # Optional: organize fields into sections in the detail view
    fieldsets = (
        ("User Info", {
            "fields": ("user", "first_name", "last_name", "email")
        }),
        ("Shipping Details", {
            "fields": ("address", "city", "postal_code", "phone_number")
        }),
    )
