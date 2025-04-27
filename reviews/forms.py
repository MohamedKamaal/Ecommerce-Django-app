from django import forms
from reviews.models import Review
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError

class ReviewForm(forms.ModelForm):
    """
    A form for submitting product reviews.
    
    This form allows users to provide a review for a product. It includes fields for the user's name, 
    email (optional for anonymous reviews), a rating (from 1 to 5 stars), and the review text.
    
    The form includes validation for the fields and custom widget styling for the review input field.
    """
    
    class Meta:
        model = Review
        fields = ["name", "email", "rating", "review"]
        widgets = {
            "review": forms.TextInput(
                attrs={
                    "class": "mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm",
                    "placeholder": "Write your review",
                    "rows": 4
                }
            )
        }
    
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email:
            validator = EmailValidator()
            try:
                validator(email)
            except ValidationError:
                raise forms.ValidationError("Enter a valid email address.")
        return email
