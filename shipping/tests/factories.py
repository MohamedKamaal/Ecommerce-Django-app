import factory
from factory.django import DjangoModelFactory
from store.models import ProductVariation
from shipping.models import ShippingInfo
from django.contrib.auth import get_user_model
from orders.models import Order, OrderItem
from store.models import Product

User = get_user_model()

class ShippingInfoFactory(DjangoModelFactory):
    class Meta:
        model = ShippingInfo

    user = factory.SubFactory('users.tests.factories.UserFactory')
    first_name = 'John'
    last_name = 'Doe'
    email = 'john.doe@example.com'
    address = '123 Main St'


