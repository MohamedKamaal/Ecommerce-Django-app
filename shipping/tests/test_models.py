import pytest
from shipping.models import ShippingInfo
from shipping.tests.factories import ShippingInfoFactory
from users.tests.factories import UserFactory
from django.db import IntegrityError


@pytest.mark.django_db
def test_shipping_info_str_method():
    """
    Test the __str__ method returns the expected string.
    """
    shipping_info = ShippingInfoFactory()
    expected = f"{shipping_info.user.username} - {shipping_info.address}"
    assert str(shipping_info) == expected


@pytest.mark.django_db
def test_shipping_info_required_fields():
    """
    Check that required fields cannot be null.
    """
    with pytest.raises(IntegrityError):
        ShippingInfo.objects.create()


@pytest.mark.django_db
def test_shipping_info_creation_success():
    """
    Confirm that a ShippingInfo instance is created successfully with valid data.
    """
    shipping_info = ShippingInfoFactory(phone_number= "+201234567890")
    assert ShippingInfo.objects.count() == 1
    assert shipping_info.phone_number== "+201234567890"


@pytest.mark.django_db
def test_city_field_nullable():
    """
    Ensure the city field can be null if needed.
    """
    user = UserFactory()
    shipping = ShippingInfo.objects.create(
        user=user,
        first_name="Ali",
        last_name="Gamal",
        email="ali@example.com",
        address="Somewhere",
        postal_code="11111",
        phone_number="+201111111111",
        city=None
    )
    assert shipping.city is None


@pytest.mark.django_db
def test_foreign_key_user_deletion_cascades():
    """
    Ensure deleting a user cascades and deletes related ShippingInfo.
    """
    shipping_info = ShippingInfoFactory()
    user = shipping_info.user
    user.delete()
    assert ShippingInfo.objects.count() == 0
