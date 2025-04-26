"""
Tests for custom login and signup forms.
"""

import pytest
from users.forms import CustomSignupForm, CustomLoginForm
from django.contrib.auth import get_user_model
from django.test import RequestFactory


User = get_user_model()

@pytest.mark.django_db
class TestSignupForm:

    def test_valid_signup_form(self):
        form = CustomSignupForm(data={
            "email": "newuser@example.com",
            "password1": "strongpass123",
            "password2": "strongpass123",
            "first_name": "John",
            "last_name": "Doe"
        })

        assert form.is_valid()

        factory = RequestFactory()
        request = factory.post("/accounts/signup/")
        request.session = {}  # mock session so allauth doesn't break

        user = form.save(request)

        assert user.first_name == "John"
        assert user.last_name == "Doe"
        assert User.objects.filter(email="newuser@example.com").exists()

    def test_passwords_mismatch(self):
        form = CustomSignupForm(data={
            "email": "fail@example.com",
            "password1": "1234543y6",
            "password2": "65432184",
            "first_name": "Foo",
            "last_name": "Bar"
        })
        assert not form.is_valid()
        assert "password2" in form.errors

@pytest.mark.django_db
class TestLoginForm:

    def test_login_form_fields_present(self):
        form = CustomLoginForm()
        assert "login" in form.fields
        assert "password" in form.fields
