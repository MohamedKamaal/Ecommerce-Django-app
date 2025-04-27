from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from shipping.models import ShippingInfo
from shipping.forms import ShippingInfoForm
from cart.cart import Cart
from orders.models import Order, OrderItem
from store.models import ProductVariation
from payments.models import Payment
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string
from django.conf import settings


class OrderCreationView(LoginRequiredMixin, View):
    """
    Handles the creation of an order during the checkout process.

    Displays a form for the user to enter shipping information, creates the order, 
    sends an email confirmation, and clears the cart once the order is successfully 
    created.

    Methods:
        get(request): Displays the checkout page with the shipping info form.
        post(request): Handles the form submission, creating the order and order items.
    """
   
    def get(self, request):
        """
        Displays the checkout page with the user's shipping info form and total cost.

        If the user has previously entered shipping information, it is pre-filled 
        in the form. Otherwise, the form is populated with the user's details 
        (first name, last name, email).

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: The rendered checkout page.
        """
        cart = Cart(request)
        if len(cart) == 0:
            return redirect("shop")
        
        user = request.user
        past_shipping_info = ShippingInfo.objects.filter(user=user).last()
        if past_shipping_info:
            form = ShippingInfoForm(instance=past_shipping_info)         
        else:
            form = ShippingInfoForm(initial={
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email 
            })
        total = cart.get_total_cost() + 10
        context = {
            "form": form,
            "total": total,
        }
        return render(request, "checkout.html", context)
        
    def post(self, request):
        """
        Handles the submission of the shipping info form, creates the order and order items.

        If the form is valid, the order is created, payment email is sent to the user, 
        and the cart is cleared. Redirects the user to the payment checkout page.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: The rendered checkout page or a redirect to the payment page.
        """
        cart = Cart(request)
        if len(cart) == 0:
            return redirect("shop")
        
        total = cart.get_total_cost() + 10
        user = request.user
        past_shipping_info = ShippingInfo.objects.filter(user=user).last()
        if past_shipping_info:
            form = ShippingInfoForm(data=request.POST, instance=past_shipping_info)         
        else:
            form = ShippingInfoForm(data=request.POST)
        
        if form.is_valid():
            shipping_info = form.save(commit=False)
            shipping_info.user = user 
            shipping_info.save()
            
            # Create order & order items, send confirmation email & clear cart
            order = Order.objects.create(
                user=user,
                shipping_info=shipping_info,
                total_cents=total,
            )

            # Render the email content
            email_body = render_to_string("orders_emails/order-created.html", {"order": order})
            
            # Send the email
            user.send_mail(
                subject="Payment Successful",
                message="Your payment was successful.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                html_message=email_body
            )
            
            for item in cart:
                OrderItem.objects.create(
                    product=ProductVariation.objects.get(id=int(item['id'])),
                    quantity=item['quantity'],
                    total_cents=int(item['total']) * 100,
                    order=order
                )
            
            # Clear the cart and redirect to checkout payment
            cart.clear()
            request.session['order'] = {"order_id": order.id}
            return redirect("checkout-pay")
        
        else:
            print("Form errors:", form.errors)
            return render(request, "checkout.html", {"form": form, "total": total})  


def create_checkout_session(request):
    """
    Creates a Stripe checkout session for processing the payment.

    This view sets up the payment session with Stripe, generates the line items 
    from the order, and redirects the user to the Stripe checkout page for 
    payment.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponseRedirect: Redirects the user to the Stripe checkout session.
    """
    try:
        order_data = request.session.get("order", {})  # Returns {} if 'order' doesn't exist
        order_id = order_data.get("order_id")  # Returns None if key doesn't exist
        order = get_object_or_404(Order, id=int(order_id))
        
        line_items = []
        order_id = order.id
        for item in order.items.all():
            price = int(item.product.price_cents)
            quantity = int(item.quantity)
            name = str(item.product.product.name)
            
            image_url = str(item.product.image)
            images = [image_url]

            line_items.append({
                "price_data": {
                    "currency": "usd",
                    "product_data": {"name": name, "images": images},
                    "unit_amount": price,
                },
                "quantity": quantity,
            })

        shipping_fee = 1000  # $10.00 in cents
        line_items.append({
            "price_data": {
                "currency": "usd",
                "product_data": {
                    "name": "Shipping Fee",
                    "description": "Standard delivery"
                },
                "unit_amount": shipping_fee,
            },
            "quantity": 1,
        })
        
        # Create Stripe checkout session
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="payment",
            success_url=f"http://localhost:8000/pay/success?order_id={order_id}",
            cancel_url=f"http://localhost:8000/pay/cancel?order_id={order_id}",
            line_items=line_items,
            metadata={"order_id": order_id},
        )

        return redirect(session.url)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


def payment_success(request):
    """
    Handles successful payment processing and updates the order status.

    After the user completes the payment, this view marks the order as 'processing', 
    decreases the stock of the purchased items, and records the payment.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders a success page indicating the order has been processed.
    """
    order_id = request.GET.get("order_id")
    order = Order.objects.get(id=order_id)
    order.status = "processing"
    order.is_paid = True
    order.save()
    
    # Update product stock and create a payment record
    for item in order.items.all():
        item.product.stock -= item.quantity
        item.save()
    
    Payment.objects.create(
        order=order,
        total_cents=order.total_cents,
    )
    
    request.session["order"] = {}
    
    return render(request, "orders/success.html")


def payment_cancel(request):
    """
    Handles the cancellation of a payment.

    If the user cancels the payment process, they are redirected to the checkout 
    page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponseRedirect: Redirects the user to the checkout payment page.
    """
    return redirect("checkout-pay")
