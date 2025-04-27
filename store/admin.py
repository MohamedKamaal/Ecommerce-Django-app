from django.contrib import admin
from .models import Category, Product, ProductVariation, Brand, Size

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for the Category model.
    
    Attributes:
        list_display: Specifies the fields to be displayed in the list view.
        list_filter: Allows filtering categories by their parent category.
        search_fields: Enables searching by category name and description.
        ordering: Defines the default ordering of categories by name.
        inlines: Allows for inline editing of related models (currently empty).
    """
    list_display = ("name", "parent", "created", "slug")  # Show important fields
    list_filter = ("parent",)  # Filter by parent category
    search_fields = ("name", "description")  # Search by name and description
    ordering = ["name"]  # Order categories by name
    
    inlines = []  # Currently no inline models to edit within this view

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for the Product model.
    
    Attributes:
        list_display: Specifies the fields to be displayed in the list view.
        list_filter: Allows filtering products by their category.
        search_fields: Enables searching by product name, description, and tags.
        ordering: Defines the default ordering of products by name.
        readonly_fields: Specifies fields that are read-only (e.g., product URL).
    """
    list_display = ("name", "category", "base_price", "is_active", "created", "slug")
    list_filter = ("category",)  # Filters products by category
    search_fields = ("name", "description", "tags__name")  # Search by name, description, or tag name
    ordering = ["name",]  # Order products by name
    readonly_fields = ("get_url",)  # Display the URL field as read-only

    def get_url(self, obj):
        """
        Returns the URL of the product.
        
        Args:
            obj: The Product instance.
        
        Returns:
            str: The URL of the product.
        """
        return obj.get_url()
    get_url.short_description = "Product URL"  # Set a short description for the field

@admin.register(ProductVariation)
class ProductVariationAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for the ProductVariation model.
    
    Attributes:
        list_display: Specifies the fields to be displayed in the list view.
        list_filter: Allows filtering product variations by product, color, and size.
        search_fields: Enables searching by SKU, product name, and size.
        ordering: Defines the default ordering of variations by product and color.
        readonly_fields: Specifies fields that are read-only (e.g., SKU).
    """
    list_display = ("product", "is_active", "size", "color", "price_cents", "stock", "slug", "discount", "featured")
    list_filter = ("product", "color", "size")  # Filters variations by product, color, and size
    search_fields = ("sku", "product__name", "size")  # Search by SKU, product name, or size
    ordering = ["product", "color"]  # Order variations by product and color
    readonly_fields = ["sku",]  # SKU is a read-only field

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for the Brand model.
    
    Attributes:
        list_display: Specifies the fields to be displayed in the list view.
        list_filter: Allows filtering brands by their name.
        search_fields: Enables searching by brand name.
        ordering: Defines the default ordering of brands by name.
    """
    list_display = ("name",)  # Show brand name in the list view
    list_filter = ("name",)  # Filter brands by name
    search_fields = ("name",)  # Search brands by name
    ordering = ["name"]  # Order brands alphabetically by name

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for the Size model.
    
    Attributes:
        list_display: Specifies the fields to be displayed in the list view.
        list_filter: Allows filtering sizes by their name.
        search_fields: Enables searching by size name.
        ordering: Defines the default ordering of sizes by name.
    """
    list_display = ("name",)  # Show size name in the list view
    list_filter = ("name",)  # Filter sizes by name
    search_fields = ("name",)  # Search sizes by name
    ordering = ["name"]  # Order sizes alphabetically by name
