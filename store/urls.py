from django.urls import path
from .views import HomePageView, ProductDetailPage, ShopPageView

urlpatterns = [
    # Path for the shop page, where users can view products with filtering options
    path("shop/", ShopPageView.as_view(), name="shop"),
    
    # Path for the product detail page, using a slug to uniquely identify the product
    path("<slug:slug>/", ProductDetailPage.as_view(), name="product-detail"),
    
    # Path for the home page, which displays featured products, categories, etc.
    path("", HomePageView.as_view(), name="home"),
]
