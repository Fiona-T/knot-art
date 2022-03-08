"""URL paths for the 'products' app (shop)"""
from django.urls import path
from . import views


urlpatterns = [
    path('', views.show_products, name='products'),
]
