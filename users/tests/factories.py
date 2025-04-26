"""
Factories for generating test data for the custom User model.
"""

import factory
from django.contrib.auth import get_user_model
from factory.django import DjangoModelFactory

User = get_user_model()

class UserFactory(DjangoModelFactory):
    """
    Factory for creating User instances for testing.
    """
    email = factory.Sequence(lambda n: f"user{n}@example.com")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    is_active = True
    is_staff = False
    is_superuser = False

    class Meta:
        model = User

    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        password = extracted if extracted else "defaultpass123"
        self.set_password(password)
        if create:
            self.save()
