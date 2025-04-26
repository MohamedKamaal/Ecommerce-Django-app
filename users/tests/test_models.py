"""
Tests for the custom User model.
"""

import pytest
from django.contrib.auth import get_user_model
from .factories import UserFactory

User = get_user_model()

@pytest.mark.django_db
class TestUserModel:

    def test_user_creation(self):
        user = UserFactory()
        assert isinstance(user, User)
        assert user.email is not None
        assert user.first_name
        assert user.check_password("defaultpass123")  # default from factory

    def test_superuser_creation(self):
        superuser = User.objects.create_superuser(
            email="admin@example.com",
            password="adminpass",
            first_name="adminfirst",
            last_name="adminlast",
        )
        assert superuser.is_superuser is True
        assert superuser.is_staff is True

    def test_email_user_method(self, mocker):
        user = UserFactory()
        mock_send = mocker.patch("users.models.send_mail")  # Patch where used
        user.email_user("Subject", "Body", from_email="admin@example.com")
        mock_send.assert_called_once()