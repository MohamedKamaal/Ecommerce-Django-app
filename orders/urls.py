from django.urls import path
from orders.views import (create_checkout_session,OrderCreationView,payment_success,payment_cancel)


urlpatterns = [
    path("",OrderCreationView.as_view(), name="checkout"),
    path("pay/", create_checkout_session, name="checkout-pay"),
    path("pay/success/", payment_success, name="success"),
    path("pay/cancel/", payment_cancel, name="cancel"),

]