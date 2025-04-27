from cart.cart import Cart

def cart(request):
    """
    Retrieves the current cart object and returns it as part of the context.

    Args:
        request (HttpRequest): The HTTP request object containing the session.

    Returns:
        dict: A dictionary containing the cart object.
    """
    cart = Cart(request)
    return {"cart": cart}