from store.models import ProductVariation
import decimal
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError

class Cart:
    """
    A class to represent a shopping cart in the session.

    This class manages the cart in the session, allowing adding/removing items,
    updating quantities, and calculating totals.

    Attributes:
        session (Session): The session object from the request to store cart data.
        cart (dict): The dictionary representing the cart, stored in the session.
    """

    def __init__(self, request):
        """
        Initializes the cart.

        Retrieves the cart from the session, or creates a new cart if none exists.

        Args:
            request (HttpRequest): The HTTP request object containing the session.
        """
        self.session = request.session
        cart = self.session.get("cart", None)
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart
    
    def save(self):
        """
        Marks the session as modified to ensure the cart is saved.

        This method is called whenever the cart is updated.
        """
        self.session.modified = True 
    
    def clear(self):
        """
        Clears the cart from the session.

        This method removes the cart from the session and resets the in-memory cart.
        It then saves the session after clearing the cart.
        """
        self.session.pop("cart", None)  # Remove cart from session
        self.cart = {}  # Reset in-memory cart
        self.save()  # Ensure session modification

    def add(self, id, quantity=1, update_quantity=False):
        id = str(id)
        variation = get_object_or_404(ProductVariation, id=int(id))
        
        # Validate stock
        current_quantity = self.cart.get(id, {'quantity': 1})['quantity']
        new_quantity = quantity if update_quantity else current_quantity + quantity
        if new_quantity > variation.stock:
            raise ValidationError("This exceeds our stock")
        
        if id not in self.cart:
            self.cart[id] = {
                'id': int(id),
                'price_cents': int(variation.price_cents),
                'quantity': 1
            }
        
        if update_quantity:
            self.cart[id]['quantity'] = int(quantity)
        else:
            self.cart[id]['quantity'] += int(quantity)
        
        # Remove item if quantity becomes 0
        if self.cart[id]['quantity'] <= 0:
            self.remove(id)
        
        self.save()

    def remove(self, id):
        """
        Removes a ProductVariation from the cart.

        This method deletes the specified product variation from the cart.

        Args:
            id (int): The ID of the product variation to be removed.
        """
        id = str(id)
        if id in self.cart:
            del self.cart[id]
            self.save()
    
    def __len__(self):
        """
        Returns the total number of items in the cart.

        This method sums up the quantities of all items in the cart.

        Returns:
            int: The total number of items in the cart.
        """
        if len(self.cart.keys()) == 0:
            return 0
        else:
            return sum(
                int(item['quantity']) for item in self.cart.values()
            )
        
    def get_total_cost(self):
        """
        Calculates the total cost of all items in the cart.

        This method multiplies the price of each item by its quantity and sums up the result.

        Returns:
            decimal.Decimal: The total cost of the cart in decimal format (representing dollars).
        """
        return sum(
            int(item['price_cents']) * int(item['quantity']) for item in self.cart.values()
        ) / 100
    
    def __iter__(self):
        """
        Iterates over the items in the cart and retrieves additional product information.

        This method enriches the cart items with product details such as the image URL, product slug,
        and calculates the total price for each item.

        Yields:
            dict: Each item in the cart with additional information (name, price, total, etc.).
        """
        ids = self.cart.keys()
        product_variations = ProductVariation.objects.filter(id__in=ids)
        
        for variation in product_variations:
            self.cart[str(variation.id)]['id'] = variation.id
            self.cart[str(variation.id)]['quantity'] = self.cart[str(variation.id)]['quantity']
            self.cart[str(variation.id)]['image_url'] = variation.image
            self.cart[str(variation.id)]['product_slug'] = variation.product.slug
            self.cart[str(variation.id)]['slug'] = variation.slug
            self.cart[str(variation.id)]['name'] = variation.product.name
            self.cart[str(variation.id)]['total'] = (variation.price_cents * self.cart[str(variation.id)]['quantity']) / 100
        
        for item in self.cart.values():
            item['price'] = item['price_cents'] / 100
            yield item
