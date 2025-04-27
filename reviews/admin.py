from django.contrib import admin
from .models import Product, Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created')  # adjust as per your Review model
    search_fields = ('user__username', 'product__name')
    list_filter = ('rating', 'created')
