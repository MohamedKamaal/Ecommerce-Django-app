from django.shortcuts import render, get_object_or_404, redirect
from store.models import Product, ProductVariation
from cart.cart import Cart
from django.views.generic import TemplateView, View
from store.forms import QuantityForm
from django.core.exceptions import ValidationError

class CartPageView(TemplateView):
    """
    Renders the cart page displaying the contents of the cart.
    """
    template_name = "cart.html"

# View for adding a product variation to the cart
class CartAddView(View):
    """
    Handles adding a product variation to the cart. 
    If the product variation exists in the cart, it updates the quantity.
    """
    def get(self, request, slug):
        """
        Adds a ProductVariation to the cart based on the provided slug.
        
        Args:
            request (HttpRequest): The HTTP request containing the quantity.
            slug (str): The slug of the product variation to be added.
        
        Returns:
            HttpResponse: Redirects to the cart page.
        """
        variation = get_object_or_404(ProductVariation, slug=slug)
        cart = Cart(request)
        quantity = 1  # Default quantity is 1
        form = QuantityForm(request.GET)
        if form.is_valid():
            quantity = form.cleaned_data.get("quantity")
            if quantity > variation.stock:
                raise ValidationError("This exceeds our stock")
        cart.add(variation.id, quantity=quantity, update_quantity=True)
        return redirect('cart')

# View for resetting the cart (clearing all items)
class CartResetView(View):
    """
    Clears all items in the cart and redirects to the cart page.
    """
    def get(self, request):
        """
        Clears the cart and redirects to the cart page.
        
        Args:
            request (HttpRequest): The HTTP request object containing the session.

        Returns:
            HttpResponse: Redirects to the cart page.
        """
        cart = Cart(request)
        cart.clear()
        return redirect('cart')

# View for updating the quantity of a product variation in the cart
class CartUpdateView(View):
    """
    Handles updating the quantity of a product variation in the cart.
    It supports both incrementing and decrementing the quantity.
    """
    def get(self, request, id, action):
        """
        Updates the quantity of a product variation in the cart.

        Args:
            request (HttpRequest): The HTTP request object containing the session.
            id (int): The ID of the product variation to update.
            action (str): The action to perform ('increment' or 'decrement').

        Returns:
            HttpResponse: Redirects to the cart page after updating the quantity.
        """
        cart = Cart(request)
        variation = get_object_or_404(ProductVariation, id=id)
        quantity = int(cart.cart[str(id)]['quantity'])

        if action == "increment":
            if quantity + 1 > variation.stock:
                raise ValidationError("This exceeds our stock")
            cart.add(id, quantity=1)
        else:
            cart.add(id, quantity=-1)

        return redirect('cart')