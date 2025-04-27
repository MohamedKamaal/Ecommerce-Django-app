import pytest
from shipping.forms import ShippingInfoForm
from shipping.tests.factories import UserFactory, CityFactory
from phonenumber_field.phonenumber import PhoneNumber


@pytest.mark.django_db
def test_form_valid_data():
    """
    Ensure the form is valid with correct data and cleaned properly.
    """
    user = UserFactory()
    city = CityFactory()
    
    form_data = {
        "first_name": "Ahmed",
        "last_name": "Youssef",
        "email": "ahmed@example.com",
        "city": city.pk,
        "address": "123 Nile Street",
        "postal_code": "12345",
        "phone_number": "+201234567890"
    }

    form = ShippingInfoForm(data=form_data)
    assert form.is_valid(), form.errors
    assert isinstance(form.cleaned_data["phone_number"], PhoneNumber)


@pytest.mark.django_db
def test_form_missing_required_fields():
    """
    Form should be invalid if required fields are missing.
    """
    form = ShippingInfoForm(data={})
    assert not form.is_valid()
    required_fields = ["first_name", "last_name", "email", "city", "address", "postal_code", "phone_number"]
    for field in required_fields:
        assert field in form.errors


@pytest.mark.django_db
def test_invalid_email_and_phone():
    """
    Form should raise validation errors on invalid email and phone number.
    """
    city = CityFactory()
    form_data = {
        "first_name": "Ali",
        "last_name": "Gamal",
        "email": "not-an-email",
        "city": city.pk,
        "address": "456 River Rd",
        "postal_code": "0000",
        "phone_number": "invalid-phone"
    }

    form = ShippingInfoForm(data=form_data)
    assert not form.is_valid()
    assert "email" in form.errors
    assert "phone_number" in form.errors


@pytest.mark.django_db
def test_form_widgets_classes():
    """
    Ensure that widgets use the correct Tailwind CSS classes.
    """
    form = ShippingInfoForm()
    for field_name, field in form.fields.items():
        widget_class = field.widget.attrs.get("class", "")
        assert "rounded-full" in widget_class
        assert "focus:ring-primary" in widget_class
