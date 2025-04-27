import factory
from django.utils.text import slugify
from .models import Brand, Category, Product, ProductVariation, Size
from taggit.models import Tag

# Factory for Size
class SizeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Size

    name = factory.Faker('word')

# Factory for Brand
class BrandFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Brand

    name = factory.Faker('company')

# Factory for Category
class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Faker('word')
    parent = factory.SubFactory('myapp.factories.CategoryFactory', name=None)  # Recursive parent for subcategory
    description = factory.Faker('paragraph')
    slug = factory.LazyAttribute(lambda o: slugify(o.name))
    image = None  # Can use CloudinaryField if you want to simulate file upload

# Factory for Product
class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Faker('word')
    category = factory.SubFactory(CategoryFactory)
    brand = factory.SubFactory(BrandFactory)
    description = factory.Faker('paragraph')
    base_price_cents = factory.Faker('random_number', digits=5)
    is_active = True
    slug = factory.LazyAttribute(lambda o: slugify(o.name))
    base_image = None  # Simulate CloudinaryField image upload

# Factory for ProductVariation
class ProductVariationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductVariation

    product = factory.SubFactory(ProductFactory)
    size = factory.SubFactory(SizeFactory)
    color = factory.Faker('color')
    sku = factory.Faker('uuid4')
    price_cents = factory.Faker('random_number', digits=5)
    stock = factory.Faker('random_number', digits=2)
    discount = factory.Faker('random_number', digits=2)
    featured = True
    is_active = True
    variation_image = None  # Simulate CloudinaryField image upload
