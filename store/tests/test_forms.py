import pytest
from store.forms import QuantityForm

# Test valid form input
def test_quantity_form_valid():
    form = QuantityForm(data={"quantity": 5})
    assert form.is_valid()  # The form should be valid if the quantity is between 1 and 10
    assert form.cleaned_data["quantity"] == 5  # Ensure the cleaned data is correct

# Test invalid form input (quantity greater than 10)
def test_quantity_form_invalid_max():
    form = QuantityForm(data={"quantity": 15})
    assert not form.is_valid()  # The form should be invalid since 15 is greater than 10
    assert "quantity" in form.errors  # Check if the error for quantity field is raised

# Test invalid form input (quantity less than 1)
def test_quantity_form_invalid_min():
    form = QuantityForm(data={"quantity": 0})
    assert not form.is_valid()  # The form should be invalid since 0 is less than 1
    assert "quantity" in form.errors  # Check if the error for quantity field is raised
