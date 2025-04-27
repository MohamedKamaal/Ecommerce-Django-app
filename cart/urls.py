from django.urls import path
from cart.views import (CartPageView, CartAddView, CartResetView,CartUpdateView)



urlpatterns = [
    path("<slug:slug>/add-to-cart",CartAddView.as_view(), name="cart-add"),
    path("<int:id>/update/<str:action>/",CartUpdateView.as_view(), name="cart-update"),
    path("reset/",CartResetView.as_view(), name="cart-reset"),
    path("",CartPageView.as_view(), name="cart"),
   
]