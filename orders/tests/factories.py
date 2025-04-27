import factory
from factory.django import DjangoModelFactory
from store.models import ProductVariation
from shipping.models import ShippingInfo
from django.contrib.auth import get_user_model
from .models import Order, OrderItem

User = get_user_model()

class ShippingInfoFactory(DjangoModelFactory):
    class Meta:
        model = ShippingInfo

    user = factory.SubFactory('tests.factories.UserFactory')
    first_name = 'John'
    last_name = 'Doe'
    email = 'john.doe@example.com'
    address = '123 Main St'

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('user_name')
    email = factory.Faker('email')
    password = factory.PostGenerationMethodCall('set_password', 'password')

class ProductVariationFactory(DjangoModelFactory):
    class Meta:
        model = ProductVariation

    product = factory.SubFactory('tests.factories.ProductFactory')
    price_cents = factory.Faker('random_int', min=1000, max=5000)  # price in cents
    stock = factory.Faker('random_int', min=1, max=100)

class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Faker('word')
    description = factory.Faker('text')
    price_cents = factory.Faker('random_int', min=1000, max=5000)

class OrderFactory(DjangoModelFactory):
    class Meta:
        model = Order

    shipping_info = factory.SubFactory(ShippingInfoFactory)
    user = factory.SubFactory(UserFactory)
    total_cents = factory.Faker('random_int', min=1000, max=5000)
    is_paid = False
    status = 'pending'

class OrderItemFactory(DjangoModelFactory):
    class Meta:
        model = OrderItem

    order = factory.SubFactory(OrderFactory)
    product = factory.SubFactory(ProductVariationFactory)
    quantity = factory.Faker('random_int', min=1, max=5)
    total_cents = factory.LazyAttribute(lambda obj: obj.product.price_cents * obj.quantity)
