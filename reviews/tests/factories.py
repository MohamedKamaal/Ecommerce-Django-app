import factory
from factory import Faker, SubFactory
from factory.django import DjangoModelFactory
from django.utils.timezone import now
from users.tests.factories import UserFactory
from store.tests.factories import  ProductFactory

from store.models import  Product
from reviews.models import Review


class ReviewFactory(DjangoModelFactory):
    class Meta:
        model = Review

    product = SubFactory(ProductFactory)
    rating = factory.Iterator([1, 2, 3, 4, 5])
    review = Faker("paragraph")

    # Default: authenticated user review
    user = SubFactory(UserFactory)
    name = None
    email = None

   