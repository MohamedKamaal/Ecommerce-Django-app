"""
Custom authentication and registration forms extending django-allauth's LoginForm and SignupForm.
These forms apply Tailwind CSS classes for styling and add first and last name fields to the signup process.
"""

from allauth.account.forms import LoginForm, SignupForm
from django import forms



class CustomLoginForm(LoginForm):
    """
    Custom login form that extends allauth's LoginForm.

    - Applies Tailwind CSS classes to input fields for styling.
    - Updates the placeholder text for better UX.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the custom login form with custom CSS classes and placeholders for:
        - login (email)
        - password
        - remember me checkbox
        """
        super().__init__(*args, **kwargs)
        self.fields['login'].widget.attrs.update({
            'class': 'w-full px-3 py-1 border rounded-full focus:border-transparent focus:outline-none focus:ring-2 focus:ring-primary',
            'placeholder': 'Email address'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'w-full px-3 py-1 border rounded-full focus:border-transparent focus:outline-none focus:ring-2 focus:ring-primary',
            'placeholder': 'Password'
        })
        self.fields['remember'].widget.attrs.update({
            'class': 'mr-2'
        })


class CustomSignupForm(SignupForm):
    """
    Custom signup form that extends allauth's SignupForm.

    - Adds required first_name and last_name fields.
    - Applies Tailwind CSS classes for consistent styling.
    - Removes help text from password fields for a cleaner UI.
    """

    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    def __init__(self, *args, **kwargs):
        """
        Initialize the custom signup form with:
        - Tailwind styling for each input field.
        - Custom placeholders for clarity.
        - Help texts removed from password fields for minimalism.
        """
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({
            'class': 'w-full px-3 py-1 border rounded-full focus:border-transparent focus:outline-none focus:ring-2 focus:ring-primary',
            'placeholder': 'Email address'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'w-full px-3 py-1 border rounded-full focus:border-transparent focus:outline-none focus:ring-2 focus:ring-primary',
            'placeholder': 'Password',
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'w-full px-3 py-1 border rounded-full focus:border-transparent focus:outline-none focus:ring-2 focus:ring-primary',
            'placeholder': 'Password (again)'
        })
        self.fields['first_name'].widget.attrs.update({
            'class': 'w-full px-3 py-1 border rounded-full focus:border-transparent focus:outline-none focus:ring-2 focus:ring-primary',
            'placeholder': 'First Name'
        })
        self.fields['last_name'].widget.attrs.update({
            'class': 'w-full px-3 py-1 border rounded-full focus:border-transparent focus:outline-none focus:ring-2 focus:ring-primary',
            'placeholder': 'Last Name'
        })

        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

    def save(self, request):
        """
        Save method override to include first_name and last_name
        before saving the user instance to the database.
        """
        user = super().save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user
