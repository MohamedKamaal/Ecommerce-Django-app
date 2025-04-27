from django import forms 


# Form to handle quantity input
class QuantityForm(forms.Form):
    """
    Form for handling product quantity input.
    
    Attributes:
        quantity (IntegerField): The quantity of the product. It must be between 1 and 10.
    """
    quantity = forms.IntegerField(max_value=10, min_value=1)