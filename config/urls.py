from django.contrib import admin
from django.urls import path, include
import store

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),  # Allauth URLs
    path('', include("store.urls")),
]
