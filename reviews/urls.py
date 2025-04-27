from django.urls import path 
from reviews.views import ReviewProductView

urlpatterns = [
    path("<slug:slug>/",ReviewProductView.as_view(), name="product-review"),
 
]