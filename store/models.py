from django.db import models
from django.urls import reverse
from autoslug import AutoSlugField
from taggit.managers import TaggableManager
from helpers import cloud_init
from cloudinary.models import CloudinaryField
from colorfield.fields import ColorField
import uuid 
import decimal
from django.db.models import OuterRef, Subquery

from django.urls import reverse
from urllib.parse import urlencode
from django.db.models import Min

cloud_init()

class TimeStampedModel(models.Model):
    """
    A base model that provides timestamp fields for tracking the creation and update times
    of each record.
    """
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


class Brand(models.Model):
    """
    Model representing a brand.
    """
    name = models.CharField("Brand", unique=True, max_length=50)

    def __str__(self):
        return self.name
    

class Category(TimeStampedModel):
    """
    Model representing a product category.

    Inherits from TimeStampedModel to track creation and update times.
    """
    name = models.CharField(max_length=50, unique=True)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="subcategories"
    )
    slug = AutoSlugField(populate_from="name", unique=True)
    description = models.TextField(max_length=255, blank=True)
    tags = TaggableManager(blank=True)
    image = CloudinaryField('image', null=True, blank=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(TimeStampedModel):
    """
    Model representing a product.

    Inherits from TimeStampedModel to track creation and update times.
    """
    name = models.CharField(max_length=50, unique=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products"
    )
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="products")
    slug = AutoSlugField(populate_from="name", unique=True)
    description = models.TextField(max_length=500, blank=True)
    tags = TaggableManager(blank=True)
    base_image = CloudinaryField('image', null=True, blank=True)
    base_price_cents = models.IntegerField()
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'
        ordering = ['name']
        
    @property
    def base_price(self):
        """
        Property method to return the base price of the product in dollars.
        """
        return self.base_price_cents / 100
    
    @property
    def featured(self):
        """
        Property method to get the featured variation of the product.
        """
        featured = self.variations.filter(
            featured=True
        ).first()
        return featured
    
    @property
    def is_active_now(self):
        """
        Property method to check if any variation of the product is active.
        """
        if self.variations.filter(
            is_active=True
        ).exists():
            return True
        return False
    
    @property
    def on_sale(self):
        """
        Property method to check if any variation of the product has a discount.
        """
        return self.variations.filter(
            has_discount=True
        ).exists()
    
    def __str__(self):
        return self.name


class Size(models.Model):
    """
    Model representing product sizes (e.g., S, M, L).
    """
    name = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name


class ProductVariation(TimeStampedModel):
    """
    Model representing a variation of a product, such as a specific size and color.
    """
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="variations"
    )
    slug = AutoSlugField(populate_from="sku", unique=True)
    description = models.TextField(max_length=500, blank=True)
    sku = models.CharField(max_length=50, unique=True, blank=True)
    size = models.ForeignKey(Size, related_name="products", on_delete=models.CASCADE)
    color = ColorField()
    price_cents = models.IntegerField(null=True)
    stock = models.PositiveIntegerField(default=0)
    variation_image = CloudinaryField('image', null=True, blank=True)
    discount = models.DecimalField("Discount", max_digits=4, decimal_places=2, default=0)
    featured = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'product variation'
        verbose_name_plural = 'product variations'
        unique_together = [['product', 'color', 'size']]
        ordering = ['product', 'color']

    def save(self, *args, **kwargs):
        """
        Overridden save method to handle SKU generation, set product price if not set,
        and ensure only one product variation is featured for every product.
        """
        if not self.is_active_now:
            self.is_active = False 
        else:
            self.is_active = True
        super().save(*args, **kwargs)
    
    
    @property
    def price_after(self):
        """
        Calculate the discounted price if a discount is applied.
        """
        if self.discount != 0:
            discounted_price = (self.price_cents / 100) * (100 - float(self.discount)) / 100
            return round(discounted_price, 2)
    
    @property
    def price_without(self):
        """
        Return the original price without any discounts.
        """
        return self.price_cents / 100

    @property
    def has_discount(self):
        """
        Check if the variation has a discount.
        """
        return self.discount != 0
    
    @property
    def display_name(self):
        """
        Return the display name for the product variation, including product name, color, and size.
        """
        return f"{self.product.name} - {self.color} - {self.size}"
    
    @property
    def image(self):
        """
        Return the image URL for the product variation. If no image exists, fallback to the product's base image.
        If no base image exists, return None or a default image URL.
        """
        if self.variation_image:
            return self.variation_image.url
        if self.product.base_image:
            return self.product.base_image.url
        return None  # Or a default image URL, e.g., '/static/default.jpg'
    
    @property
    def price(self):
        """
        Return the final price of the variation, applying any discounts.
        """
        if self.has_discount:
            return self.price_cents * (100 - float(self.discount)) / 100
        return self.price_cents
    
    @property
    def same_colors(self):
        """
        Return other active variations of the same product with the same color.
        """
        variations = ProductVariation.objects.exclude(id=self.id).filter(
            product=self.product, color=self.color, is_active=True
        )
        return variations
        
    @property
    def other_color_variations(self):
        """
        Return variations of the same product in other colors.
        """
        min_ids = (
            ProductVariation.objects
            .filter(product=self.product, is_active=True)
            .exclude(color=self.color)
            .values('color')
            .annotate(min_id=Min('id'))
            .values_list('min_id', flat=True)
        )
        return ProductVariation.objects.filter(id__in=min_ids)

    def save(self, *args, **kwargs):
        """
        Overridden save method to generate SKU if missing, set product price if not set,
        and ensure only one product variation is featured for every product.
        """
        if not self.sku:
            uid = str(uuid.uuid4()).replace("-", "")[:5]
            color_hex = self.color.replace('#', '')
            self.sku = f"{self.product.id}-{self.size}-{color_hex}-{uid}"
        if not self.price_cents:
            self.price_cents = self.product.base_price_cents
        if self.featured:
            ProductVariation.objects.filter(
                product=self.product
            ).update(
                featured=False
            )
        if not ProductVariation.objects.filter(
            product=self.product, featured=True
        ).exists():
            self.featured = True 
        
        if self.stock == 0:
            self.is_active = False 
        super().save(*args, **kwargs)

    def __str__(self):
        return self.display_name
