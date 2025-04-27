from django.contrib import admin
from django.urls import path, include
import store, cart, reviews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),  # Allauth URLs
    path('cart/', include("cart.urls")),
    path('checkout/', include("orders.urls")),
    path('reviews/', include("reviews.urls")),
    path('', include("store.urls")),
]
