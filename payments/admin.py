from django.contrib import admin
from payments.models import Payment




class PaymentAdmin(admin.ModelAdmin):
    """
    Admin interface for managing Payment objects.

    The PaymentAdmin class defines how the `Payment` model is displayed in the Django admin 
    interface. It specifies the fields to be shown in the list view, enables search functionality, 
    and adds filters for easier management of payments.

    Attributes:
        list_display (tuple): The fields to be displayed in the list view.
        search_fields (tuple): The fields to be searchable in the admin.
        list_filter (tuple): The fields by which the list can be filtered.
        readonly_fields (tuple): The fields that cannot be edited in the admin.
    """
    list_display = ('order', 'total_cents', 'created', 'updated')
    search_fields = ('order__id', 'total_cents')
    list_filter = ('created', 'updated')
    readonly_fields = ('created', 'updated')

    
    

admin.site.register(Payment, PaymentAdmin)
