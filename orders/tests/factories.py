import factory
from factory.django import DjangoModelFactory
from store.models import ProductVariation
from shipping.models import ShippingInfo
from django.contrib.auth import get_user_model
from orders.models import Order, OrderItem
from store.models import Product
from store.tests.factories import  ProductVariationFactory
from users.tests.factories import UserFactory
from shipping.tests.factories import ShippingInfoFactory

User = get_user_model()

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
