"""URL paths for the 'cart' app (purchasing items)"""
from django.urls import path
from . import views


urlpatterns = [
    path('', views.view_cart, name='view_cart'),
]
