from django import forms
from shipping.models import ShippingInfo
from cities_light.models import City
from phonenumber_field.formfields import PhoneNumberField


class ShippingInfoForm(forms.ModelForm):
    """
    Form for collecting and validating shipping information from the user.
    
    This form is used during checkout to collect:
    - First and last name
    - Email address
    - City (using Django Cities Light)
    - Address
    - Postal code
    - Phone number (validated using `phonenumber_field`)
    
    It also applies Tailwind CSS classes to widgets for styling.
    """

    city = forms.ModelChoiceField(
        queryset=City.objects.all(),
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control w-full px-3 mt-2 py-2 border focus:border-transparent '
                     'rounded-full focus:outline-none focus:ring-2 focus:ring-primary'
        })
    )
    """Dropdown for selecting city from Cities Light."""

    phone_number = PhoneNumberField(
        region="EG",
        widget=forms.TextInput(attrs={
            'placeholder': '+20 123 456 7890',
            'class': 'form-control w-full px-3 mt-2 py-2 border focus:border-transparent '
                     'rounded-full focus:outline-none focus:ring-2 focus:ring-primary'
        })
    )
    """Phone number input with validation and formatting for Egypt."""

    class Meta:
        model = ShippingInfo
        fields = [
            "first_name",
            "last_name",
            "email",
            "city",
            "address",
            "postal_code",
            "phone_number",
        ]
        widgets = {
            "first_name": forms.TextInput(attrs={
                "class": "w-full px-3 mt-2 py-2 border focus:border-transparent "
                         "rounded-full focus:outline-none focus:ring-2 focus:ring-primary"
            }),
            "last_name": forms.TextInput(attrs={
                "class": "w-full px-3 mt-2 py-2 border focus:border-transparent "
                         "rounded-full focus:outline-none focus:ring-2 focus:ring-primary"
            }),
            "email": forms.EmailInput(attrs={
                "class": "w-full px-3 mt-2 py-2 border focus:border-transparent "
                         "rounded-full focus:outline-none focus:ring-2 focus:ring-primary"
            }),
            "address": forms.Textarea(attrs={
                "class": "w-full px-3 mt-2 py-2 border focus:border-transparent "
                         "rounded-full focus:outline-none focus:ring-2 focus:ring-primary",
                "rows": 3
            }),
            "postal_code": forms.TextInput(attrs={
                "class": "w-full px-3 mt-2 py-2 border focus:border-transparent "
                         "rounded-full focus:outline-none focus:ring-2 focus:ring-primary"
            }),
        }
