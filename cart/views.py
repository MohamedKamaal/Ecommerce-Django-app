from django.shortcuts import render, get_object_or_404, redirect
from store.models import Product, ProductVariation
from cart.cart import Cart
from django.views.generic import TemplateView, View
from store.forms import QuantityForm
from django.core.exceptions import ValidationError
from django.http import Http404
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
        variation = get_object_or_404(ProductVariation, slug=slug)
        cart = Cart(request)
        quantity = 1  # Default quantity
        form = QuantityForm(request.GET)
        if form.is_valid():
            quantity = form.cleaned_data.get("quantity", 1)
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

        # Check if the item exists in the cart
        if str(id) not in cart.cart:
            raise Http404("Product variation not found in cart")
        quantity = int(cart.cart[str(id)]['quantity'])

        if action == "increment":
            if quantity + 1 > variation.stock:
                raise ValidationError("This exceeds our stock")
            cart.add(id, quantity=1)
        elif action == "decrement":
            cart.add(id, quantity=-1)
        
        else:
            raise Http404

        return redirect('cart')